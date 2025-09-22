from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import asyncio
import uuid
from datetime import datetime
import json
import os
from dotenv import load_dotenv

from google.cloud import firestore
import google.generativeai as genai

from scanner import OnlineBoutiqueScanner, Vulnerability, Severity

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="GKE Security Agent", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firestore
try:
    # Try multiple possible locations for the service account key
    possible_keys = [
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        '/c/Users/Saksham Kapoor/Downloads/gke-turns-10-472809-54676967bf7d.json',
        'firestore-key.json',
        '../firestore-key.json'
    ]
    
    key_file_path = None
    for key_path in possible_keys:
        if key_path and os.path.exists(key_path):
            key_file_path = key_path
            break
    
    if key_file_path:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file_path
        db = firestore.Client()
        print(f"✅ Firestore client initialized with key: {key_file_path}")
    else:
        print("❌ Service account key file not found in any of these locations:")
        for key_path in possible_keys:
            if key_path:
                print(f"   - {key_path}")
        print("💡 Run './scripts/copy-service-account.sh' to copy the key to the backend directory")
        db = None
except Exception as e:
    print(f"❌ Warning: Could not initialize Firestore: {e}")
    print("💡 Make sure the Firestore database exists: gcloud firestore databases create --region=us-central1")
    db = None

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# In-memory storage for scan results (in production, use Firestore)
scan_results: Dict[str, Dict[str, Any]] = {}

class ScanRequest(BaseModel):
    target_url: str

class ScanResponse(BaseModel):
    scan_id: str
    status: str
    message: str

class ScanResult(BaseModel):
    scan_id: str
    status: str
    findings: List[Dict[str, Any]]
    summary: Dict[str, Any]
    timestamp: str

class AISummaryRequest(BaseModel):
    scan_id: str

class AISummaryResponse(BaseModel):
    summary: str
    generated_at: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "GKE Security Agent"}

@app.get("/api/firestore/test")
async def test_firestore():
    """Test Firestore connectivity"""
    if not db:
        return {"status": "error", "message": "Firestore not initialized"}
    
    try:
        # Test write
        doc_ref = db.collection("test_collection").document("test_doc")
        doc_ref.set({"message": "Hello Firestore!", "timestamp": datetime.now().isoformat()})
        
        # Test read
        doc = doc_ref.get()
        if doc.exists:
            return {
                "status": "success", 
                "message": "Firestore is working!",
                "data": doc.to_dict()
            }
        else:
            return {"status": "error", "message": "Document not found after write"}
    except Exception as e:
        return {"status": "error", "message": f"Firestore error: {str(e)}"}

@app.get("/api/firestore/scans")
async def get_firestore_scans():
    """Get all scans from Firestore"""
    if not db:
        return {"status": "error", "message": "Firestore not initialized"}
    
    try:
        scans_ref = db.collection('scans')
        docs = scans_ref.stream()
        
        scans = []
        for doc in docs:
            scan_data = doc.to_dict()
            scan_data['id'] = doc.id
            scans.append(scan_data)
        
        return {
            "status": "success",
            "scans": scans,
            "count": len(scans)
        }
    except Exception as e:
        return {"status": "error", "message": f"Error reading from Firestore: {str(e)}"}

@app.post("/api/scan/start", response_model=ScanResponse)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """Start a new security scan"""
    scan_id = str(uuid.uuid4())
    
    # Initialize scan result
    scan_results[scan_id] = {
        "scan_id": scan_id,
        "status": "running",
        "target_url": request.target_url,
        "findings": [],
        "summary": {},
        "timestamp": datetime.now().isoformat(),
        "ai_summary": None
    }
    
    # Start background scan
    background_tasks.add_task(run_security_scan, scan_id, request.target_url)
    
    return ScanResponse(
        scan_id=scan_id,
        status="started",
        message=f"Security scan started for {request.target_url}"
    )

