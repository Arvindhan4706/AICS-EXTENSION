# CyberShield AI - User Manual, Setup & Deployment Guide

Welcome to **CyberShield AI**, an enterprise-grade AI-powered anti-phishing and cyber threat detection platform.

---

## 1. Environment Requirements
- **Python**: 3.11 or higher
- **Node.js**: v18.0.0 or higher (npm v9+)
- **Browser**: Google Chrome / Microsoft Edge (for Manifest V3 extension)

---

## 2. Installation & Quick Start

### Step 1: Install & Launch FastAPI Backend API
```bash
cd cybershield-ai/apps/backend
pip install -r requirements.txt
python main.py
```
- Server will launch at: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/api/v1/docs`

---

### Step 2: Launch Next.js Enterprise Web Dashboard
```bash
cd cybershield-ai/apps/web
npm install
npm run dev
```
- Open browser at: `http://localhost:3005`

---

### Step 3: Install Chrome Browser Extension
1. Open Google Chrome or Microsoft Edge.
2. Navigate to `chrome://extensions`.
3. Enable **Developer mode** toggle in the top-right corner.
4. Click **Load unpacked**.
5. Select the folder: `cybershield-ai/apps/extension`.
6. CyberShield AI shield icon will appear in your browser extension toolbar!

---

## 3. Features & Usage Guide

### 3.1 Real-Time URL Scanner (`/scan`)
- Paste any URL (e.g. `http://192.168.1.1/paypal-verify/login.php`).
- Click **Analyze Threat**.
- View Threat Score (0-100), Risk Level (CRITICAL, HIGH, MEDIUM, LOW), Model Probabilities, SHAP Risk Factors, and MITRE ATT&CK mappings.

### 3.2 Email EML Scanner (`/email-scan`)
- Paste raw EML headers or email content.
- Evaluates SPF, DKIM, DMARC status, spoofing flags, and extracts/scans links inside the email body.

### 3.3 QR Code Scanner (`/qr-scan`)
- Input decoded QR text or URL target to test for Quishing (QR code phishing).

### 3.4 Password Leak Checker (`/password-check`)
- Check password strength and evaluate whether it appears in public leak dumps via Have I Been Pwned API k-Anonymity privacy hashing.

### 3.5 AI Cyber Assistant (`/assistant`)
- Ask security questions to the RAG-augmented security chatbot.

### 3.6 Admin Panel & ML Retraining (`/admin`)
- Trigger automated retraining of Random Forest, XGBoost, and Decision Tree ensemble classifiers.
- Add custom domains or IP addresses to the explicit threat blacklist.

---

## 4. Academic Presentation & Review Deliverables
- **IEEE Research Paper**: Located in `docs/IEEE_Research_Paper.md`.
- **System Requirements Specification (SRS)**: Located in `docs/SRS.md`.
- **Architecture & System Design (HLD/LLD)**: Located in `docs/Architecture_HLD_LLD.md`.
