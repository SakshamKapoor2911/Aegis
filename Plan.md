# GKE Security Agent - 1-Day Battle Plan

## 🚨 URGENT: 1-Day Execution Strategy

**Goal**: Build a Security Agent MVP that performs autonomous penetration testing on the Online Boutique microservice application, demonstrating AI-powered security scanning capabilities for the GKE Turns 10 Hackathon.

**Deadline**: September 22, 2025 @ 8:00pm EDT (TOMORROW!)  
**Strategy**: Ruthless prioritization - single FastAPI backend + Next.js frontend deployed on Cloud Run

## ⚡ RUTHLESS SIMPLIFICATIONS

### ❌ CUT IMMEDIATELY:
- **Three Microservices → One Service**: Single FastAPI backend (eliminates Go API + Pub/Sub)
- **GKE Deployment → Cloud Run**: Faster deployment, still containerized
- **All "Should Have" & "Could Have" Features**: Only MVP essentials
- **Complex Architecture**: Direct API calls instead of async messaging

---

## 🏗️ SIMPLIFIED Architecture

### Technology Stack
- **Backend**: FastAPI (Python) - API + LangGraph agent in one service
- **Frontend**: Next.js/React (minimalist dashboard)
- **Cloud Platform**: Cloud Run (containerized, faster than GKE)
- **AI Model**: Google Gemini via Vertex AI API - Required
- **Database**: Firestore (NoSQL for scan results)
- **Container Registry**: Google Artifact Registry

### Architecture Flow
```
Frontend (Next.js) → FastAPI Backend → Online Boutique (GKE - 11 microservices)
                           ↓
                    Firestore + Vertex AI
```

---

## 📁 SIMPLIFIED Project Structure

```
gke-security-agent/
├── backend/                     # Single FastAPI service
│   ├── main.py                 # FastAPI app + LangGraph agent
│   ├── scanner.py              # Security scanning logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # Next.js dashboard
│   ├── app/
│   │   ├── page.tsx           # Main dashboard
│   │   └── globals.css        # Professional dark theme
│   ├── components/
│   │   ├── ScanForm.tsx       # URL input + scan button
│   │   └── ResultsTable.tsx   # Vulnerability display
│   ├── package.json
│   └── Dockerfile
├── scripts/
│   └── deploy.sh              # Cloud Run deployment
└── README.md
```

---

## ✅ RUTHLESS Feature Prioritization

### 🚨 MUST HAVE (ONLY MVP - 1 Day)

#### 1. Target Definition & One-Click Scan
- **UI Input**: Single input box for Online Boutique URL
- **Scan Trigger**: One "Start Scan" button
- **Backend**: FastAPI endpoint that triggers scan immediately

#### 2. Core Agentic Scan (The "Wow" Factor)
- **Step 1: gRPC Service Discovery**
  - Discover all 11 microservices (frontend, cart, productcatalog, etc.)
  - Map gRPC service definitions and endpoints
  - Identify service communication patterns
- **Step 2: Essential Vulnerability Checks**
  - Missing Content-Security-Policy header
  - Missing HSTS header
  - Insecure HTTP redirects
  - gRPC service security configurations
- **Step 3: Results Storage**
  - Store findings in Firestore with severity levels

#### 3. Results Dashboard
- **Single Page**: Display scan findings in clean cards
- **Severity Colors**: Red (Critical), Orange (High), Yellow (Medium), Blue (Low)
- **Professional Dark Theme**: Security tool aesthetic

#### 4. AI Summary (Critical for Judging)
- **Gemini Integration**: Generate security summary
- **One Button**: "Generate AI Summary" button
- **Plain English**: Human-readable security assessment

### ❌ CUT EVERYTHING ELSE
- No user authentication
- No scan history
- No real-time updates
- No complex vulnerability checks
- No export functionality
- No multiple targets

---

## ⚡ 1-DAY EXECUTION PLAN

### Phase 1: Setup & Target Deployment (2-4 Hours)

#### Step 1.1: GCP Project Setup
```bash
# Commands to run:
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable container.googleapis.com
```

