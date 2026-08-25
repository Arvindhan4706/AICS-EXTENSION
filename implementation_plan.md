# Implementation Plan - CyberShield AI (AI-Powered Anti-Phishing & Cyber Threat Detection Platform)

CyberShield AI is an enterprise-grade, startup-ready cybersecurity platform designed to detect, analyze, and explain complex cyber threats including phishing URLs, fake login/banking portals, typosquatting domains, homograph attacks, QR scams, email phishing (.eml), and credential harvesting pages.

The system combines **multi-model Machine Learning ensembles** (Random Forest, XGBoost, LightGBM, Neural Networks), **real-time 40+ feature extraction** (Lexical, DNS, SSL/TLS, HTML/DOM complexity, JavaScript behavior, Visual features), **Threat Intelligence API aggregation** (VirusTotal, PhishTank, AbuseIPDB, OpenPhish), **Explainable AI (SHAP/LIME feature importance)**, a **Chrome Browser Extension**, and a modern **CrowdStrike/Cloudflare-inspired Next.js Analytics Dashboard**.

---

## User Review Required

> [!IMPORTANT]
> **Academic & Startup Dual Target**: The architecture is designed to satisfy both rigorous Final Year IEEE Computer Science / AI & Data Science requirements and real-world startup production standards.

> [!NOTE]
> **Tech Stack & Modular Architecture**:
> - **Frontend**: Next.js 14 (App Router), React 18, TypeScript, TailwindCSS, Framer Motion, Recharts, Lucide Icons, Redux Toolkit.
> - **Backend API**: FastAPI (Python 3.11), Pydantic v2, SQLAlchemy 2.0, AsyncPG / SQLite (dev) / PostgreSQL (prod), JWT Auth & RBAC.
> - **AI/ML Microservice**: Python ML Engine with Scikit-learn, XGBoost, LightGBM, PyTorch, SHAP explainability, OpenCV, tesseract OCR, spaCy/NLTK.
> - **Browser Extension**: Manifest V3 Chrome/Edge Extension for real-time tab monitoring, page safety scoring, and instant blocking.
> - **MLOps & Infra**: Docker, Docker Compose, MLflow model tracking structure, Prometheus/Grafana metrics stubs.

---

## Architecture Overview

