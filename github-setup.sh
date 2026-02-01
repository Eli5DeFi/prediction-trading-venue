#!/bin/bash

# 🐙 GITHUB SETUP SCRIPT FOR PREDICTION VENUE

echo "🐙 SETTING UP GITHUB REPOSITORY"
echo "================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "🏛️ Initial commit: Automated Prediction Trading Venue"
fi

echo "✅ Git repository ready"

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "🐙 GitHub CLI found. Creating repository..."
    
    # Create GitHub repository
    gh repo create prediction-trading-venue --public --description "🏛️ Automated Prediction Trading Venue - AI-Powered Prediction Market Exchange with React Dashboard" --clone=false
    
    if [ $? -eq 0 ]; then
        echo "✅ GitHub repository created"
        
        # Add remote origin
        gh repo view --json url --jq .url | xargs -I {} git remote add origin {}.git
        
        # Push to GitHub
        echo "📤 Pushing code to GitHub..."
        git branch -M main
        git push -u origin main
        
        echo "✅ Code pushed to GitHub successfully!"
    else
        echo "⚠️ Repository might already exist or there was an error"
    fi
else
    echo "⚠️ GitHub CLI not found. Please follow manual setup:"
    echo ""
    echo "1️⃣ Go to https://github.com/new"
    echo "2️⃣ Create a repository named 'prediction-trading-venue'"
    echo "3️⃣ Run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/prediction-trading-venue.git"
    echo "   git branch -M main" 
    echo "   git push -u origin main"
    echo ""
fi

echo ""
echo "🎯 REPOSITORY SETUP COMPLETE"
echo "============================"
echo ""
echo "📁 Repository structure:"
echo "   • 🚀 Complete venue system"
echo "   • 🎨 React frontend dashboard"
echo "   • 🌐 API server"
echo "   • 📖 Documentation"
echo "   • ⚙️ Vercel deployment config"
echo ""
echo "🚀 Next steps:"
echo "   • Push any changes: git add . && git commit -m 'Update' && git push"
echo "   • Deploy to Vercel: ./deploy-to-vercel.sh"
echo "   • Share your repository: https://github.com/YOUR_USERNAME/prediction-trading-venue"