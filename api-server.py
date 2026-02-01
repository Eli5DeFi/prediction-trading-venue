#!/usr/bin/env python3
"""
🌐 PREDICTION VENUE API SERVER

Simple Flask server to serve demo data for the frontend dashboard.
Provides mock API endpoints with real venue data structure.

Author: Ether (Crypto Trading Swarm Agent)
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load demo data
def load_demo_data():
    """Load demonstration data for API responses"""
    return {
        "status": "operational",
        "uptime": "4.7h",
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "activeMarkets": 8,
            "activeAgents": 15,
            "totalPredictions": 147,
            "accuracyRate": 0.68,
            "totalPnL": 347.85,
            "winRate": 0.75,
            "executedTrades": 8,
            "profitableTrades": 6
        },
        "markets": [
            {
                "id": 1,
                "question": "Will BTC be above $105,000 by March 15, 2025?",
                "type": "crypto_price",
                "asset": "BTC",
                "consensus": 0.74,
                "confidence": 0.79,
                "agentCount": 5,
                "volume": 15420,
                "status": "active",
                "currentPrice": 97500,
                "targetPrice": 105000
            },
            {
                "id": 2,
                "question": "Will AI trading agents achieve >70% win rate this month?",
                "type": "ai_performance",
                "consensus": 0.62,
                "confidence": 0.71,
                "agentCount": 4,
                "volume": 8900,
                "status": "active",
                "targetAccuracy": 0.70,
                "currentAccuracy": 0.68
            },
            {
                "id": 3,
                "question": "Will we see a major quantum computing breakthrough in 2025?",
                "type": "tech_trends",
                "consensus": 0.35,
                "confidence": 0.68,
                "agentCount": 6,
                "volume": 12100,
                "status": "active",
                "trendTopic": "quantum_computing"
            }
        ],
        "agents": [
            {
                "id": 1,
                "name": "crypto_specialist_1",
                "type": "Crypto Specialist",
                "reputation": 8650,
                "accuracy": 0.82,
                "trades": 23,
                "status": "active",
                "specialty": "BTC/ETH"
            },
            {
                "id": 2,
                "name": "market_maker_2",
                "type": "Market Maker",
                "reputation": 8020,
                "accuracy": 0.76,
                "trades": 31,
                "status": "active",
                "specialty": "Liquidity"
            },
            {
                "id": 3,
                "name": "trend_analyst",
                "type": "Trend Analyst",
                "reputation": 6720,
                "accuracy": 0.69,
                "trades": 18,
                "status": "active",
                "specialty": "Tech Trends"
            },
            {
                "id": 4,
                "name": "arbitrage_hunter",
                "type": "Arbitrage Hunter",
                "reputation": 7800,
                "accuracy": 0.73,
                "trades": 27,
                "status": "active",
                "specialty": "Price Inefficiencies"
            },
            {
                "id": 5,
                "name": "ai_specialist",
                "type": "AI Specialist",
                "reputation": 7300,
                "accuracy": 0.71,
                "trades": 19,
                "status": "active",
                "specialty": "AI Performance"
            }
        ],
        "recentTrades": [
            {
                "id": 1,
                "asset": "BTC-USDT",
                "direction": "long",
                "size": 0.021,
                "confidence": 0.74,
                "status": "executed",
                "pnl": 45.20,
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat()
            },
            {
                "id": 2,
                "asset": "ETH-USDT",
                "direction": "short", 
                "size": 0.018,
                "confidence": 0.71,
                "status": "executed",
                "pnl": 23.50,
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                "id": 3,
                "asset": "SOL-USDT",
                "direction": "long",
                "size": 0.015,
                "confidence": 0.69,
                "status": "pending",
                "pnl": 0,
                "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat()
            }
        ],
        "systemHealth": {
            "components": [
                {"name": "Prediction Engine", "status": "operational", "uptime": "99.8%"},
                {"name": "Trading Bridge", "status": "operational", "uptime": "99.5%"},
                {"name": "Agent Coordinator", "status": "operational", "uptime": "100%"},
                {"name": "Risk Manager", "status": "operational", "uptime": "99.9%"}
            ],
            "performance": {
                "cpu": 23,
                "memory": 67,
                "network": 45
            }
        }
    }

@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        "name": "Prediction Venue API",
        "version": "1.0.0",
        "description": "API server for Automated Prediction Trading Venue",
        "endpoints": [
            "/api/system-status",
            "/api/markets",
            "/api/agents", 
            "/api/trades",
            "/api/health"
        ]
    })

@app.route('/api/system-status')
def system_status():
    """Complete system status with all data"""
    return jsonify(load_demo_data())

@app.route('/api/markets')
def markets():
    """Prediction markets data"""
    data = load_demo_data()
    return jsonify({
        "markets": data["markets"],
        "total": len(data["markets"]),
        "active": len([m for m in data["markets"] if m["status"] == "active"])
    })

@app.route('/api/agents')
def agents():
    """AI agents status"""
    data = load_demo_data()
    return jsonify({
        "agents": data["agents"],
        "total": len(data["agents"]),
        "active": len([a for a in data["agents"] if a["status"] == "active"])
    })

@app.route('/api/trades')
def trades():
    """Recent trades data"""
    data = load_demo_data()
    return jsonify({
        "trades": data["recentTrades"],
        "metrics": data["metrics"]
    })

@app.route('/api/health')
def health():
    """System health monitoring"""
    data = load_demo_data()
    return jsonify({
        "status": data["status"],
        "uptime": data["uptime"],
        "systemHealth": data["systemHealth"],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/feed')
def activity_feed():
    """Live activity feed"""
    now = datetime.now()
    
    feed_items = [
        {
            "id": "trade-1",
            "type": "trade",
            "timestamp": (now - timedelta(minutes=5)).isoformat(),
            "title": "LONG BTC-USDT Executed",
            "description": "Size: 2.1% • Confidence: 74% • P&L: +$45.20",
            "status": "executed"
        },
        {
            "id": "market-1",
            "type": "market",
            "timestamp": (now - timedelta(minutes=12)).isoformat(),
            "title": "New Prediction Market Created",
            "description": "ETH price prediction market with 4 agents deployed",
            "status": "completed"
        },
        {
            "id": "consensus-1",
            "type": "consensus",
            "timestamp": (now - timedelta(minutes=18)).isoformat(),
            "title": "Consensus Reached",
            "description": "BTC market: 79% confidence, executable signal generated",
            "status": "executed"
        },
        {
            "id": "agent-1",
            "type": "agent",
            "timestamp": (now - timedelta(minutes=25)).isoformat(),
            "title": "Agent Reputation Updated",
            "description": "crypto_specialist_1 gained +150 reputation points",
            "status": "completed"
        }
    ]
    
    return jsonify({
        "feed": feed_items,
        "total": len(feed_items)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🏛️ PREDICTION VENUE API SERVER")
    print("=" * 40)
    print("🌐 Starting API server...")
    print("📡 Server will run at: http://localhost:8080")
    print("🔗 Available endpoints:")
    print("   • GET /api/system-status  - Complete system data")
    print("   • GET /api/markets       - Prediction markets")
    print("   • GET /api/agents        - AI agents status")
    print("   • GET /api/trades        - Trading history")
    print("   • GET /api/health        - System health")
    print("   • GET /api/feed          - Activity feed")
    print("")
    print("🎯 Frontend can connect to these endpoints")
    print("⚡ Press Ctrl+C to stop server")
    print("")
    
    app.run(host='0.0.0.0', port=8080, debug=True)