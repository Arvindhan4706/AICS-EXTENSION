"""
CyberShield AI - Advanced JavaScript & Browser API Feature Extraction
Extracts script complexity, permission requests, and browser API fingerprinting indicators.
"""

def extract_js_behavior_features(js_code: str) -> dict:
    """
    Analyzes JavaScript code snippet for malicious behavior, fingerprinting, and permission abuse.
    """
    if not js_code:
        return {
            'canvas_fingerprinting': 0,
            'webrtc_ip_leak': 0,
            'localstorage_abuse': 0,
            'clipboard_hijack': 0,
            'websocket_usage': 0,
            'service_worker_abuse': 0,
            'permission_request_count': 0,
            'obfuscation_score': 0.0
        }
        
    code_lower = js_code.lower()
    
    canvas_fp = 1 if ('toDataURL' in js_code or 'getImageData' in js_code) and 'canvas' in code_lower else 0
    webrtc = 1 if 'RTCPeerConnection' in js_code or 'createDataChannel' in js_code else 0
    localstorage = 1 if 'localStorage' in js_code or 'sessionStorage' in js_code else 0
    clipboard = 1 if 'navigator.clipboard' in js_code or 'execCommand("copy")' in js_code else 0
    websocket = 1 if 'WebSocket(' in js_code else 0
    sw = 1 if 'serviceWorker.register' in js_code else 0
    
    perm_requests = sum(1 for perm in ['geolocation', 'notifications', 'camera', 'microphone'] if perm in code_lower)
    
    # Calculate crude obfuscation ratio
    obfuscation_keywords = ['eval', 'unescape', 'atob', 'btoa', 'string.fromcharcode', 'decodeuricomponent']
    matches = sum(1 for kw in obfuscation_keywords if kw in code_lower)
    obfuscation_score = min(1.0, round(matches * 0.25, 2))
    
    return {
        'canvas_fingerprinting': canvas_fp,
        'webrtc_ip_leak': webrtc,
        'localstorage_abuse': localstorage,
        'clipboard_hijack': clipboard,
        'websocket_usage': websocket,
        'service_worker_abuse': sw,
        'permission_request_count': perm_requests,
        'obfuscation_score': obfuscation_score
    }
