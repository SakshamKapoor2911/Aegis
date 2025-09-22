# Quick Setup Guide - GKE Security Agent

## 🚀 Fast Setup for Hackathon

### Step 1: Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### Step 2: Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:PROJECT_ID="your-project-id"
$env:GEMINI_API_KEY="your-gemini-api-key"
```

**Windows (Command Prompt):**
```cmd
set PROJECT_ID=your-project-id
set GEMINI_API_KEY=your-gemini-api-key
```

**Linux/Mac:**
```bash
export PROJECT_ID=your-project-id
export GEMINI_API_KEY=your-gemini-api-key
```

### Step 3: Deploy Online Boutique to GKE

```bash
# Run the setup script
./scripts/setup-gcp.sh
```

This will:
- Create GKE cluster
- Deploy Online Boutique (11 microservices)
- Give you the external IP

### Step 4: Deploy Security Agent

```bash
# Deploy to Cloud Run
./scripts/deploy.sh
```

This will:
- Build and deploy FastAPI backend
- Build and deploy Next.js frontend
- Give you the frontend URL

### Step 5: Test the System

1. **Get Online Boutique URL**: Use the external IP from Step 3
2. **Open Security Agent**: Use the frontend URL from Step 4
3. **Start Scan**: Enter Online Boutique URL and click "Start Security Scan"
4. **View Results**: See vulnerabilities and generate AI summary

## 🔧 Local Development

### Option 1: Run Everything Locally

```bash
# Copy environment template
cp backend/.env.example backend/.env

# Edit backend/.env and add your GEMINI_API_KEY
# Then run:
./scripts/run-local.sh
```

### Option 2: Run Services Individually

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📱 URLs

- **Frontend**: http://localhost:3000 (local) or Cloud Run URL
- **Backend**: http://localhost:8000 (local) or Cloud Run URL
- **API Docs**: http://localhost:8000/docs (local) or Cloud Run URL/docs

## 🎯 What to Demo

1. **Show Online Boutique**: Browse products, add to cart
2. **Start Security Scan**: Enter Online Boutique URL
3. **Show Real-time Status**: "Scanning in Progress"
4. **Show Results**: Vulnerability cards with severity colors
5. **Generate AI Summary**: Click "Generate AI Summary" button
6. **Show Professional UI**: Dark theme, security tool aesthetic

## 🚨 Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**: Set the environment variable
2. **"External IP not ready"**: Wait 5-10 minutes for GKE load balancer
3. **"Scan fails"**: Check if Online Boutique is accessible
4. **"Deployment fails"**: Check Cloud Run quotas and permissions

### Debug Commands

```bash
# Check Online Boutique
kubectl get pods
kubectl get services

# Check Cloud Run
gcloud run services list

# View logs
gcloud run services logs read security-agent-backend
```

## ⚡ Quick Commands

```bash
# Get Online Boutique IP
kubectl get service frontend-external

# Get Security Agent URLs
gcloud run services describe security-agent-frontend --format="value(status.url)"
gcloud run services describe security-agent-backend --format="value(status.url)"
```

---

**Ready to win the hackathon! 🏆**
