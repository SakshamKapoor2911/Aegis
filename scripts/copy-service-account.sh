#!/bin/bash

# Copy service account key to backend directory
# This script copies the service account key to the backend directory for easier access

set -e

SOURCE_KEY="/c/Users/Saksham Kapoor/Downloads/gke-turns-10-472809-54676967bf7d.json"
TARGET_KEY="backend/firestore-key.json"

echo "📋 Copying service account key..."

if [ -f "$SOURCE_KEY" ]; then
    cp "$SOURCE_KEY" "$TARGET_KEY"
    echo "✅ Service account key copied to: $TARGET_KEY"
    
    # Set proper permissions
    chmod 600 "$TARGET_KEY"
    echo "🔒 Set proper permissions on key file"
else
    echo "❌ Source key file not found: $SOURCE_KEY"
    echo "Please check the path and try again"
    exit 1
fi

echo "🎉 Service account key setup completed!"
