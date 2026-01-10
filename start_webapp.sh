#!/bin/bash

# Credit Risk Assessment Web App Startup Script
# This script starts both the backend API and frontend dev server

echo "======================================"
echo "  Credit Risk Assessment Web App"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Please create one first: python -m venv venv"
    exit 1
fi

# Check if models exist
if [ ! -d "models" ] || [ ! -f "models/LogisticRegression.pkl" ]; then
    echo "❌ Trained models not found!"
    echo "   Please train the model first: python run_train.py"
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not installed!"
    echo "   Please run: cd frontend && npm install"
    exit 1
fi

echo "✅ All prerequisites met!"
echo ""
echo "Starting servers..."
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup INT TERM

# Start backend server
echo "🚀 Starting Backend API on http://localhost:5001"
source venv/bin/activate
python api/app.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend server
echo "🚀 Starting Frontend on http://localhost:5173"
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "======================================"
echo "  🎉 Application is running!"
echo "======================================"
echo ""
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:5001"
echo ""
echo "  Press Ctrl+C to stop both servers"
echo "======================================"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
