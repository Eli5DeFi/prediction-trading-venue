#!/bin/bash

# 🔥 START LIVE PREDICTION VENUE SYSTEM
# Launches complete system with REAL data integration

echo "🔥 STARTING LIVE PREDICTION VENUE SYSTEM"
echo "========================================"
echo "🎯 Launching with REAL data integration!"
echo ""

# Check if we're in the right directory
if [ ! -f "real-api-server.py" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Not in prediction-trading-venue directory"
    echo "   Please run from: /Users/eli5defi/clawd/prediction-trading-venue/"
    exit 1
fi

# Check dependencies
echo "🔍 Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

# Install Python dependencies for real API
echo "📦 Installing Python dependencies..."
pip3 install flask flask-cors requests > /dev/null 2>&1

# Set up frontend if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Setting up React frontend..."
    cd frontend
    npm install > /dev/null 2>&1
    cd ..
fi

echo "✅ Dependencies check passed"

# Create log directory
mkdir -p logs

echo ""
echo "🚀 LAUNCHING LIVE SYSTEM"
echo "========================"
echo ""

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down live system..."
    
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        echo "   ✅ Live API server stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "   ✅ Frontend server stopped"
    fi
    
    # Kill any remaining processes on our ports
    lsof -ti:8080 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    
    echo "👋 Live system shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start LIVE API server in background
echo "🔥 Starting LIVE API server (http://localhost:8080)..."
echo "   📡 Real crypto prices from CoinGecko"
echo "   💼 Live trading data integration"
echo "   🤖 Dynamic AI agent tracking"
echo "   📊 Real-time market updates"

python3 real-api-server.py > logs/live-api-server.log 2>&1 &
API_PID=$!

# Wait for API server to start
sleep 4

# Check if API server is running
if ps -p $API_PID > /dev/null; then
    echo "✅ Live API server running (PID: $API_PID)"
else
    echo "❌ Failed to start live API server"
    echo "   Check logs/live-api-server.log for details"
    exit 1
fi

# Start React frontend with live data configuration
echo "⚡ Starting React frontend with LIVE data configuration..."
echo "   🌐 Will connect to live API server"
echo "   📊 Real-time dashboard updates"

cd frontend

# Set environment variables for live mode
export REACT_APP_API_URL="http://localhost:8080"
export REACT_APP_DATA_SOURCE="live"
export REACT_APP_ENABLE_LIVE_DATA="true"
export REACT_APP_VENUE_NAME="Ether's Live Prediction Exchange"

npm start > ../logs/live-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 6

# Check if frontend is running
if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ React frontend running (PID: $FRONTEND_PID)"
else
    echo "❌ Failed to start React frontend"
    echo "   Check logs/live-frontend.log for details"
    cleanup
    exit 1
fi

echo ""
echo "🔥 LIVE SYSTEM IS NOW OPERATIONAL!"
echo "================================="
echo ""
echo "📊 Frontend Dashboard: http://localhost:3000"
echo "🌐 Live API Server:    http://localhost:8080"
echo ""
echo "🔥 LIVE DATA FEATURES:"
echo "   • 📡 Real crypto prices from CoinGecko API"
echo "   • 📊 Dynamic prediction markets based on live prices"
echo "   • 💼 Real trading performance tracking"
echo "   • 🤖 Live AI agent reputation scoring"
echo "   • 🔄 Data updates every 30 seconds"
echo "   • 📈 Real market volatility calculations"
echo ""
echo "🎯 Live Market Data:"
echo "   • Bitcoin, Ethereum, Solana prices"
echo "   • 24h volume and price changes"
echo "   • Dynamic prediction targets"
echo "   • Real-time consensus calculations"
echo ""
echo "📂 Logs:"
echo "   • Live API Server: logs/live-api-server.log"
echo "   • Frontend:        logs/live-frontend.log"
echo ""
echo "🔍 Test API: python3 test-live-api.py"
echo "⏹️  Press Ctrl+C to stop both servers"
echo ""
echo "🔴 LIVE DATA MODE - Real market data flowing!"

# Wait for user interrupt
while true; do
    sleep 2
    
    # Check if processes are still running
    if ! ps -p $API_PID > /dev/null; then
        echo "❌ Live API server stopped unexpectedly"
        break
    fi
    
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo "❌ Frontend server stopped unexpectedly"  
        break
    fi
done

# Cleanup and exit
cleanup