#### Step 1.2: GKE Cluster Creation (for Bank of Anthos)
```bash
# Create GKE Autopilot cluster (time-saver)
gcloud container clusters create-auto gke-security-agent \
    --region=us-central1 \
    --project=YOUR_PROJECT_ID
```

#### Step 1.3: Deploy Online Boutique
```bash
# Clone Online Boutique repository
git clone --depth 1 --branch v0 https://github.com/GoogleCloudPlatform/microservices-demo.git
cd microservices-demo

# Deploy to GKE
kubectl apply -f ./release/kubernetes-manifests.yaml

# Get external IP
kubectl get service frontend-external
```

#### Step 1.4: Verify Online Boutique Deployment
- Access the application via external IP
- Test basic functionality (browse products, add to cart)
- Note the 11 microservices and gRPC endpoints for security scanning

### Phase 2: FastAPI Backend Development (10-12 Hours)

#### Step 2.1: Single FastAPI Service
**Files to create:**
- `backend/main.py` (FastAPI app + LangGraph agent)
- `backend/scanner.py` (Security scanning logic)
- `backend/requirements.txt`
- `backend/Dockerfile`

**Key Features:**
- REST API endpoints for scan management
- LangGraph agent for scan orchestration
- HTTP client for API reconnaissance
- Security vulnerability detection logic
- Firestore integration for results storage
- Vertex AI integration for report generation

**API Endpoints:**
```
POST /api/scan/start           # Start new scan
GET  /api/scan/results/{id}    # Get scan results
POST /api/scan/summary/{id}    # Generate AI summary
GET  /health                   # Health check
```

**Scan Workflow:**
1. Receive scan request via API
2. Perform reconnaissance on target
3. Execute vulnerability checks
4. Store results in Firestore
5. Generate AI summary via Gemini

### Phase 3: Next.js Frontend Development (6-8 Hours)

#### Step 3.1: Minimalist Dashboard
**Files to create:**
- `frontend/app/page.tsx` (main dashboard)
- `frontend/app/globals.css` (professional dark theme)
- `frontend/components/ScanForm.tsx`
- `frontend/components/ResultsTable.tsx`
- `frontend/package.json`
- `frontend/Dockerfile`

**Key Features:**
- Target URL input form
- One-click scan initiation
- Results display with severity colors
- AI-generated summary display
- Professional dark theme (security tool aesthetic)

### Phase 4: GCP Services Configuration (1 Hour)

#### Step 4.1: Firestore Database Setup
```bash
# Enable Firestore and create database
gcloud firestore databases create --region=us-central1
```

#### Step 4.2: Vertex AI Configuration
```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

#### Step 4.3: Artifact Registry Setup
```bash
# Create container registry
gcloud artifacts repositories create gke-security-agent \
    --repository-format=docker \
    --location=us-central1
```

### Phase 5: Cloud Run Deployment (2-3 Hours)

#### Step 5.1: Build and Push Container Images
```bash
# Build FastAPI Backend
cd backend
docker build -t gcr.io/YOUR_PROJECT_ID/security-agent-backend .
docker push gcr.io/YOUR_PROJECT_ID/security-agent-backend

# Build Next.js Frontend
cd ../frontend
docker build -t gcr.io/YOUR_PROJECT_ID/security-agent-frontend .
docker push gcr.io/YOUR_PROJECT_ID/security-agent-frontend
```

#### Step 5.2: Deploy to Cloud Run
```bash
# Deploy Backend
gcloud run deploy security-agent-backend \
    --image gcr.io/YOUR_PROJECT_ID/security-agent-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated

# Deploy Frontend
gcloud run deploy security-agent-frontend \
    --image gcr.io/YOUR_PROJECT_ID/security-agent-frontend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Phase 6: Testing & Demo Recording (4-6 Hours)

#### Step 6.1: End-to-End Testing
- Test complete scan workflow
- Verify all services communicate correctly
- Test error handling and edge cases

#### Step 6.2: Demo Recording (CRITICAL)
- Record 3-minute demo video
- Show Bank of Anthos deployment
- Demonstrate security scanning
- Show AI-generated summary
- Highlight technical achievements

