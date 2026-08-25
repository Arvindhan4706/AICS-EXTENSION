from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid
import datetime

from app.scanner.orchestrator import ScanOrchestrator
from app.ml.feature_engine import FeatureEngine
from app.ml.ensemble import MLEnsemble
from app.ml.explainer import SHAPExplainer
from app.ml.risk_engine import RiskEngine

router = APIRouter()

# In-memory store for demonstration purposes
# In production, this would hit PostgreSQL via SQLAlchemy
fake_db = {}

class ScanRequest(BaseModel):
    url: str

@router.post("/")
async def create_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = f"SCN-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    fake_db[scan_id] = {
        "scan_id": scan_id,
        "target": {"url": request.url},
        "status": "pending",
        "timestamps": {"created_at": datetime.datetime.now().isoformat()}
    }
    
    background_tasks.add_task(process_scan, scan_id, request.url)
    
    return {"scan_id": scan_id, "status": "started"}

async def process_scan(scan_id: str, url: str):
    try:
        orchestrator = ScanOrchestrator()
        analysis_results = await orchestrator.run_scan(url)
        
        feature_engine = FeatureEngine()
        features = feature_engine.extract_features(analysis_results.get("analysis", {}))
        
        ensemble = MLEnsemble()
        prediction = ensemble.predict(features)
        
        explainer = SHAPExplainer()
        explanations = explainer.explain(features, prediction)
        
        risk_engine = RiskEngine()
        risk_assessment = risk_engine.calculate_risk(prediction, analysis_results.get("analysis", {}))
        
        # Dynamic MITRE ATT&CK & OWASP mapping based on actual evidence & features
        mitre_mappings = []
        owasp_mappings = []
        recommendations = []
        
        url_data = analysis_results.get("analysis", {}).get("url", {})
        vt_data = analysis_results.get("analysis", {}).get("virustotal", {})
        threat_score = risk_assessment.get("risk_score", 0)
        
        has_keywords = len(url_data.get("suspicious_keywords", [])) > 0
        has_ip = url_data.get("has_ip", False)
        high_entropy = url_data.get("entropy", 0) > 4.0
        multi_subdomains = url_data.get("subdomain_count", 0) > 2
        vt_flagged = vt_data.get("positives", 0) > 0
        
        if threat_score >= 50 or has_keywords or vt_flagged:
            mitre_mappings.extend(["T1566.002 - Spearphishing Link", "T1204.001 - User Execution: Malicious Link"])
            owasp_mappings.extend(["A07:2021 - Identification and Authentication Failures", "A03:2021 - Injection"])
            recommendations.extend([
                "Block target domain/URL at DNS and perimeter firewall level.",
                "Revoke and rotate any user credentials submitted to this target.",
                "Quarantine related email or SMS messages containing this link."
            ])
            
        if has_ip:
            mitre_mappings.append("T1071.001 - Web Protocols (Direct IP Access)")
            owasp_mappings.append("A05:2021 - Security Misconfiguration")
            recommendations.append("Enforce policy requiring valid Fully Qualified Domain Names (FQDN).")
            
        if high_entropy:
            mitre_mappings.append("T1027 - Obfuscated/Encoded Hostname Information")
            
        if multi_subdomains:
            mitre_mappings.append("T1583.001 - Acquire Infrastructure: Excessive Subdomains")
            
        if not mitre_mappings:
            mitre_mappings = ["M1021 - Network Intrusion Prevention (Clean Traffic)"]
            owasp_mappings = ["A00:2021 - Compliant Baseline"]
            recommendations = [
                "Target verified clean across lexical heuristic and ML models.",
                "Safe for user access under standard corporate security policy."
            ]
            
        # Deduplicate
        mitre_mappings = list(dict.fromkeys(mitre_mappings))
        owasp_mappings = list(dict.fromkeys(owasp_mappings))
        recommendations = list(dict.fromkeys(recommendations))
        
        features_dict = {
            "subdomain_count": url_data.get("subdomain_count", 0),
            "has_ip": 1 if has_ip else 0,
            "entropy": round(url_data.get("entropy", 0.0), 3),
            "keyword_count": len(url_data.get("suspicious_keywords", [])),
            "url_length": url_data.get("url_length", len(url)),
            "hostname_length": url_data.get("hostname_length", 0),
            "vt_positives": vt_data.get("positives", 0)
        }
        
        # Log to SQLite Database so Dashboard & Reports populate
        from app.core.database import SessionLocal
        from app.models.models import ScanLog
        import json
        
        db = SessionLocal()
        try:
            new_log = ScanLog(
                target_url=url,
                threat_score=risk_assessment.get("risk_score", 0),
                risk_level=risk_assessment.get("risk_level", "UNKNOWN"),
                category=risk_assessment.get("classification", "UNKNOWN"),
                scan_type="URL",
                result_json=json.dumps(analysis_results.get("analysis", {}))
            )
            db.add(new_log)
            db.commit()
        finally:
            db.close()
            
        fake_db[scan_id].update({
            "status": "completed",
            "verdict": risk_assessment,
            "analysis": analysis_results.get("analysis", {}),
            "ml": prediction,
            "explanations": explanations,
            "evidence": risk_assessment.get("evidence", []),
            "mitre_mappings": mitre_mappings,
            "owasp_mappings": owasp_mappings,
            "recommendations": recommendations,
            "features": features_dict
        })

@router.get("/{scan_id}")
async def get_scan(scan_id: str):
    if scan_id not in fake_db:
        raise HTTPException(status_code=404, detail="Scan not found")
    return fake_db[scan_id]