```
                               ┌───────────────────────────────────────────────┐
                               │           Chrome Browser Extension            │
                               │  (Manifest V3 - Real-time Page Check & Sync)  │
                               └──────────────────────┬────────────────────────┘
                                                      │ HTTPS / REST API
                                                      ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       CyberShield AI Frontend                                          │
│                          (Next.js 14 + TailwindCSS + Recharts + Framer Motion)                          │
│                                                                                                        │
│   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐   ┌──────────────────┐   │
│   │ Analytics Dashboard │   │  Live URL Scanner   │   │ Email / EML Scanner │   │  QR Code Scanner │   │
│   └─────────────────────┘   └─────────────────────┘   └─────────────────────┘   └──────────────────┘   │
│   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐   ┌──────────────────┐   │
│   │ Explainable AI View │   │ Threat Intel Feed   │   │  Admin & Retraining │   │ RAG Cyber Chat   │   │
│   └─────────────────────┘   └─────────────────────┘   └─────────────────────┘   └──────────────────┘   │
└──────────────────────────────────────────────────┬─────────────────────────────────────────────────────┘
                                                   │ HTTPS / REST API / JWT
                                                   ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      CyberShield FastAPI Backend                                       │
│                                                                                                        │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────┐ │
│  │ Auth & RBAC (JWT/OAuth) │  │ Scan Orchestrator Engine│  │ Threat Intel Aggregator │  │ Admin / Logs│ │
│  └─────────────────────────┘  └────────────┬────────────┘  └─────────────────────────┘  └─────────────┘ │
└────────────────────────────────────────────┼───────────────────────────────────────────────────────────┘
                                             │ Inter-Process / Microservice Call
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      CyberShield AI/ML Engine                                          │
│                                                                                                        │
│  ┌──────────────────────────────────┐  ┌─────────────────────────────────┐  ┌──────────────────────────┐  │
│  │     40+ Feature Extractor        │  │     ML Model Ensemble           │  │   Explainable AI Engine  │  │
│  │  (URL, HTML, DNS, SSL, JS, NLP)  │  │ (Scikit-Learn, XGBoost, LightGBM│  │ (SHAP Feature Importance │  │
│  │                                  │  │  PyTorch Neural Network)        │  │  & Reason Generator)     │  │
│  └──────────────────────────────────┘  └─────────────────────────────────┘  └──────────────────────────┘  │
└────────────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                                     │
                                                     ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       Database & Storage Layer                                         │
│                      (PostgreSQL / SQLite, Redis Cache, File Storage for EML/PDF)                       │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Proposed Changes & Components

### 1. Monorepo Directory Structure
We will establish a modular directory structure:
```
cybershield-ai/
├── apps/
│   ├── backend/               # FastAPI Application
│   │   ├── app/
│   │   │   ├── api/v1/        # API Endpoints (auth, scan, email, qr, admin, threat_intel, chatbot, reports)
│   │   │   ├── core/          # Security, Config, JWT, Rate Limiter, Database setup
│   │   │   ├── models/        # SQLAlchemy Models (User, Scan, ThreatLog, ModelMetric, Blacklist)
│   │   │   ├── schemas/       # Pydantic Schemas
│   │   │   └── services/      # Business logic services
│   │   ├── requirements.txt
│   │   └── main.py
│   ├── ml_engine/             # Machine Learning & AI Detection Microservice
│   │   ├── feature_extraction/# 40+ Feature extractors (url, html, dns_ssl, js_dom, visual)
│   │   ├── models/            # Trained models & Ensemble logic (Random Forest, XGBoost, LightGBM)
│   │   ├── explainability/    # SHAP explainer & human-readable reason generator
│   │   ├── dataset/           # Synthetic/Real dataset generator & sample dataset
│   │   ├── train.py           # Model training pipeline
│   │   └── predict.py         # Prediction & SHAP engine interface
│   ├── web/                   # Next.js 14 App Router Frontend
│   │   ├── src/
│   │   │   ├── app/           # Routes: dashboard, scan, email, qr, threat-feed, admin, assistant, reports, login
│   │   │   ├── components/    # Reusable UI (Navbar, Sidebar, ThreatCard, StatBox, RiskBadge, Graphs, SHAPChart)
│   │   │   ├── lib/           # API Client, Auth helper, utils
│   │   │   └── types/         # TypeScript definitions
│   │   ├── package.json
│   │   └── tailwind.config.js
│   └── extension/             # Manifest V3 Chrome Extension
│       ├── manifest.json
│       ├── background.js
│       ├── content.js
│       ├── popup.html
│       ├── popup.js
│       └── styles.css
├── docs/                      # Documentation & Academic Deliverables
│   ├── SRS.md                 # System Requirement Specification
│   ├── Architecture_HLD_LLD.md# High-Level & Low-Level Design Document
│   ├── IEEE_Research_Paper.md # Complete IEEE Format Research Paper
│   └── User_Manual_Guide.md   # Setup, Run, and Deployment Guide
├── docker-compose.yml
└── README.md
```

---

### 2. Feature Extraction Engine (40+ Cyber Threat Indicators)
The extraction engine computes features in real-time across multiple threat categories:
1. **URL Lexical Features**: Length, dot count, `@` count, hyphen count, IP in URL, subdirectory depth, shortening service usage, sensitive keywords (`login`, `bank`, `verify`, `secure`, `update`, `paypal`), homograph/Unicode check, entropy score.
2. **Domain & Network Features**: Typosquatting distance, domain age (WHOIS), DNS record presence (A, MX, NS, TXT), TLD risk rating.
3. **SSL/TLS Features**: Valid certificate presence, self-signed detection, issuer risk, expiry timeframe.
4. **HTML & DOM Complexity**: Form action targets, external form submission, hidden inputs, iframe count, suspicious script tag count, popup scripts, password field presence, external favicon source.
5. **JavaScript & Behavior**: Obfuscation score, eval() usage, canvas fingerprinting, localStorage/WebRTC/clipboard access indicators, event listener complexity.
6. **Email & QR Features**: SPF/DKIM/DMARC status indicators, link count, attachment risk rating, embedded QR URL extractor.

---

### 3. AI Detection & Explainable AI (XAI) Engine
- **Ensemble Architecture**: Combines predictions from:
  - **Random Forest Classifier** (High stability, non-linear feature splits)
  - **XGBoost Classifier** (Gradient boosting for high precision)
  - **LightGBM Classifier** (Fast, leaf-wise boosting for real-time throughput)
  - **Neural Network / Rule Fallback** (Deep pattern detection)
- **Threat Score Algorithm**: Scaled 0–100 threat score combining ML probabilities, Threat Intel hits (VirusTotal/PhishTank/AbuseIPDB), and hard safety rule triggers.
- **Explainability Engine (SHAP)**: Calculates contribution weights for each feature. Translates raw SHAP values into user-friendly explanations (e.g., *"High Risk: URL contains IP address instead of domain name (+24% risk)", "Domain registered 2 days ago (+18% risk)", "Forms post to unverified external origin (+30% risk)"*).

---

### 4. Enterprise Frontend UI (Next.js 14 + TailwindCSS + Recharts)
Designed with a sleek, dark-mode cybersecurity visual hierarchy (inspired by Cloudflare Radar, CrowdStrike, Stripe Dashboard):
- **Hero & Command Center**: Real-time URL Quick-Scan bar with instant live analysis.
- **Analytics Dashboard**: Threat Score Gauge, Risk Level breakdown, Total vs Today Scans, Threat Category Heatmaps, Geo/Domain risk distribution, Live Activity Feed.
- **Detailed Threat Inspector**: Breakdown of URL features, SHAP contribution bar chart, Threat Intel feeds breakdown, MITRE ATT&CK & OWASP mapping, Actionable Mitigations.
- **Specialized Scanners**:
  - **EML Email Threat Scanner**: Upload or paste email source for SPF/DKIM validation, malicious link extraction, and header analysis.
  - **QR Code Threat Scanner**: Upload or camera-scan QR codes to safely preview and analyze decoded target URLs.
  - **AI Cyber Assistant (RAG Chatbot)**: Interactive security advisor for users to ask security questions, analyze suspicious snippets, or request threat advice.
  - **Password Leak & Strength Checker**: Checks passwords against Have I Been Pwned API format and local entropy calculation.
- **Admin Control & Retraining Hub**: User management, blacklist/whitelist editor, custom dataset uploader, model accuracy metrics, ML model retraining trigger.

---

### 5. Manifest V3 Chrome Browser Extension
- **Real-Time Active Tab Monitoring**: Inspects active tab URLs instantly.
- **Threat Badge & Overlay**: Shows Green (Safe), Yellow (Suspicious), or Red (High Risk) badge icon in browser toolbar.
- **Automated Warning Banner**: Injectable content script overlay on malicious pages preventing user credential input.
- **Dashboard Sync**: One-click sync with CyberShield backend account to record threats and submit user reports.

---

### 6. Academic Deliverables & Comprehensive Documentation
- **`SRS.md`**: Complete Software Requirements Specification (Functional, Non-Functional, External Interfaces, System Matrix).
- **`Architecture_HLD_LLD.md`**: Detailed System Diagrams (System Context, Sequence Diagram, DFD Level 0/1, ER Diagram, Class Diagram, Use Case Matrix).
- **`IEEE_Research_Paper.md`**: Complete 6-page IEEE format academic research paper titled *"CyberShield AI: A Multi-Modal Ensemble Learning and Explainable AI Architecture for Real-Time Phishing and Cyber Threat Detection"*.
- **`User_Manual_Guide.md`**: Step-by-step installation, dataset training, API reference, deployment, and testing instructions.

---

## Verification Plan

### Automated & Unit Verification
- Backend FastAPI endpoint tests using `pytest` and HTTP test client.
- ML Feature Extraction unit test suite verifying feature extraction against known safe (e.g. `google.com`) and phishing URLs.
- Dataset generation and ML model training accuracy validation (>95% F1-Score target).
- Pydantic schema validation tests for API request/response payloads.

### Manual & Interactive Verification
- Launch Next.js dev server (`npm run dev`) and test interactive scan flows, charts, EML upload, QR scanner, SHAP explainability view, and dark mode UI.
- Verify browser extension loading via Chrome `chrome://extensions` developer mode.
- Verify end-to-end flow: User pastes phishing URL -> Features Extracted -> ML Ensemble Predicts -> SHAP Explainer Generates Reasons -> Dashboard Displays Rich Results -> Stored in Postgres/SQLite DB.
