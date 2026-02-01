#!/usr/bin/env python3
"""
🎭 AUTOMATED PREDICTION VENUE DEMO

Demonstrates the prediction trading venue with sample data and mock operations.
Shows how the entire system works without requiring real trading capital.

Author: Ether (Crypto Trading Swarm Agent)
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

def create_demo_output():
    """Create demonstration output files"""
    Path("output").mkdir(exist_ok=True)
    
    # Demo system metrics
    system_metrics = {
        "system_status": "operational",
        "uptime_hours": 4.7,
        "cycles_completed": 9,
        "last_update": datetime.now().isoformat(),
        "venue_stats": {
            "active_markets": 8,
            "active_agents": 15,
            "total_markets_created": 23,
            "total_predictions": 147,
            "accuracy_rate": 0.68
        },
        "trading_performance": {
            "total_signals": 12,
            "executed_trades": 8,
            "profitable_trades": 6,
            "total_pnl": 347.85,
            "accuracy_rate": 0.75
        }
    }
    
    with open("output/system_metrics.json", "w") as f:
        json.dump(system_metrics, f, indent=2, default=str)
    
    # Demo venue metrics
    venue_metrics = {
        "venue_stats": {
            "active_markets": 8,
            "active_agents": 15,
            "pending_signals": 3,
            "total_markets_created": 23,
            "total_predictions": 147,
            "total_volume": 15420.75,
            "accuracy_rate": 0.68,
            "last_update": datetime.now().isoformat()
        }
    }
    
    with open("output/venue_metrics.json", "w") as f:
        json.dump(venue_metrics, f, indent=2, default=str)
    
    # Demo trading performance
    trading_performance = {
        "metrics": {
            "total_signals": 12,
            "executed_trades": 8,
            "profitable_trades": 6,
            "total_pnl": 347.85,
            "accuracy_rate": 0.75,
            "avg_hold_time": 18.4
        },
        "last_updated": datetime.now().isoformat(),
        "active_trades": 2
    }
    
    with open("output/prediction_trading_performance.json", "w") as f:
        json.dump(trading_performance, f, indent=2, default=str)

async def demo_market_creation():
    """Demonstrate automatic market creation"""
    print("🏭 DEMO: Creating Prediction Markets")
    print("-" * 40)
    
    markets = [
        {
            "type": "crypto_price",
            "question": "Will BTC be above $105,000 by March 15, 2025?",
            "asset": "BTC",
            "current_price": 97500,
            "target_price": 105000,
            "agents_assigned": 5
        },
        {
            "type": "ai_performance", 
            "question": "Will AI trading agents achieve >70% win rate this month?",
            "target_accuracy": 0.70,
            "current_accuracy": 0.68,
            "agents_assigned": 4
        },
        {
            "type": "tech_trends",
            "question": "Will we see a major quantum computing breakthrough in 2025?",
            "trend_topic": "quantum_computing",
            "probability": 0.35,
            "agents_assigned": 6
        }
    ]
    
    for i, market in enumerate(markets, 1):
        print(f"   📊 Market {i}: {market['question']}")
        print(f"       Type: {market['type']}")
        print(f"       Agents: {market['agents_assigned']}")
        await asyncio.sleep(0.5)
    
    print(f"   ✅ Created {len(markets)} markets with {sum(m['agents_assigned'] for m in markets)} total agents")
    print()

async def demo_prediction_consensus():
    """Demonstrate prediction consensus aggregation"""
    print("📊 DEMO: Aggregating Agent Predictions")
    print("-" * 40)
    
    predictions = [
        {
            "market": "BTC > $105k",
            "agent_predictions": [
                {"agent": "crypto_specialist_1", "signal": 0.73, "confidence": 0.85, "reputation": 8500},
                {"agent": "crypto_specialist_2", "signal": 0.68, "confidence": 0.78, "reputation": 7200},
                {"agent": "trend_analyst", "signal": 0.82, "confidence": 0.71, "reputation": 6800},
                {"agent": "market_maker", "signal": 0.75, "confidence": 0.82, "reputation": 7900},
                {"agent": "arbitrage_hunter", "signal": 0.71, "confidence": 0.79, "reputation": 8100}
            ]
        }
    ]
    
    for prediction in predictions:
        print(f"   📈 Market: {prediction['market']}")
        
        total_weight = 0
        weighted_signal = 0
        weighted_confidence = 0
        
        for agent_pred in prediction['agent_predictions']:
            weight = agent_pred['reputation'] / 10000  # Normalize reputation
            weighted_signal += agent_pred['signal'] * weight
            weighted_confidence += agent_pred['confidence'] * weight
            total_weight += weight
            
            print(f"       🤖 {agent_pred['agent']}: {agent_pred['signal']:.2%} signal, {agent_pred['confidence']:.1%} confidence (rep: {agent_pred['reputation']})")
            await asyncio.sleep(0.3)
        
        # Calculate consensus
        consensus_signal = weighted_signal / total_weight
        consensus_confidence = weighted_confidence / total_weight
        
        print(f"   🎯 CONSENSUS: {consensus_signal:.2%} signal strength, {consensus_confidence:.1%} confidence")
        
        # Check execution threshold
        threshold = 0.70
        if consensus_confidence >= threshold:
            print(f"   ✅ EXECUTION APPROVED: Confidence {consensus_confidence:.1%} ≥ {threshold:.1%} threshold")
        else:
            print(f"   🚫 EXECUTION BLOCKED: Confidence {consensus_confidence:.1%} < {threshold:.1%} threshold")
    
    print()

async def demo_trading_execution():
    """Demonstrate trading signal execution"""
    print("💼 DEMO: Executing Trading Signals")
    print("-" * 40)
    
    signals = [
        {
            "asset": "BTC-USDT",
            "direction": "long",
            "size": 0.021,  # 2.1%
            "confidence": 0.74,
            "reasoning": "Prediction consensus: 73% bullish signal with 74% confidence from 5 agents"
        },
        {
            "asset": "ETH-USDT", 
            "direction": "short",
            "size": 0.018,  # 1.8%
            "confidence": 0.71,
            "reasoning": "Prediction consensus: -45% bearish signal with 71% confidence from 4 agents"
        }
    ]
    
    for i, signal in enumerate(signals, 1):
        print(f"   ⚡ Signal {i}: {signal['direction'].upper()} {signal['asset']}")
        print(f"       Size: {signal['size']:.1%} of portfolio")
        print(f"       Confidence: {signal['confidence']:.1%}")
        print(f"       Reasoning: {signal['reasoning']}")
        
        # Simulate execution
        print(f"       🔄 Executing trade...")
        await asyncio.sleep(0.8)
        
        # Mock execution result
        executed_price = 97500 if "BTC" in signal['asset'] else 3200
        success = random.choice([True, True, True, False])  # 75% success rate
        
        if success:
            print(f"       ✅ EXECUTED at ${executed_price:,}")
        else:
            print(f"       ❌ FAILED - insufficient liquidity")
        print()

async def demo_performance_update():
    """Demonstrate performance tracking"""
    print("📈 DEMO: Performance Tracking")
    print("-" * 40)
    
    # Simulate performance metrics update
    metrics = {
        "total_signals_processed": 12,
        "trades_executed": 8, 
        "profitable_trades": 6,
        "current_accuracy": 0.75,
        "total_pnl": 347.85,
        "avg_hold_time_hours": 18.4,
        "best_performing_agent": "crypto_specialist_1",
        "worst_performing_agent": "trend_analyst_3"
    }
    
    print("   📊 Current Performance Metrics:")
    print(f"       🎯 Signal Accuracy: {metrics['current_accuracy']:.1%}")
    print(f"       💰 Total P&L: ${metrics['total_pnl']:,.2f}")
    print(f"       📈 Trades: {metrics['profitable_trades']}/{metrics['trades_executed']} profitable")
    print(f"       ⏱️  Avg Hold Time: {metrics['avg_hold_time_hours']:.1f} hours")
    print(f"       🏆 Top Performer: {metrics['best_performing_agent']}")
    print()
    
    # Reputation updates
    print("   🏆 Agent Reputation Updates:")
    reputation_changes = [
        {"agent": "crypto_specialist_1", "old": 8500, "new": 8650, "change": "+150"},
        {"agent": "market_maker_2", "old": 7900, "new": 8020, "change": "+120"}, 
        {"agent": "trend_analyst_3", "old": 6800, "new": 6720, "change": "-80"}
    ]
    
    for update in reputation_changes:
        change_color = "🟢" if "+" in update['change'] else "🔴"
        print(f"       {change_color} {update['agent']}: {update['old']} → {update['new']} ({update['change']})")
    
    print()

async def main_demo():
    """Run complete venue demonstration"""
    print("🎭 AUTOMATED PREDICTION TRADING VENUE - LIVE DEMO")
    print("=" * 60)
    print()
    print("🏛️ Welcome to Ether's Automated Prediction Exchange!")
    print("   This demo shows how AI agents predict markets and execute trades.")
    print()
    
    # Create demo output files
    create_demo_output()
    
    # Run demo sequence
    await demo_market_creation()
    await asyncio.sleep(1)
    
    await demo_prediction_consensus()
    await asyncio.sleep(1)
    
    await demo_trading_execution()
    await asyncio.sleep(1)
    
    await demo_performance_update()
    
    print("🎯 DEMO COMPLETE")
    print("-" * 40)
    print("✅ Demo files created in output/ directory")
    print("📊 Run './check_status.py' to see venue status")
    print("🚀 Run './launch_venue.py' to start the real system")
    print()

if __name__ == "__main__":
    asyncio.run(main_demo())