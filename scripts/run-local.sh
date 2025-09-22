#!/bin/bash

# Local Development Script
# This script runs the security agent locally for development and testing

set -e

echo "🚀 Starting local development environment..."

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "❌ .env file not found in backend directory"
    echo "📝 Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env file"
    echo "⚠️  Please edit backend/.env and add your GEMINI_API_KEY"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    exit 1
fi

# Load environment variables
export $(cat backend/.env | grep -v '^#' | xargs)

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY not found in .env file"
    echo "   Please add GEMINI_API_KEY=your_api_key to backend/.env"
    exit 1
fi

echo "✅ Environment variables loaded"

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Start backend in background
echo "🚀 Starting FastAPI backend..."
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install

# Start frontend
echo "🚀 Starting Next.js frontend..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 Local development environment started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✅ Services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for user to stop
wait
