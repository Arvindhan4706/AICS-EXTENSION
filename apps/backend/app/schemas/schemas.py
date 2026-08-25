"""
CyberShield AI Pydantic Data Validation Schemas
"""

from pydantic import BaseModel, EmailStr, Field, validator
import re
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: Optional[str] = None
    role: Optional[str] = "User"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class URLScanRequest(BaseModel):
    url: str = Field(..., min_length=4, max_length=2048, description="Target URL or domain to scan")
    html_content: Optional[str] = ""
    js_code: Optional[str] = ""
    
    @validator('url')
    def validate_url_format(cls, v):
        # Basic sanity check for a domain, localhost, or IP structure
        if not re.search(r'(localhost|[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+|(?:\d{1,3}\.){3}\d{1,3})', v):
            raise ValueError('Invalid URL or domain format')
        return v

class EmailScanRequest(BaseModel):
    raw_eml: Optional[str] = None
    email_text: Optional[str] = None

class QRScanRequest(BaseModel):
    qr_data: str

class ChatbotRequest(BaseModel):
    query: str

class PasswordCheckRequest(BaseModel):
    password: str

class RuleAddRequest(BaseModel):
    entry: str
    entry_type: str = "DOMAIN"
    list_type: str = "BLACKLIST"
