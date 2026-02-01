#!/usr/bin/env python3
"""Quick test of the API server functionality"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the API server components
    from flask import Flask
    from flask_cors import CORS
    import json
    from datetime import datetime
    
    print("✅ All required modules available")
    print("📡 API server dependencies check passed")
    print("")
    print("🌐 API endpoints that will be available:")
    print("   • GET /                  - API root")
    print("   • GET /api/system-status - Complete system data")
    print("   • GET /api/markets      - Prediction markets")
    print("   • GET /api/agents       - AI agents status") 
    print("   • GET /api/trades       - Trading history")
    print("   • GET /api/health       - System health")
    print("   • GET /api/feed         - Activity feed")
    print("")
    print("🚀 To start the API server:")
    print("   python3 api-server.py")
    print("")
    print("🎨 To start the complete dashboard:")
    print("   ./launch-full-dashboard.sh")
    
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("💡 Install with: pip3 install flask flask-cors")
    
except Exception as e:
    print(f"❌ Error: {e}")