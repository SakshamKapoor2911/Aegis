#!/bin/bash

# GKE Security Agent Cloud Build Deployment Script
# This script uses Cloud Build for more reliable deployments

set -e

# Configuration
PROJECT_ID="gke-turns-10-472809"
REGION="us-central1"
BACKEND_SERVICE="security-agent-backend"
FRONTEND_SERVICE="security-agent-frontend"

echo "🚀 Starting Cloud Build deployment..."

# Check if PROJECT_ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "❌ Please set PROJECT_ID environment variable"
    echo "   export PROJECT_ID=your-actual-project-id"
    exit 1
fi

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Please set GEMINI_API_KEY environment variable"
    echo "   export GEMINI_API_KEY=your_gemini_api_key"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Create Artifact Registry repository
echo "📦 Creating Artifact Registry repository..."
gcloud artifacts repositories create gke-security-agent \
    --repository-format=docker \
    --location=$REGION \
    --description="GKE Security Agent container images" || echo "Repository already exists"

# Build and deploy backend using Cloud Build
echo "🏗️ Building and deploying backend with Cloud Build..."
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/gke-security-agent/backend ./backend

# Deploy backend to Cloud Run
echo "🚀 Deploying backend to Cloud Run..."
gcloud run deploy $BACKEND_SERVICE \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/gke-security-agent/backend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8000 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,GOOGLE_CLOUD_PROJECT_ID=$PROJECT_ID

# Get backend URL
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region=$REGION --format="value(status.url)")
echo "✅ Backend deployed at: $BACKEND_URL"

# Build and deploy frontend using Cloud Build
echo "🏗️ Building and deploying frontend with Cloud Build..."
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/gke-security-agent/frontend ./frontend

# Deploy frontend to Cloud Run
echo "🚀 Deploying frontend to Cloud Run..."
gcloud run deploy $FRONTEND_SERVICE \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/gke-security-agent/frontend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 3000 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 5 \
    --set-env-vars NEXT_PUBLIC_API_URL=$BACKEND_URL

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE --region=$REGION --format="value(status.url)")
echo "✅ Frontend deployed at: $FRONTEND_URL"

echo ""
echo "🎉 Deployment completed successfully!"
echo "📱 Frontend URL: $FRONTEND_URL"
echo "🔧 Backend URL: $BACKEND_URL"
echo ""
echo "Next steps:"
echo "1. Visit the frontend URL to access your security agent"
echo "2. Enter the Online Boutique URL: http://35.232.193.170"
echo "3. Start scanning and generate AI summaries!"