#!/bin/bash

# 🚀 FULL PREDICTION VENUE DASHBOARD LAUNCHER
# Starts both API server and React frontend for complete dashboard experience

echo "🏛️ AUTOMATED PREDICTION TRADING VENUE - FULL DASHBOARD"
echo "======================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "api-server.py" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Not in prediction-trading-venue directory"
    echo "   Please run from: /Users/eli5defi/clawd/prediction-trading-venue/"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed"
    echo "   Please install Python 3.7+ first"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed" 
    echo "   Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install flask flask-cors > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed"
else
    echo "⚠️  Warning: Could not install Python dependencies"
    echo "   You may need to install flask and flask-cors manually:"
    echo "   pip3 install flask flask-cors"
fi

# Set up frontend if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Setting up React frontend..."
    cd frontend
    chmod +x setup.sh
    ./setup.sh
    cd ..
    echo "✅ Frontend setup complete"
fi

# Create log directory
mkdir -p logs

echo ""
echo "🚀 LAUNCHING PREDICTION VENUE DASHBOARD"
echo "======================================="
echo ""

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down dashboard..."
    
    # Kill background processes
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        echo "   ✅ API server stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "   ✅ Frontend server stopped"
    fi
    
    # Kill any remaining processes on our ports
    lsof -ti:8080 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    
    echo "👋 Dashboard shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start API server in background
echo "🌐 Starting API server (http://localhost:8080)..."
python3 api-server.py > logs/api-server.log 2>&1 &
API_PID=$!

# Wait for API server to start
sleep 3

# Check if API server is running
if ps -p $API_PID > /dev/null; then
    echo "✅ API server running (PID: $API_PID)"
else
    echo "❌ Failed to start API server"
    echo "   Check logs/api-server.log for details"
    exit 1
fi

# Start React frontend in background
echo "⚡ Starting React frontend (http://localhost:3000)..."
cd frontend
npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 5

# Check if frontend is running
if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ React frontend running (PID: $FRONTEND_PID)"
else
    echo "❌ Failed to start React frontend"
    echo "   Check logs/frontend.log for details"
    cleanup
    exit 1
fi

echo ""
echo "🎯 DASHBOARD IS NOW LIVE!"
echo "========================="
echo ""
echo "📊 Frontend Dashboard: http://localhost:3000"
echo "🌐 API Server:         http://localhost:8080"
echo ""
echo "✨ Features Available:"
echo "   • 📈 Live prediction markets with AI agent consensus"
echo "   • 💼 Trading performance dashboard and analytics" 
echo "   • 🤖 AI agent network status and reputation tracking"
echo "   • 🛡️ System health monitoring and performance metrics"
echo "   • 📡 Real-time activity feed with live updates"
echo ""
echo "🔗 API Endpoints:"
echo "   • GET /api/system-status  - Complete system data"
echo "   • GET /api/markets       - Prediction markets"
echo "   • GET /api/agents        - AI agents status"
echo "   • GET /api/trades        - Trading history"
echo "   • GET /api/health        - System health"
echo "   • GET /api/feed          - Activity feed"
echo ""
echo "📂 Logs:"
echo "   • API Server: logs/api-server.log"
echo "   • Frontend:   logs/frontend.log"
echo ""
echo "⏹️  Press Ctrl+C to stop both servers"
echo ""

# Wait for user interrupt
while true; do
    sleep 1
    
    # Check if processes are still running
    if ! ps -p $API_PID > /dev/null; then
        echo "❌ API server stopped unexpectedly"
        break
    fi
    
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo "❌ Frontend server stopped unexpectedly"
        break
    fi
done

# Cleanup and exit
cleanup