"""
CyberShield AI Real-Time URL Scanner API Router
Integrates ML feature extraction, ensemble model inference, Threat Intel aggregation, and Explainable AI.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.schemas.schemas import URLScanRequest
from app.models.models import ScanLog, BlacklistWhitelist
from apps.ml_engine.predict import analyze_target_url

router = APIRouter(prefix="/scan", tags=["URL Scanner"])

@router.post("/url")
def scan_url(payload: URLScanRequest, db: Session = Depends(get_db)):
    if not payload.url or len(payload.url.strip()) < 3:
        raise HTTPException(status_code=400, detail="Invalid target URL provided.")
        
    url = payload.url.strip()
    
    # 1. Check Blacklist / Whitelist override
    blacklist_match = db.query(BlacklistWhitelist).filter(
        BlacklistWhitelist.entry.in_([url, url.split('/')[0]]),
        BlacklistWhitelist.list_type == "BLACKLIST"
    ).first()
    
    if blacklist_match:
        analysis_result = {
            'url': url,
            'threat_score': 100,
            'risk_level': "CRITICAL",
            'risk_color': "red",
            'category': "Blacklisted Threat Domain",
            'probability': 1.0,
            'model_breakdown': {'rule_engine': 1.0},
            'features_extracted': {'blacklisted': 1},
            'threat_intelligence': {'blacklist_status': 'FORCE_BLOCKED'},
            'explainable_ai': {
                'reasons': [{
                    'title': 'Domain Explicitly Blacklisted',
                    'description': 'Target domain matches an administrator threat blacklist entry.',
                    'risk_level': 'CRITICAL',
                    'contribution_percentage': '+100%'
                }],
                'mitre_attack': ['T1566 - Phishing'],
                'owasp_top10': ['A01:2021 - Broken Access Control'],
                'recommendations': ['Block all access to this domain immediately.']
            }
        }
    else:
        # Run ML engine workflow
        analysis_result = analyze_target_url(url, payload.html_content or "", payload.js_code or "")
        
    # Save scan to database
    new_log = ScanLog(
        target_url=url,
        threat_score=analysis_result['threat_score'],
        risk_level=analysis_result['risk_level'],
        category=analysis_result['category'],
        scan_type="URL",
        result_json=json.dumps(analysis_result)
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    analysis_result['scan_id'] = new_log.id
    return analysis_result

@router.get("/history")
def get_scan_history(limit: int = 20, db: Session = Depends(get_db)):
    logs = db.query(ScanLog).order_by(ScanLog.created_at.desc()).limit(limit).all()
    history = []
    for item in logs:
        history.append({
            'id': item.id,
            'target_url': item.target_url,
            'threat_score': item.threat_score,
            'risk_level': item.risk_level,
            'category': item.category,
            'scan_type': item.scan_type,
            'created_at': item.created_at
        })
    return history

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Optimize multiple count queries into a single group_by query
    risk_counts_query = db.query(ScanLog.risk_level, func.count(ScanLog.id)).group_by(ScanLog.risk_level).all()
    risk_counts = {level: count for level, count in risk_counts_query}
    
    total_scans = sum(risk_counts.values())
    critical_threats = risk_counts.get("CRITICAL", 0)
    high_threats = risk_counts.get("HIGH", 0)
    medium_threats = risk_counts.get("MEDIUM", 0)
    safe_scans = risk_counts.get("LOW", 0)
    
    threats_detected = critical_threats + high_threats + medium_threats
    safety_rate = 100.0 if total_scans == 0 else round((safe_scans / total_scans) * 100, 2)
    
    # Calculate today scans
    from datetime import datetime
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_scans = db.query(ScanLog).filter(ScanLog.created_at >= today_start).count()
    
    # Get top 5 dangerous categories
    cat_query = db.query(ScanLog.category, func.count(ScanLog.id))\
        .filter(ScanLog.risk_level.in_(["CRITICAL", "HIGH"]))\
        .group_by(ScanLog.category)\
        .order_by(func.count(ScanLog.id).desc())\
        .limit(5).all()
        
    top_categories = [{'category': c[0], 'count': c[1]} for c in cat_query]
    
    return {
        'total_scans': total_scans,
        'today_scans': today_scans,
        'threats_detected': threats_detected,
        'safety_rate_percentage': safety_rate,
        'avg_scan_latency_ms': 120, # Simulated
        'risk_level_distribution': {
            'CRITICAL': critical_threats,
            'HIGH': high_threats,
            'MEDIUM': medium_threats,
            'LOW': safe_scans
        },
        'top_dangerous_categories': top_categories
    }
