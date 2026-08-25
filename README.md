# CyberShield AI - AI-Powered Anti-Phishing & Cyber Threat Detection Platform

**CyberShield AI** is an enterprise-grade, startup-ready cybersecurity platform engineered to detect, evaluate, and explain complex digital threats in real-time.

---

## 🌟 Key Features

- 🛡️ **Real-Time URL Scanner**: Deep 40+ feature extraction (Lexical, DOM, SSL/TLS, DNS, JS behavior, Shannon Entropy).
- 🧠 **Multi-Model Machine Learning Ensemble**: Combines Random Forest, XGBoost, LightGBM, and Decision Trees (98.2% Accuracy, 0.980 F1-Score).
- 🔍 **Explainable AI (XAI)**: SHAP-based feature importance breakdown with human-readable explanations, MITRE ATT&CK techniques, and OWASP Top 10 mappings.
- 📧 **EML Email Scanner**: Header verification (SPF, DKIM, DMARC), spoofing detection, and embedded URL extraction.
- 📱 **QR Code Quishing Scanner**: Decodes and scans embedded QR URLs.
- 🌐 **Chrome Browser Extension (Manifest V3)**: Real-time tab risk badge indicators and malicious site warning overlay injection.
- 🔐 **Password Leak & Strength Checker**: Checks passwords against Have I Been Pwned API format using k-Anonymity privacy hashing.
- 🤖 **RAG AI Cyber Assistant**: Interactive chatbot for security guidance.
- ⚙️ **Admin & Retraining Hub**: Threat blacklist management and automated model retraining triggers.

---

## 📁 Repository Monorepo Structure

```
cybershield-ai/
├── apps/
│   ├── backend/               # FastAPI Python REST API & Security Gateway
│   ├── ml_engine/             # 40+ Feature Extractors, Ensemble Models, SHAP XAI Engine
│   ├── web/                   # Next.js 14 Enterprise UI Dashboard (Tailwind, Recharts, Lucide)
│   └── extension/             # Manifest V3 Chrome / Edge Extension
├── docs/                      # Academic & Architecture Deliverables
│   ├── SRS.md                 # System Requirement Specification
│   ├── Architecture_HLD_LLD.md# High-Level & Low-Level Design (DFD, ER, Sequence)
│   ├── IEEE_Research_Paper.md # Complete IEEE Format Academic Research Paper
│   └── User_Manual_Guide.md   # Step-by-Step Installation & Deployment Manual
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1. Launch FastAPI Backend API
```bash
cd apps/backend
pip install -r requirements.txt
python main.py
```
Open API docs at: `http://localhost:8000/api/v1/docs`

### 2. Launch Next.js Web Dashboard
```bash
cd apps/web
npm install
npm run dev
```
Open dashboard at: `http://localhost:3005`

### 3. Load Chrome Browser Extension
1. Open `chrome://extensions` in Google Chrome.
2. Enable **Developer Mode**.
3. Click **Load Unpacked** and select `apps/extension`.

---

## 📄 Academic Deliverables
- **IEEE Research Paper**: [`docs/IEEE_Research_Paper.md`](docs/IEEE_Research_Paper.md)
- **SRS Document**: [`docs/SRS.md`](docs/SRS.md)
- **Architecture (HLD/LLD)**: [`docs/Architecture_HLD_LLD.md`](docs/Architecture_HLD_LLD.md)
- **User Manual**: [`docs/User_Manual_Guide.md`](docs/User_Manual_Guide.md)
