#!/bin/bash

# 🏛️ PREDICTION VENUE FRONTEND SETUP SCRIPT
# Sets up and launches the React dashboard for the prediction trading venue

echo "🏛️ Setting up Prediction Venue Frontend Dashboard..."
echo "=" * 50

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are available"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env configuration file..."
    cat > .env << EOL
# Prediction Venue Dashboard Configuration
REACT_APP_API_URL=http://localhost:8080
REACT_APP_VENUE_NAME=Ether's Prediction Exchange
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0
GENERATE_SOURCEMAP=false
EOL
    echo "✅ Created .env file"
fi

# Create directories
mkdir -p public/static
mkdir -p src/utils
mkdir -p src/hooks

echo "🎯 Frontend setup complete!"
echo ""
echo "🚀 To start the dashboard:"
echo "   npm start"
echo ""
echo "🌐 Dashboard will be available at:"
echo "   http://localhost:3000"
echo ""
echo "📊 Features:"
echo "   • Live prediction markets"
echo "   • Trading performance dashboard" 
echo "   • AI agent status monitoring"
echo "   • Real-time activity feed"
echo "   • System health monitoring"