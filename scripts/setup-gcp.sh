#!/bin/bash

# GKE Security Agent GCP Setup Script
# This script sets up the GCP project and deploys Online Boutique to GKE

set -e

# Configuration
PROJECT_ID="gke-turns-10-472809"
REGION=${REGION:-"us-central1"}
CLUSTER_NAME="online-boutique-cluster"

echo "🚀 Setting up GCP project and deploying Online Boutique..."

# Check if PROJECT_ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "❌ Please set PROJECT_ID environment variable"
    echo "   export PROJECT_ID=your-actual-project-id"
    exit 1
fi

# Set project
echo "📋 Setting project to $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable container.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Create GKE cluster
echo "🏗️ Creating GKE Autopilot cluster..."
gcloud container clusters create-auto $CLUSTER_NAME \
    --project=$PROJECT_ID \
    --region=$REGION

# Get cluster credentials
echo "🔐 Getting cluster credentials..."
gcloud container clusters get-credentials $CLUSTER_NAME \
    --project=$PROJECT_ID \
    --region=$REGION

# Create Artifact Registry repository for Online Boutique
echo "📦 Creating Artifact Registry repository for Online Boutique..."
gcloud artifacts repositories create microservices-demo \
    --repository-format=docker \
    --location=us \
    --description="Online Boutique microservices demo" || echo "Repository already exists"

# Configure Docker authentication
echo "🔐 Configuring Docker authentication..."
gcloud auth configure-docker us-docker.pkg.dev

# Clone and deploy Online Boutique
echo "📥 Cloning Online Boutique repository..."
if [ ! -d "microservices-demo" ]; then
    git clone --depth 1 --branch v0 https://github.com/GoogleCloudPlatform/microservices-demo.git
fi

cd microservices-demo

# Deploy Online Boutique using kubectl
echo "🚀 Deploying Online Boutique to GKE..."
kubectl apply -f ./release/kubernetes-manifests.yaml

# Wait for deployment
echo "⏳ Waiting for Online Boutique to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/frontend

# Get external IP
echo "🌐 Getting external IP..."
EXTERNAL_IP=$(kubectl get service frontend-external -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

if [ -z "$EXTERNAL_IP" ]; then
    echo "⏳ External IP not ready yet, waiting..."
    sleep 30
    EXTERNAL_IP=$(kubectl get service frontend-external -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
fi

echo ""
echo "🎉 Online Boutique deployed successfully!"
echo "🌐 External IP: $EXTERNAL_IP"
echo "🔗 URL: http://$EXTERNAL_IP"
echo ""
echo "Next steps:"
echo "1. Wait a few minutes for the external IP to be assigned"
echo "2. Visit http://$EXTERNAL_IP to verify Online Boutique is running"
echo "3. Use this URL as the target for your security agent"
echo ""
echo "To check the status:"
echo "kubectl get pods"
echo "kubectl get services"
echo ""
echo "To get the external IP again:"
echo "kubectl get service frontend-external"