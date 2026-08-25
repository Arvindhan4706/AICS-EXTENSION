"""
CyberShield AI - Email & QR Code Parsing Module
Parses EML headers, SPF/DKIM flags, links, attachments, and extracts URLs from QR code images.
"""

import re
import email
from email import policy
from urllib.parse import urlparse

def parse_eml_content(raw_eml: str) -> dict:
    """
    Parses EML message structure to extract header signals, links, attachments, and authentication records.
    """
    msg = email.message_from_string(raw_eml, policy=policy.default)
    
    sender = msg.get('From', '')
    subject = msg.get('Subject', '')
    reply_to = msg.get('Reply-To', '')
    received = msg.get_all('Received', [])
    
    # Body extraction
    body_text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ['text/plain', 'text/html']:
                body_text += part.get_payload(decode=True).decode('utf-8', errors='ignore')
    else:
        body_text = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
    # Extract links from email body
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    extracted_urls = re.findall(url_pattern, body_text)
    
    # Check SPF / DKIM status from Authentication-Results header
    auth_results = msg.get('Authentication-Results', '').lower()
    spf_pass = 1 if 'spf=pass' in auth_results else (0 if 'spf=fail' in auth_results else -1)
    dkim_pass = 1 if 'dkim=pass' in auth_results else (0 if 'dkim=fail' in auth_results else -1)
    dmarc_pass = 1 if 'dmarc=pass' in auth_results else (0 if 'dmarc=fail' in auth_results else -1)
    
    # Attachment count
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_filename():
                attachments.append(part.get_filename())
                
    # Detect Spoofing (From domain != Reply-To domain)
    from_domain = urlparse('http://' + sender.split('@')[-1].strip('>')).netloc if '@' in sender else ''
    reply_domain = urlparse('http://' + reply_to.split('@')[-1].strip('>')).netloc if '@' in reply_to else ''
    spoofing_detected = 1 if (reply_domain and from_domain and reply_domain != from_domain) else 0

    return {
        'sender': sender,
        'subject': subject,
        'reply_to': reply_to,
        'extracted_urls': extracted_urls,
        'url_count': len(extracted_urls),
        'attachment_count': len(attachments),
        'attachments': attachments,
        'spf_status': spf_pass,
        'dkim_status': dkim_pass,
        'dmarc_status': dmarc_pass,
        'spoofing_detected': spoofing_detected,
        'body_length': len(body_text)
    }

def decode_qr_image_url(qr_decoded_text: str) -> str:
    """
    Decodes QR target text and formats URL for threat scanning.
    """
    cleaned = qr_decoded_text.strip()
    if not cleaned.startswith(('http://', 'https://')):
        cleaned = 'http://' + cleaned
    return cleaned
