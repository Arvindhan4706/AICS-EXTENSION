"""
CyberShield AI - Main FastAPI Web Application Server
Production REST API with CORS, Security headers, and Route Registration.
"""

from fastapi import FastAPI, Request
import sys
import os

# Add root directory to sys.path to allow absolute imports from 'apps.'
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine

# Routers
from app.api.v1 import auth, scans, scan, email, qr, threat_intel, admin, chatbot, reports

# Initialize SQLite / Postgres DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log exception here in production
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)}
    )

# Configure CORS Middleware for Next.js & Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production should restrict to allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API V1 Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(scan.router, prefix=settings.API_V1_STR)
app.include_router(scans.router, prefix=f"{settings.API_V1_STR}/scans")
app.include_router(email.router, prefix=settings.API_V1_STR)
app.include_router(qr.router, prefix=settings.API_V1_STR)
app.include_router(threat_intel.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(chatbot.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "service": "CyberShield AI Threat Detection API",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.backend.main:app", host="0.0.0.0", port=8000, reload=True)
