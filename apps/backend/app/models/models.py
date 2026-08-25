"""
CyberShield AI SQLAlchemy Database Schema
Defines User, Scan, Analysis and Threat models.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="User")  # User, Analyst, Admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    scans = relationship("Scan", back_populates="user")

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    target_url = Column(String, index=True, nullable=False)
    
    # Verdict
    classification = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=True)
    risk_level = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="scans")
    url_analysis = relationship("URLAnalysis", back_populates="scan", uselist=False)
    domain_analysis = relationship("DomainAnalysis", back_populates="scan", uselist=False)

class URLAnalysis(Base):
    __tablename__ = "url_analysis"
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    data_json = Column(Text, nullable=False)
    
    scan = relationship("Scan", back_populates="url_analysis")

class DomainAnalysis(Base):
    __tablename__ = "domain_analysis"
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    data_json = Column(Text, nullable=False)
    
    scan = relationship("Scan", back_populates="domain_analysis")

class ThreatFeedItem(Base):
    __tablename__ = "threat_feed_items"

    id = Column(Integer, primary_key=True, index=True)
    domain_or_url = Column(String, index=True, nullable=False)
    threat_type = Column(String, nullable=False)
    confidence_score = Column(Float, default=0.95)
    source = Column(String, default="CyberShield Sentinel Engine")
    status = Column(String, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BlacklistWhitelist(Base):
    __tablename__ = "blacklist_whitelist"
    id = Column(Integer, primary_key=True, index=True)
    entry = Column(String, index=True, nullable=False)
    entry_type = Column(String, nullable=False)
    list_type = Column(String, nullable=False)
    added_by = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ScanLog(Base):
    __tablename__ = "scan_logs"
    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, index=True, nullable=True)
    threat_score = Column(Integer, nullable=True)
    risk_level = Column(String, nullable=True)
    category = Column(String, nullable=True)
    scan_type = Column(String, nullable=True)
    result_json = Column(Text, nullable=True)
    scan_data = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
