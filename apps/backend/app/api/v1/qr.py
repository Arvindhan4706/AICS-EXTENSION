"""
CyberShield AI QR Code Threat Scanner API Router
(Deprecated: The UI now sends decoded QR payloads directly to the /scans/ API)
"""

from fastapi import APIRouter

router = APIRouter(prefix="/qr", tags=["QR Scanner"])

@router.post("/scan")
def scan_qr_code():
    return {"message": "Deprecated. Use /scans/ API."}