async def run_security_scan(scan_id: str, target_url: str):
    """Run the security scan in background"""
    try:
        print(f"Starting scan {scan_id} for {target_url}")
        
        # Initialize scanner
        scanner = OnlineBoutiqueScanner(target_url)
        
        # Run scan
        findings = await scanner.scan()
        
        # Convert findings to dict format
        findings_dict = []
        for finding in findings:
            findings_dict.append({
                "id": finding.id,
                "title": finding.title,
                "description": finding.description,
                "severity": finding.severity.value,
                "affected_endpoint": finding.affected_endpoint,
                "recommendation": finding.recommendation,
                "cwe_id": finding.cwe_id
            })
        
        # Get scan summary
        try:
            summary = scanner.get_scan_summary()
        except Exception as e:
            print(f"Error getting scan summary: {e}")
            summary = {
                "total_findings": len(findings_dict),
                "severity_breakdown": {"Critical": 0, "High": 0, "Medium": 0, "Low": 0},
                "scan_target": target_url,
                "scan_timestamp": datetime.now().isoformat()
            }
        
        # Update scan results
        scan_results[scan_id].update({
            "status": "completed",
            "findings": findings_dict,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        })
        
        # Store in Firestore
        if db:
            try:
                doc_ref = db.collection('scans').document(scan_id)
                doc_ref.set(scan_results[scan_id])
                print(f"✅ Scan results stored in Firestore: {scan_id}")
            except Exception as e:
                print(f"❌ Error storing in Firestore: {e}")
                print("💡 Tip: Run 'gcloud firestore databases create --region=us-central1' to create the database")
        else:
            print("⚠️ Firestore not available - results stored in memory only")
        
        # Save results to log file
        try:
            import json
            log_data = {
                "scan_id": scan_id,
                "timestamp": datetime.now().isoformat(),
                "target_url": target_url,
                "status": "completed",
                "findings": findings_dict,
                "summary": summary
            }
            
            with open(f"scan_results_{scan_id}.json", "w") as f:
                json.dump(log_data, f, indent=2)
            
            print(f"Scan results saved to: scan_results_{scan_id}.json")
        except Exception as e:
            print(f"Error saving to log file: {e}")
        
        print(f"Scan {scan_id} completed with {len(findings)} findings")
        
    except Exception as e:
        print(f"Error in scan {scan_id}: {e}")
        scan_results[scan_id].update({
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })

@app.get("/api/scan/results/{scan_id}", response_model=ScanResult)
async def get_scan_results(scan_id: str):
    """Get scan results by scan ID"""
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    result = scan_results[scan_id]
    
    return ScanResult(
        scan_id=result["scan_id"],
        status=result["status"],
        findings=result["findings"],
        summary=result["summary"],
        timestamp=result["timestamp"]
    )

@app.post("/api/scan/summary/{scan_id}", response_model=AISummaryResponse)
async def generate_ai_summary(scan_id: str):
    """Generate AI summary for scan results"""
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    result = scan_results[scan_id]
    
    if result["status"] != "completed":
        raise HTTPException(status_code=400, detail="Scan not completed yet")
    
    try:
        # Prepare findings for AI analysis
        findings_text = ""
        for finding in result["findings"]:
            findings_text += f"- {finding['severity']}: {finding['title']} ({finding['affected_endpoint']})\n"
        
        # Create prompt for AI
        prompt = f"""
        As a cybersecurity expert, analyze the following security scan results for the Online Boutique microservices application:

        Target: {result['target_url']}
        Total Findings: {result['summary']['total_findings']}
        
        Findings:
        {findings_text}
        
        Please provide a concise, professional security assessment summary that:
        1. Highlights the most critical security issues
        2. Explains the overall security posture
        3. Provides actionable recommendations
        4. Is written for both technical and non-technical stakeholders
        
        Keep the summary under 200 words and focus on business impact.
        """
        
        # Generate AI summary
        response = model.generate_content(prompt)
        ai_summary = response.text
        
        # Update scan results with AI summary
        scan_results[scan_id]["ai_summary"] = ai_summary
        
        # Store updated results in Firestore
        if db:
            try:
                doc_ref = db.collection('scans').document(scan_id)
                doc_ref.update({"ai_summary": ai_summary})
            except Exception as e:
                print(f"Error updating Firestore: {e}")
        
        return AISummaryResponse(
            summary=ai_summary,
            generated_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"Error generating AI summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate AI summary")

@app.get("/api/scans")
async def list_scans():
    """List all scans"""
    return {
        "scans": list(scan_results.values()),
        "total": len(scan_results)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
