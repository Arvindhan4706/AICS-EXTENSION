"""
CyberShield AI Email & EML Threat Scanner API Router
Parses email headers, SPF/DKIM validation, extracts links, and scans links via ML model engine.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.schemas import EmailScanRequest
from apps.ml_engine.feature_extraction.email_qr_features import parse_eml_content
from app.ml.email_classifier import MLEmailClassifier
from app.scanner.orchestrator import ScanOrchestrator
from app.ml.feature_engine import FeatureEngine
from app.ml.ensemble import MLEnsemble
from app.ml.risk_engine import RiskEngine
import asyncio

router = APIRouter(prefix="/email", tags=["Email Scanner"])
email_nlp_engine = MLEmailClassifier()

async def scan_url_sync(url: str):
    try:
        orchestrator = ScanOrchestrator()
        analysis_results = await orchestrator.run_scan(url)
        feature_engine = FeatureEngine()
        features = feature_engine.extract_features(analysis_results.get("analysis", {}))
        ensemble = MLEnsemble()
        prediction = ensemble.predict(features)
        risk_engine = RiskEngine()
        risk_assessment = risk_engine.calculate_risk(prediction, analysis_results.get("analysis", {}))
        return {'threat_score': risk_assessment.get('risk_score', 15), 'risk_level': risk_assessment.get('risk_level', 'LOW')}
    except Exception:
        return {'threat_score': 15, 'risk_level': 'LOW'}

@router.post("/scan-eml")
async def scan_eml_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    raw_eml = content.decode('utf-8', errors='ignore')
    
    parsed = parse_eml_content(raw_eml)
    
    # Scan extracted URLs
    url_results = []
    max_threat = 0
    for url in parsed['extracted_urls'][:5]: # Scan top 5 links
        res = await scan_url_sync(url)
        url_results.append(res)
        if res['threat_score'] > max_threat:
            max_threat = res['threat_score']
            
    # NLP Email Text Analysis
    nlp_res = email_nlp_engine.predict(raw_eml)
    nlp_score = nlp_res['threat_score']
    
    # Email overall threat score calculation
    spf_penalty = 25 if parsed['spf_status'] == 0 else 0
    dkim_penalty = 25 if parsed['dkim_status'] == 0 else 0
    spoof_penalty = 30 if parsed['spoofing_detected'] == 1 else 0
    
    overall_score = min(100, max(max_threat, nlp_score, spf_penalty + dkim_penalty + spoof_penalty))
    
    if overall_score >= 70:
        email_risk = "CRITICAL PHISHING EMAIL"
    elif overall_score >= 40:
        email_risk = "SUSPICIOUS EMAIL"
    else:
        email_risk = "SAFE EMAIL"

    return {
        'filename': file.filename,
        'overall_threat_score': overall_score,
        'email_risk_level': email_risk,
        'parsed_metadata': parsed,
        'link_analysis_results': url_results
    }

@router.post("/scan-text")
async def scan_email_text(payload: EmailScanRequest, db: Session = Depends(get_db)):
    if not payload.email_text:
        raise HTTPException(status_code=400, detail="No email text provided.")
        
    parsed = parse_eml_content(payload.email_text)
    
    url_results = []
    for u in parsed['extracted_urls'][:5]:
        res = await scan_url_sync(u)
        url_results.append(res)
        
    max_threat = max([r['threat_score'] for r in url_results], default=15)
    
    nlp_res = email_nlp_engine.predict(payload.email_text)
    nlp_score = nlp_res['threat_score']
    
    final_score = max(max_threat, nlp_score)
    
    return {
        'overall_threat_score': final_score,
        'email_risk_level': 'HIGH' if final_score > 60 else 'LOW',
        'nlp_analysis': nlp_res,
        'parsed_metadata': parsed,
        'link_analysis_results': url_results
    }
