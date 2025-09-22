# Firestore Setup Guide

This guide will help you set up Firestore for the GKE Security Agent to store scan results persistently.

## Quick Setup

### 1. Create Firestore Database
```bash
# Run the setup script
chmod +x scripts/setup-firestore.sh
./scripts/setup-firestore.sh
```

### 2. Copy Service Account Key
```bash
# Copy the service account key to the backend directory
chmod +x scripts/copy-service-account.sh
./scripts/copy-service-account.sh
```

### 3. Deploy Updated Backend
```bash
# Deploy the updated backend with Firestore support
cd backend
gcloud builds submit --tag us-central1-docker.pkg.dev/gke-turns-10-472809/gke-security-agent/backend .
gcloud run deploy security-agent-backend --image us-central1-docker.pkg.dev/gke-turns-10-472809/gke-security-agent/backend --platform managed --region us-central1 --allow-unauthenticated --port 8000 --memory 1Gi --cpu 1 --max-instances 10 --timeout 300 --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,GOOGLE_CLOUD_PROJECT_ID=gke-turns-10-472809
```

## Manual Setup (if scripts don't work)

### 1. Enable Firestore API
```bash
gcloud services enable firestore.googleapis.com
```

### 2. Create Firestore Database
```bash
gcloud firestore databases create --region=us-central1 --project=gke-turns-10-472809
```

### 3. Verify Database Creation
```bash
gcloud firestore databases list --project=gke-turns-10-472809
```

## Testing Firestore

### 1. Test Firestore Connectivity
```bash
curl https://your-backend-url/api/firestore/test
```

### 2. View Stored Scans
```bash
curl https://your-backend-url/api/firestore/scans
```

## Troubleshooting

### Error: "The database (default) does not exist"
- **Solution**: Run `gcloud firestore databases create --region=us-central1`

### Error: "Service account key file not found"
- **Solution**: Run `./scripts/copy-service-account.sh` or set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### Error: "Permission denied"
- **Solution**: Make sure your service account has the `Cloud Datastore User` role

## Benefits of Firestore Integration

1. **Persistent Storage**: Scan results are stored permanently
2. **Scalability**: Can handle large numbers of scans
3. **Real-time Updates**: Frontend can get live updates
4. **Backup**: Data is automatically backed up by Google Cloud
5. **Analytics**: Can analyze scan trends over time

## Next Steps

Once Firestore is set up:
1. Run a security scan
2. Check that results are stored in Firestore
3. Verify the frontend displays results correctly
4. Enjoy persistent scan result storage!
