"""
CyberShield AI - Main Prediction & Analysis Orchestrator
Coordinates feature extraction, Threat Intelligence lookup, ML model ensemble inference, and XAI report generation.
"""

import os
import requests
from bs4 import BeautifulSoup
from apps.ml_engine.feature_extraction.url_features import extract_url_lexical_features
from apps.ml_engine.feature_extraction.html_features import extract_html_dom_features
from apps.ml_engine.feature_extraction.dns_ssl_features import extract_dns_ssl_features
from apps.ml_engine.feature_extraction.js_dom_features import extract_js_behavior_features
from apps.ml_engine.models.ensemble import CyberShieldEnsemble
from apps.ml_engine.explainability.reason_generator import generate_explanation_report

# Singleton Ensemble Model Instance
ensemble_engine = CyberShieldEnsemble()

def threat_intel_lookup(url: str, domain: str) -> dict:
    """Aggregates threat intelligence scores from external feeds."""
    intel = {
        'virustotal': {'positives': 0, 'total': 0, 'status': 'CLEAN'},
        'phishtank': {'in_database': 0, 'verified': False},
        'google_safe_browsing': {'matches': []},
        'abuse_ipdb': {'abuse_confidence_score': 0},
        'openphish': {'listed': 0}
    }
    
    vt_api_key = os.getenv('VT_API_KEY')
    if vt_api_key:
        try:
            import base64
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            headers = {"x-apikey": vt_api_key}
            resp = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=2)
            if resp.status_code == 200:
                stats = resp.json().get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                intel['virustotal']['positives'] = stats.get('malicious', 0)
                intel['virustotal']['total'] = sum(stats.values())
                intel['virustotal']['status'] = 'FLAGGED' if stats.get('malicious', 0) > 0 else 'CLEAN'
        except Exception:
            pass

    gsb_api_key = os.getenv('GSB_API_KEY')
    if gsb_api_key:
        try:
            payload = {
                "client": {"clientId": "cybershield", "clientVersion": "1.0"},
                "threatInfo": {
                    "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url}]
                }
            }
            resp = requests.post(f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={gsb_api_key}", json=payload, timeout=2)
            if resp.status_code == 200:
                matches = resp.json().get('matches', [])
                intel['google_safe_browsing']['matches'] = [m['threatType'] for m in matches]
        except Exception:
            pass
            
    return intel

import concurrent.futures
from functools import lru_cache

def map_to_uci_features(features: dict) -> dict:
    """Maps extracted internal features to the 30 UCI ARFF dataset features (-1 for phishing, 1 for legit, 0 for suspicious)"""
    uci = {}
    uci['having_IP_Address'] = -1 if features.get('has_ip', 0) == 1 else 1
    uci['URL_Length'] = -1 if features.get('url_length', 0) > 75 else (0 if features.get('url_length', 0) > 54 else 1)
    uci['Shortining_Service'] = -1 if features.get('is_shortened', 0) == 1 else 1
    uci['having_At_Symbol'] = -1 if features.get('at_count', 0) > 0 else 1
    uci['double_slash_redirecting'] = -1 if features.get('slash_count', 0) > 5 else 1
    uci['Prefix_Suffix'] = -1 if features.get('hyphen_count_domain', 0) > 0 else 1
    uci['having_Sub_Domain'] = -1 if features.get('subdomain_count', 0) > 2 else (0 if features.get('subdomain_count', 0) == 2 else 1)
    uci['SSLfinal_State'] = 1 if features.get('ssl_valid', 0) == 1 else -1
    uci['Domain_registeration_length'] = -1 if features.get('age_of_domain', 0) < 365 else 1
    uci['Favicon'] = -1 if features.get('external_favicon', 0) == 1 else 1
    uci['port'] = 1 # Default standard
    uci['HTTPS_token'] = -1 if 'https' in features.get('domain', '') else 1
    uci['Request_URL'] = -1 if features.get('external_script_ratio', 0.0) > 0.61 else 1
    uci['URL_of_Anchor'] = 1 # Default approximation
    uci['Links_in_tags'] = 1 
    uci['SFH'] = -1 if features.get('external_form_action', 0) == 1 else 1
    uci['Submitting_to_email'] = 1 
    uci['Abnormal_URL'] = -1 if features.get('keyword_match_count', 0) > 1 else 1
    uci['Redirect'] = -1 if features.get('slash_count', 0) > 4 else 1
    uci['on_mouseover'] = -1 if features.get('suspicious_popup_scripts', 0) > 0 else 1
    uci['RightClick'] = -1 if features.get('has_disabled_right_click', 0) == 1 else 1
    uci['popUpWidnow'] = -1 if features.get('suspicious_popup_scripts', 0) > 0 else 1
    uci['Iframe'] = -1 if features.get('iframe_count', 0) > 0 else 1
    uci['age_of_domain'] = -1 if features.get('age_of_domain', 0) < 180 else 1
    uci['DNSRecord'] = 1 if features.get('dns_has_a_record', 0) == 1 else -1
    uci['web_traffic'] = 1 # Approximation
    uci['Page_Rank'] = 1
    uci['Google_Index'] = 1
    uci['Links_pointing_to_page'] = 1
    uci['Statistical_report'] = -1 if features.get('tld_risk_score', 0) > 0.5 else 1
    return uci

@lru_cache(maxsize=1024)
def analyze_target_url(url: str, html_content: str = "", js_code: str = "") -> dict:
    """
    Complete end-to-end cyber threat assessment workflow.
    Returns Threat Score, Risk Level, Model Breakdown, Threat Intel, XAI Explanations, and Mitigations.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    # Live Web Scraping
    if not html_content:
        try:
            resp = requests.get(url, timeout=3, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200:
                html_content = resp.text
                soup = BeautifulSoup(html_content, 'html.parser')
                js_snippets = [script.string for script in soup.find_all('script') if script.string]
                js_code = "\n".join(js_snippets)
        except Exception:
            pass # Fail gracefully if unreachable
            
    # 1. Feature Extraction (Parallelized)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_url = executor.submit(extract_url_lexical_features, url)
        future_html = executor.submit(extract_html_dom_features, html_content, url)
        future_dns = executor.submit(extract_dns_ssl_features, url)
        future_js = executor.submit(extract_js_behavior_features, js_code)
        
        url_feats = future_url.result()
        html_feats = future_html.result()
        dns_ssl_feats = future_dns.result()
        js_feats = future_js.result()
    
    # Merge into master feature dictionary
    all_features = {**url_feats, **html_feats, **dns_ssl_feats, **js_feats}
    
    # 2. Threat Intel Aggregation
    domain = url_feats.get('domain', url)
    threat_intel = threat_intel_lookup(url, domain)
    
    # Map to UCI features
    uci_mapped_features = map_to_uci_features(all_features)
    
    # 3. Machine Learning Ensemble Prediction
    ml_result = ensemble_engine.predict(uci_mapped_features)
    
    # Threat score calculation combining ML prob & Threat Intel hits
    base_ml_score = ml_result['threat_score']
    intel_boost = 25 if threat_intel['virustotal']['positives'] > 0 else 0
    final_threat_score = min(100, max(0, base_ml_score + intel_boost))
    
    # Risk Level Determination
    if final_threat_score >= 75:
        risk_level = "CRITICAL"
        risk_color = "red"
        category = "Phishing & Credential Harvesting Website"
    elif final_threat_score >= 50:
        risk_level = "HIGH"
        risk_color = "orange"
        category = "Suspicious Domain / Potential Scam"
    elif final_threat_score >= 25:
        risk_level = "MEDIUM"
        risk_color = "yellow"
        category = "Unverified Low-Reputation Site"
    else:
        risk_level = "LOW"
        risk_color = "green"
        category = "Legitimate Web Application"
        
    # 4. Explainable AI Reason Generation
    xai_report = generate_explanation_report(uci_mapped_features, ml_result['shap_values'], final_threat_score)

    return {
        'url': url,
        'threat_score': final_threat_score,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'category': category,
        'probability': ml_result['ensemble_probability'],
        'model_breakdown': ml_result['model_breakdown'],
        'features_extracted': all_features,
        'threat_intelligence': threat_intel,
        'explainable_ai': xai_report
    }

if __name__ == '__main__':
    test_res = analyze_target_url("http://192.168.1.1/paypal-verify-billing/login.php?id=8823")
    import json
    print(json.dumps(test_res, indent=2))
