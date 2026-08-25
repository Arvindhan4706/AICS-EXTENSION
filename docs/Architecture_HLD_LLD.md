# High-Level & Low-Level Architecture Design (HLD & LLD)

## 1. High-Level Architecture (HLD)

### 1.1 System Context Diagram
```
┌───────────────────────────┐          ┌────────────────────────────┐
│  Chrome Extension (MV3)   │          │  Next.js Enterprise Web UI │
└──────────────┬────────────┘          └─────────────┬──────────────┘
               │                                     │
               │ REST API / HTTPS                    │ REST API / HTTPS
               ▼                                     ▼
┌───────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend Gateway                        │
│         (Auth, Security Middleware, API V1 Routers, DB ORM)       │
└──────────────────────────────────┬────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────┐
│                    Python AI & ML Engine Service                  │
│                                                                   │
│   ┌──────────────────────────┐     ┌──────────────────────────┐   │
│   │ 40+ Feature Extractors   │ ──► │  ML Model Ensemble       │   │
│   │ (Lexical, DOM, SSL, JS)  │     │ (RF + XGBoost + LightGBM)│   │
│   └──────────────────────────┘     └────────────┬─────────────┘   │
│                                                 │                 │
│                                                 ▼                 │
│                                    ┌──────────────────────────┐   │
│                                    │  Explainable AI (SHAP)   │   │
│                                    └──────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 2. Low-Level Architecture (LLD)

### 2.1 Sequence Diagram: URL Threat Scanning Flow
```
User / Extension        Next.js / Popup      FastAPI Gateway        ML Engine          Database
       │                       │                    │                   │                  │
       │─── Paste URL ────────►│                    │                   │                  │
       │                       │─── POST /scan/url─►│                   │                  │
       │                       │                    │─── Extract Feats─►│                  │
       │                       │                    │    (40+ Lexical/  │                  │
       │                       │                    │     DOM indicators)                  │
       │                       │                    │                   │                  │
       │                       │                    │─── Inference ────►│                  │
       │                       │                    │    (Ensemble RF/  │                  │
       │                       │                    │     XGB/LGBM)     │                  │
       │                       │                    │                   │                  │
       │                       │                    │◄── Score & SHAP ──│                  │
       │                       │                    │                   │                  │
       │                       │                    │─── Save Log ────────────────────────►│
       │                       │◄── JSON Report ────│                                      │
       │◄── Render Dashboard ──│
```

---

### 2.2 Entity-Relationship (ER) Diagram
```
┌─────────────────────────┐             ┌─────────────────────────┐
│          Users          │             │        ScanLogs         │
├─────────────────────────┤             ├─────────────────────────┤
│ id (PK)                 │1           *│ id (PK)                 │
│ email (UQ)              ├────────────►│ user_id (FK)            │
│ hashed_password         │             │ target_url              │
│ role                    │             │ threat_score            │
│ created_at              │             │ risk_level              │
└─────────────────────────┘             │ category                │
                                        │ result_json             │
                                        │ created_at              │
                                        └─────────────────────────┘

┌─────────────────────────┐             ┌─────────────────────────┐
│     ThreatFeedItems     │             │   BlacklistWhitelist    │
├─────────────────────────┤             ├─────────────────────────┤
│ id (PK)                 │             │ id (PK)                 │
│ domain_or_url           │             │ entry                   │
│ threat_type             │             │ entry_type              │
│ confidence_score        │             │ list_type               │
│ status                  │             │ added_by                │
└─────────────────────────┘             └─────────────────────────┘
```

---

### 2.3 Data Flow Diagram (DFD) Level 0 & Level 1

#### Level 0 (Context Diagram)
- **External Entities**: User, Security Analyst, Chrome Browser.
- **System**: CyberShield AI Platform.
- **Data Flows**: Input Target URL / EML / QR -> Threat Score, SHAP Reasons, Certificate Output.

#### Level 1 DFD
1. **Process 1.0**: Feature Extraction Subsystem (Extracts Lexical, DOM, SSL, DNS features).
2. **Process 2.0**: Ensemble Prediction Subsystem (Computes RF + XGBoost + LightGBM weighted threat probabilities).
3. **Process 3.0**: XAI Subsystem (Generates SHAP feature attributions and human readable reason cards).
4. **Process 4.0**: Database Logging & Certificate Generator.
