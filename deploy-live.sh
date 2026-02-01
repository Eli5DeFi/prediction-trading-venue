#!/bin/bash

# 🔥 DEPLOY LIVE PREDICTION VENUE WITH REAL DATA

echo "🔥 DEPLOYING LIVE PREDICTION VENUE"
echo "=================================="
echo "🎯 This will deploy with REAL data integration!"
echo ""

# Check if we're in the right directory
if [ ! -f "vercel-live.json" ]; then
    echo "❌ Error: vercel-live.json not found. Run from project root."
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ Vercel CLI available"

# Install API dependencies
echo "📦 Installing API dependencies..."
cd api && pip3 install -r requirements.txt && cd ..
echo "✅ API dependencies installed"

# Build the frontend with production settings
echo "🏗️ Building frontend for LIVE deployment..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Set production environment for live data
export REACT_APP_API_URL="https://prediction-venue-live.vercel.app"
export REACT_APP_DATA_SOURCE="live"
export REACT_APP_ENABLE_LIVE_DATA="true"

# Build the React app
echo "🔨 Building React app with LIVE configuration..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed"
    exit 1
fi

echo "✅ Frontend built successfully with LIVE data configuration"
cd ..

# Deploy to Vercel with live configuration
echo "🚀 Deploying LIVE system to Vercel..."
vercel --prod --config vercel-live.json --yes

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 LIVE DEPLOYMENT COMPLETE!"
    echo "==========================="
    echo ""
    echo "🔥 Your LIVE prediction venue is now deployed!"
    echo ""
    echo "✨ Features:"
    echo "   🌐 Real crypto prices from CoinGecko API"
    echo "   📊 Live market data and predictions"
    echo "   💼 Real trading integration capabilities"
    echo "   🤖 Dynamic AI agent performance tracking"
    echo "   📡 Live data updates every 30 seconds"
    echo ""
    echo "🎯 Data Sources:"
    echo "   • Live crypto prices"
    echo "   • Real market volatility"
    echo "   • Dynamic prediction markets"
    echo "   • Live agent reputation scoring"
    echo ""
    echo "⚡ Built by Ether - Crypto Trading Swarm Agent"
    echo "🔗 Share your LIVE prediction venue with the world!"
else
    echo "❌ Deployment failed. Check logs above for details."
    exit 1
fi