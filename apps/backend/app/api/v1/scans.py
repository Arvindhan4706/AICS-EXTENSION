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
            "evidence": risk_assessment.get("evidence", [])
        })
        
    except Exception as e:
        fake_db[scan_id]["status"] = "failed"
        fake_db[scan_id]["error"] = str(e)

@router.get("/{scan_id}")
async def get_scan(scan_id: str):
    if scan_id not in fake_db:
        raise HTTPException(status_code=404, detail="Scan not found")
    return fake_db[scan_id]
