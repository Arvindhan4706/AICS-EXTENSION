"""
CyberShield AI Database Connection & Session Setup
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# We expect a Supabase Postgres URL
# We default to a local sqlite fallback for development
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./cybershield.db")

# In production (Supabase), connect_args={'check_same_thread': False} is not needed for Postgres
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
