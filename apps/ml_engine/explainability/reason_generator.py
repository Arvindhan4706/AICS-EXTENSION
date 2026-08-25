"""
CyberShield AI - Human Readable Explainable AI (XAI) & Reason Generator
Maps feature values and SHAP contribution scores to human-understandable risk explanations,
MITRE ATT&CK techniques, OWASP Top 10 categories, and remediation recommendations.
"""

# Feature impact mapping rules
REASON_MAPPINGS = {
    'has_ip': {
        'title': 'IP Address Hostname Detected',
        'desc': 'URL uses a raw IP address instead of a domain name to bypass domain reputation checks.',
        'risk_level': 'HIGH',
        'mitre': 'T1566.002 - Phishing: Spearphishing Link',
        'owasp': 'A01:2021 - Broken Access Control'
    },
    'is_shortened': {
        'title': 'URL Shortening Abuse',
        'desc': 'Target URL utilizes a redirection shortening service (e.g. bit.ly, tinyurl) to obfuscate final destination.',
        'risk_level': 'MEDIUM',
        'mitre': 'T1027 - Obfuscated Files or Information',
        'owasp': 'A04:2021 - Insecure Design'
    },
    'has_homograph_unicode': {
        'title': 'Homograph / Typosquatting Attack',
        'desc': 'Domain contains non-ASCII Unicode characters masquerading as legitimate brand letters (Cyrillic lookalikes).',
        'risk_level': 'CRITICAL',
        'mitre': 'T1036.007 - Masquerading: Double Extension / Lookalike Domain',
        'owasp': 'A07:2021 - Identification and Authentication Failures'
    },
    'external_form_action': {
        'title': 'Cross-Domain Credential Harvesting Form',
        'desc': 'HTML login form posts sensitive inputs to an unverified third-party external server.',
        'risk_level': 'CRITICAL',
        'mitre': 'T1556 - Modify Authentication Process',
        'owasp': 'A03:2021 - Injection'
    },
    'has_password_field': {
        'title': 'Password Input Field Present',
        'desc': 'Page collects password credentials, elevating risk if domain authenticity is untrusted.',
        'risk_level': 'MEDIUM',
        'mitre': 'T1552 - Unsecured Credentials',
        'owasp': 'A07:2021 - Identification and Authentication Failures'
    },
    'has_obfuscated_js': {
        'title': 'Obfuscated JavaScript Code',
        'desc': 'Page executes encrypted or eval/unescape obfuscated scripts designed to hide malware downloaders.',
        'risk_level': 'HIGH',
        'mitre': 'T1027.002 - Obfuscated Files or Information: Software Packing',
        'owasp': 'A08:2021 - Software and Data Integrity Failures'
    },
    'tld_risk_score': {
        'title': 'High Risk Top-Level Domain (TLD)',
        'desc': 'Domain uses a top-level extension frequently associated with disposable scam websites (.xyz, .top, .tk).',
        'risk_level': 'MEDIUM',
        'mitre': 'T1583.001 - Acquire Infrastructure: Domains',
        'owasp': 'A05:2021 - Security Misconfiguration'
    },
    'keyword_match_count': {
        'title': 'Sensitive Phishing Keywords Detected',
        'desc': 'URL includes high-risk brand or security bait terms ("verify", "banking", "update-security").',
        'risk_level': 'HIGH',
        'mitre': 'T1566.002 - Phishing: Spearphishing Link',
        'owasp': 'A07:2021 - Identification and Authentication Failures'
    },
    'url_entropy': {
        'title': 'High URL Character Randomness (Entropy)',
        'desc': 'URL path or parameter structure exhibits algorithmic randomness common in automated scam generators.',
        'risk_level': 'MEDIUM',
        'mitre': 'T1568 - Dynamic Resolution',
        'owasp': 'A04:2021 - Insecure Design'
    }
}

def generate_explanation_report(feature_dict: dict, shap_values: dict, threat_score: float) -> dict:
    """
    Generates human-readable explanations, top risk factors, MITRE ATT&CK mapping, and mitigation steps.
    """
    reasons = []
    mitre_mappings = set()
    owasp_mappings = set()
    
    # Sort features by SHAP impact score descending
    sorted_features = sorted(shap_values.items(), key=lambda item: abs(item[1]), reverse=True)
    
    for feat_name, impact in sorted_features:
        if feat_name in REASON_MAPPINGS and feature_dict.get(feat_name, 0) > 0:
            info = REASON_MAPPINGS[feat_name]
            reasons.append({
                'feature': feat_name,
                'title': info['title'],
                'description': info['desc'],
                'risk_level': info['risk_level'],
                'impact_score': round(float(impact), 4),
                'contribution_percentage': f"+{int(abs(impact) * 100)}%" if impact > 0 else f"-{int(abs(impact) * 100)}%"
            })
            mitre_mappings.add(info['mitre'])
            owasp_mappings.add(info['owasp'])
            
    # Default fallback if no specific rule matched
    if not reasons and threat_score > 50:
        reasons.append({
            'feature': 'composite_risk',
            'title': 'Suspicious Behavioral Combination',
            'description': 'Multiple subtle statistical indicators combined exceed safe domain thresholds.',
            'risk_level': 'MEDIUM',
            'impact_score': 0.35,
            'contribution_percentage': '+35%'
        })
        mitre_mappings.add('T1566 - Phishing')
        owasp_mappings.add('A04:2021 - Insecure Design')
        
    # Recommendations
    if threat_score >= 70:
        recommendations = [
            "DO NOT enter any passwords, credit card numbers, or personal credentials.",
            "Close the browser tab immediately and report the URL to your security operations team.",
            "Verify the official website URL directly through a trusted bookmark or web search."
        ]
    elif threat_score >= 40:
        recommendations = [
            "Proceed with extreme caution. Verify SSL certificate issuer before continuing.",
            "Check whether the domain URL matches the official brand name exactly."
        ]
    else:
        recommendations = [
            "URL appears safe based on structural and threat intelligence analysis.",
            "Always ensure HTTPS is active when submitting sensitive forms."
        ]

    return {
        'reasons': reasons[:5],  # Top 5 contributing explanations
        'mitre_attack': list(mitre_mappings),
        'owasp_top10': list(owasp_mappings),
        'recommendations': recommendations
    }
