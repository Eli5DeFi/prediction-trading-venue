#!/bin/bash

# 🚀 QUICK LAUNCH SCRIPT FOR PREDICTION VENUE DASHBOARD

echo "🏛️ LAUNCHING PREDICTION VENUE DASHBOARD"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Not in frontend directory"
    echo "   Please run from: prediction-trading-venue/frontend/"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Dependencies not installed. Running setup..."
    chmod +x setup.sh
    ./setup.sh
fi

echo "🚀 Starting React development server..."
echo ""
echo "📊 Dashboard Features:"
echo "   • Real-time prediction markets"
echo "   • Live trading performance"  
echo "   • AI agent network status"
echo "   • System health monitoring"
echo ""
echo "🌐 Opening at: http://localhost:3000"
echo "⚡ Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm start