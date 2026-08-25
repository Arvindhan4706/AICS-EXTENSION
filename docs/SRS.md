# Software Requirements Specification (SRS) - CyberShield AI

## 1. Introduction

### 1.1 Purpose
This document defines the Software Requirements Specification (SRS) for **CyberShield AI**, an enterprise-grade AI-powered cyber threat detection and explainability platform. CyberShield AI detects phishing URLs, credential harvesting portals, fake banking/crypto websites, homograph attacks, typosquatting domains, quishing (QR phishing), and email phishing (.eml) in real-time using multi-model Machine Learning ensembles and Explainable AI (XAI).

### 1.2 Scope
CyberShield AI encompasses:
- **FastAPI REST Service**: Backend microservice for authentication, scan orchestration, threat intelligence feed aggregation, and rule enforcement.
- **Python AI/ML Microservice**: Multi-model ensemble (Random Forest, XGBoost, LightGBM) extracting 40+ high-dimensional lexical, DOM, DNS, SSL, JS behavior, and visual features.
- **Explainable AI (XAI) Engine**: SHAP-based feature attribution engine mapping feature weights to human-readable explanations, MITRE ATT&CK techniques, and OWASP Top 10 categories.
- **Next.js Enterprise Web Dashboard**: Modern CrowdStrike/Cloudflare-inspired analytics UI for monitoring threat metrics, deep scans, EML email scans, QR scans, and RAG assistant queries.
- **Chrome Manifest V3 Extension**: Real-time browser tab monitor displaying threat badges and blocking credential entry on malicious portals.

---

## 2. Overall Description

### 2.1 User Classes and Characteristics
1. **End User / Browser User**: Submits URLs, uploads EML/QR files, browses with Chrome extension active.
2. **Security Analyst**: Inspects SHAP feature weights, reviews threat intelligence feed, generates PDF certificates.
3. **System Administrator**: Configures blacklist/whitelist rules, manages users, triggers ML model retraining pipelines.

### 2.2 Functional Requirements

| Requirement ID | Module | Description | Priority |
|---|---|---|---|
| FR-01 | Auth | User registration, login, JWT token issuance, and Role-Based Access Control (RBAC). | HIGH |
| FR-02 | Feature Extraction | Extract 40+ lexical, HTML/DOM, DNS, SSL/TLS, JS behavior, and entropy features in <150ms. | HIGH |
| FR-03 | ML Ensemble | Predict threat score (0-100) using Random Forest, XGBoost, and LightGBM weighted voting. | HIGH |
| FR-04 | XAI Engine | Generate top 5 human-readable risk reasons, MITRE ATT&CK mappings, and OWASP categories. | HIGH |
| FR-05 | EML Email Scan | Parse raw EML headers for SPF, DKIM, DMARC, spoofing, and scan embedded hyper-links. | MEDIUM |
| FR-06 | QR Code Scan | Decode QR payload URLs and analyze quishing risk in real-time. | MEDIUM |
| FR-07 | Threat Intelligence | Aggregate live feeds from VirusTotal, OpenPhish, PhishTank, and AbuseIPDB. | MEDIUM |
| FR-08 | Chrome Extension | Manifest V3 background tab scanning with real-time badge updates and warning overlay injection. | HIGH |
| FR-09 | Admin & Retraining | Add explicit domain blacklists/whitelists and trigger automated ML model re-fitting. | MEDIUM |
| FR-10 | RAG AI Assistant | Interactive security chatbot for query resolution and password breach checks. | LOW |

---

## 3. Non-Functional Requirements

### 3.1 Performance Requirements
- **Scan Latency**: URL feature extraction and ensemble inference completed within <200ms.
- **Accuracy**: Ensemble model achieves >97.5% F1-score on benchmark phishing datasets.

### 3.2 Security & Compliance Requirements
- **HTTPS & TLS**: All inter-service and extension REST communications encrypted.
- **Password Hashing**: Passwords stored using bcrypt with high work factor.
- **JWT Authentication**: Tokens expire after set duration and use HS256 / RS256 cryptographic signatures.
- **Input Sanitization**: Strict input validation against XSS, SQL injection, and command injection.

### 3.3 Reliability & Availability
- **High Availability**: Graceful fallbacks if external Threat Intel APIs fail.
- **Offline ML Execution**: Local ensemble model inference functions without third-party cloud dependence.
