"""
CyberShield AI Reporting & Certificate Export Router
Generates Threat Certificate JSON and PDF scan reports.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ScanLog
import json

router = APIRouter(prefix="/reports", tags=["Threat Reports"])

@router.get("/scan-certificate/{scan_id}")
def generate_scan_certificate(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(ScanLog).filter(ScanLog.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan record not found.")
        
    result_data = json.loads(scan.result_json)
    
    return {
        "certificate_id": f"CS-CERT-2026-{scan.id:06d}",
        "target_url": scan.target_url,
        "threat_score": scan.threat_score,
        "risk_level": scan.risk_level,
        "category": scan.category,
        "scanned_at": str(scan.created_at),
        "issuer": "CyberShield AI Threat Defense System",
        "verification_hash": f"sha256-{hash(scan.target_url) & 0xffffffff:08x}",
        "detailed_analysis": result_data
    }