#### Step 6.3: Submission Preparation
- Update README.md with setup instructions
- Document API endpoints and usage
- Prepare Devpost submission
- Submit before deadline

---

## 🚀 1-Day Quick Start Commands

### Prerequisites Setup
```bash
# Install required tools
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud container clusters get-credentials gke-security-agent --region=us-central1
```

### Development Workflow
```bash
# Start local development
cd backend && python main.py
cd frontend && npm run dev

# Deploy to Cloud Run
./scripts/deploy.sh
```

### Testing Commands
```bash
# Test FastAPI Backend
curl -X POST http://BACKEND_URL/api/scan/start \
  -H "Content-Type: application/json" \
  -d '{"target_url": "http://BANK_OF_ANTHOS_IP"}'

# Check scan results
curl http://BACKEND_URL/api/scan/results/SCAN_ID
```

---

## 📊 1-Day Success Metrics

### Technical Metrics
- [ ] Bank of Anthos deployed on GKE
- [ ] FastAPI backend deployed on Cloud Run
- [ ] Next.js frontend deployed on Cloud Run
- [ ] Complete scan workflow functional
- [ ] AI-generated reports working
- [ ] Professional dark theme UI

### Hackathon Judging Criteria
- [ ] **Innovation**: AI-powered autonomous security scanning
- [ ] **Technical Excellence**: Clean architecture, proper GKE usage
- [ ] **Impact**: Demonstrates real security value
- [ ] **Presentation**: Professional demo and documentation

### Demo Checklist (CRITICAL)
- [ ] 3-minute demo video recorded
- [ ] Bank of Anthos scanning demonstrated
- [ ] AI summary generation shown
- [ ] Professional UI showcased
- [ ] Devpost submission completed

---

## 🆘 1-Day Troubleshooting Guide

### Common Issues
1. **GKE Cluster Issues**: Use Autopilot mode for easier management
2. **Container Registry**: Ensure proper authentication and permissions
3. **Cloud Run**: Check service account permissions
4. **Firestore**: Verify database rules and access permissions
5. **Vertex AI**: Ensure API is enabled and properly configured

### Emergency Fallbacks
- If GKE deployment fails, use Cloud Run for everything
- If Firestore fails, use local file storage temporarily
- If Vertex AI fails, use hardcoded summary text
- If Cloud Run fails, use local development and screen recording

---

## 📝 1-Day Execution Notes

### Time Management (24 Hours)
- **Hours 1-4**: Setup GCP, deploy Bank of Anthos
- **Hours 5-16**: Build FastAPI backend + Next.js frontend
- **Hours 17-19**: Deploy to Cloud Run
- **Hours 20-24**: Test, record demo, submit

### Risk Mitigation
- Start with simplest possible implementation
- Test each component individually before integration
- Keep detailed logs for debugging
- Have backup plans for critical components
- **CRITICAL**: Record demo video early in case of last-minute issues

### Professional UI Design Prompt
Use this prompt with AI to generate professional security tool UI:
```
Act as a senior UI/UX designer at a top-tier cybersecurity firm. Create a professional, dark-mode dashboard for "Aegis Agent" - an AI-powered autonomous penetration testing tool.

Requirements:
- Dark mode mandatory (#0D1117 background)
- Primary accent: Electric blue (#007BFF) or secure green (#28A745)
- Severity colors: Critical red (#DC3545), High orange (#FFC107), Medium yellow (#FDDA0D), Low blue (#17A2B8)
- Clean three-section layout: navigation, command center, results pane
- Vulnerability cards with severity tags
- "Generate AI Summary" button prominently displayed
- Modern sans-serif font (Inter/Lexend/Manrope)
- Professional, trustworthy aesthetic
```

### Future Enhancements (Post-Hackathon)
- RLHF feedback loop implementation
- Advanced vulnerability detection
- CI/CD pipeline integration
- Enterprise features and scaling
- Custom AI model training

---

**REMEMBER**: The goal is to create a compelling, working demonstration of autonomous security scanning that showcases your technical skills and vision for the future of AI-powered security testing. **DEMO VIDEO IS CRITICAL FOR WINNING.**
