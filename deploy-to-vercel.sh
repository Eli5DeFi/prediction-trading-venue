#!/bin/bash

# 🚀 VERCEL DEPLOYMENT SCRIPT FOR PREDICTION VENUE

echo "🚀 DEPLOYING PREDICTION VENUE TO VERCEL"
echo "======================================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Run from project root."
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ Vercel CLI available"

# Build the frontend
echo "🏗️ Building frontend..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Build the React app
echo "🔨 Building React app..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed"
    exit 1
fi

echo "✅ Frontend built successfully"
cd ..

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================="
echo ""
echo "🌐 Your prediction venue dashboard is now live on Vercel!"
echo ""
echo "📊 Features deployed:"
echo "   • Real-time prediction markets dashboard"
echo "   • Trading performance analytics"
echo "   • AI agent network monitoring"
echo "   • System health dashboard"
echo "   • Live activity feed"
echo ""
echo "💡 Next steps:"
echo "   • Visit your Vercel dashboard to see the deployment"
echo "   • Share the live URL with others"
echo "   • Set up custom domain if needed"
echo ""
echo "⚡ Built by Ether - Crypto Trading Swarm Agent"