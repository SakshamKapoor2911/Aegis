#!/bin/bash

# Setup Firestore Database for GKE Security Agent
# This script creates the Firestore database and sets up the necessary permissions

set -e

PROJECT_ID=${PROJECT_ID:-"gke-turns-10-472809"}
REGION=${REGION:-"us-central1"}

echo "🔥 Setting up Firestore database for project: $PROJECT_ID"

# Set the project
gcloud config set project $PROJECT_ID

# Enable Firestore API
echo "📋 Enabling Firestore API..."
gcloud services enable firestore.googleapis.com

# Create Firestore database
echo "🗄️ Creating Firestore database..."
gcloud firestore databases create --region=$REGION --project=$PROJECT_ID || echo "Database might already exist"

# Verify database exists
echo "✅ Verifying Firestore database..."
gcloud firestore databases list --project=$PROJECT_ID

echo "🎉 Firestore setup completed!"
echo ""
echo "Next steps:"
echo "1. Deploy your backend with the updated code"
echo "2. Test Firestore connectivity: curl https://your-backend-url/api/firestore/test"
echo "3. Run a security scan to see results stored in Firestore"
