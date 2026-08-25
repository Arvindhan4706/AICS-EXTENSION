"""
CyberShield AI - Lexical & URL Feature Extraction Engine
Extracts 15+ lexical, statistical, and structural features from target URLs.
"""

import re
import math
from urllib.parse import urlparse, parse_qs

# Known URL Shorteners
SHORTENERS = {
    'bit.ly', 'goo.gl', 'tinyurl.com', 'is.gd', 'cli.gs', 'yfrog.com', 
    'migre.me', 'ff.im', 'tiny.cc', 'url4.eu', 'twit.ac', 'su.pr', 
    'twurl.nl', 'snipurl.com', 'short.to', 'BudURL.com', 'ping.fm', 
    'post.ly', 'Just.as', 'bkite.com', 'snipr.com', 'fic.kr', 'loopt.us'
}

# Suspicious Phishing Keywords
SUSPICIOUS_KEYWORDS = [
    'login', 'signin', 'verify', 'update', 'account', 'banking', 'secure',
    'confirm', 'password', 'credential', 'support', 'wallet', 'paypal',
    'netflix', 'amazon', 'appleid', 'microsoft', 'google', 'meta', 'meta-mask',
    'binance', 'coinbase', 'security-update', 'validation', 'billing'
]

def calculate_entropy(text: str) -> float:
    """Calculate Shannon Entropy of a string to detect random obfuscation."""
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum([p * math.log2(p) for p in prob])

def is_ip_address(domain: str) -> int:
    """Checks if domain is an IPv4 or IPv6 address."""
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    hex_ip_pattern = r'^0x[0-9a-fA-F]+\.'
    return 1 if re.match(ip_pattern, domain) or re.match(hex_ip_pattern, domain) else 0

def extract_url_lexical_features(url: str) -> dict:
    """
    Extracts high-dimensional lexical features from a URL.
    Returns dictionary of numerical and categorical metrics.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path
    query = parsed.query
    
    # Strip port if present
    domain_clean = domain.split(':')[0]
    
    features = {
        'url_length': len(url),
        'domain_length': len(domain_clean),
        'path_length': len(path),
        'has_ip': is_ip_address(domain_clean),
        'dot_count': url.count('.'),
        'hyphen_count_domain': domain_clean.count('-'),
        'at_count': url.count('@'),
        'question_mark_count': url.count('?'),
        'equal_count': url.count('='),
        'slash_count': url.count('/'),
        'numeric_ratio_url': sum(c.isdigit() for c in url) / max(len(url), 1),
        'numeric_ratio_domain': sum(c.isdigit() for c in domain_clean) / max(len(domain_clean), 1),
        'url_entropy': round(calculate_entropy(url), 4),
        'domain_entropy': round(calculate_entropy(domain_clean), 4),
        'is_shortened': 1 if domain_clean in SHORTENERS or any(s in url for s in SHORTENERS) else 0,
        'has_https': 1 if parsed.scheme == 'https' else 0,
        'subdomain_count': max(0, len(domain_clean.split('.')) - 2),
        'keyword_match_count': sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in url.lower()),
        'has_homograph_unicode': 1 if any(ord(c) > 127 for c in domain) else 0
    }
    
    return features

if __name__ == '__main__':
    test_url = "http://192.168.1.1/paypal-security-update/verify.php?user=123@admin"
    print("Extracted URL Features:", extract_url_lexical_features(test_url))
