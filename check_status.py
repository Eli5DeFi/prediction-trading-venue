#!/usr/bin/env python3
"""
📊 PREDICTION VENUE STATUS CHECKER

Quick health check and performance summary for the automated prediction trading venue.
Can be run independently to monitor venue performance.

Author: Ether (Crypto Trading Swarm Agent)
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

def load_json_file(file_path: str) -> Optional[Dict]:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.0f}m"
    elif seconds < 86400:
        return f"{seconds/3600:.1f}h"
    else:
        return f"{seconds/86400:.1f}d"

def format_percentage(value: float) -> str:
    """Format percentage with color coding"""
    color = "🟢" if value >= 0.6 else "🟡" if value >= 0.4 else "🔴"
    return f"{color} {value:.1%}"

def format_currency(value: float) -> str:
    """Format currency value"""
    if abs(value) >= 1000000:
        return f"${value/1000000:.1f}M"
    elif abs(value) >= 1000:
        return f"${value/1000:.1f}K"
    else:
        return f"${value:.2f}"

def check_venue_status():
    """Check and display venue status"""
    print("📊 AUTOMATED PREDICTION TRADING VENUE - STATUS CHECK")
    print("=" * 60)
    print()
    
    # Check if venue is running
    venue_dir = Path(".")
    if not venue_dir.joinpath("config").exists():
        print("❌ ERROR: Not in venue directory or venue not set up")
        print("   Please run from prediction-trading-venue/ directory")
        return False
    
    # Load system metrics
    system_metrics = load_json_file("output/system_metrics.json")
    venue_metrics = load_json_file("output/venue_metrics.json") 
    trading_metrics = load_json_file("output/prediction_trading_performance.json")
    
    if not system_metrics:
        print("🔴 VENUE STATUS: OFFLINE")
        print("   No system metrics found - venue may not be running")
        print()
        print("🚀 To start venue: python3 launch_venue.py")
        return False
    
    print("🟢 VENUE STATUS: ONLINE")
    print()
    
    # System Status
    print("🖥️  SYSTEM STATUS")
    print("-" * 20)
    uptime_hours = system_metrics.get('uptime_hours', 0)
    cycles_completed = system_metrics.get('cycles_completed', 0)
    last_update = system_metrics.get('last_update', 'Unknown')
    
    print(f"   ⏱️  Uptime: {format_duration(uptime_hours * 3600)}")
    print(f"   🔄 Cycles: {cycles_completed}")
    print(f"   🕐 Last Update: {last_update[:19].replace('T', ' ')}")
    print()
    
    # Venue Metrics
    if venue_metrics:
        print("🏛️  VENUE METRICS")
        print("-" * 20)
        stats = venue_metrics.get('venue_stats', {})
        
        print(f"   📊 Active Markets: {stats.get('active_markets', 0)}")
        print(f"   🤖 Active Agents: {stats.get('active_agents', 0)}")
        print(f"   📈 Total Markets Created: {stats.get('total_markets_created', 0)}")
        print(f"   🎯 Total Predictions: {stats.get('total_predictions', 0)}")
        
        accuracy = stats.get('accuracy_rate', 0)
        if accuracy > 0:
            print(f"   🎯 Accuracy Rate: {format_percentage(accuracy)}")
        print()
    
    # Trading Performance
    if trading_metrics:
        print("💼 TRADING PERFORMANCE") 
        print("-" * 20)
        metrics = trading_metrics.get('metrics', {})
        
        total_signals = metrics.get('total_signals', 0)
        executed_trades = metrics.get('executed_trades', 0)
        profitable_trades = metrics.get('profitable_trades', 0)
        total_pnl = metrics.get('total_pnl', 0)
        accuracy_rate = metrics.get('accuracy_rate', 0)
        
        print(f"   📡 Total Signals: {total_signals}")
        print(f"   ✅ Executed Trades: {executed_trades}")
        print(f"   💰 Profitable Trades: {profitable_trades}")
        print(f"   💵 Total P&L: {format_currency(total_pnl)}")
        
        if total_signals > 0:
            execution_rate = executed_trades / total_signals
            print(f"   🎯 Execution Rate: {format_percentage(execution_rate)}")
        
        if executed_trades > 0:
            win_rate = profitable_trades / executed_trades
            print(f"   🏆 Win Rate: {format_percentage(win_rate)}")
        
        if accuracy_rate > 0:
            print(f"   📊 Accuracy Rate: {format_percentage(accuracy_rate)}")
        
        print()
    
    # Performance Summary
    print("📈 PERFORMANCE SUMMARY")
    print("-" * 20)
    
    # Calculate overall health score
    health_factors = []
    
    # System health (uptime)
    if uptime_hours >= 1:
        health_factors.append(min(1.0, uptime_hours / 24))  # Good if >24h uptime
    
    # Venue activity (markets and agents)
    if venue_metrics:
        active_markets = venue_metrics.get('venue_stats', {}).get('active_markets', 0)
        active_agents = venue_metrics.get('venue_stats', {}).get('active_agents', 0)
        if active_markets > 0 and active_agents > 0:
            health_factors.append(min(1.0, (active_markets * active_agents) / 50))
    
    # Trading performance
    if trading_metrics and executed_trades > 0:
        win_rate = profitable_trades / executed_trades if executed_trades > 0 else 0
        health_factors.append(win_rate)
    
    if health_factors:
        overall_health = sum(health_factors) / len(health_factors)
        health_status = "🟢 EXCELLENT" if overall_health >= 0.8 else \
                       "🟡 GOOD" if overall_health >= 0.6 else \
                       "🟠 FAIR" if overall_health >= 0.4 else "🔴 POOR"
        
        print(f"   🏥 Overall Health: {health_status} ({overall_health:.1%})")
    else:
        print("   🏥 Overall Health: 🔴 NO DATA")
    
    # Profitability
    if trading_metrics and total_pnl != 0:
        profit_status = "🟢 PROFITABLE" if total_pnl > 0 else "🔴 LOSS"
        print(f"   💰 Profitability: {profit_status}")
    else:
        print("   💰 Profitability: ⚪ NO TRADES YET")
    
    # Recent activity check
    if last_update != 'Unknown':
        try:
            last_update_time = datetime.fromisoformat(last_update.replace('Z', ''))
            time_since_update = (datetime.now() - last_update_time).total_seconds()
            
            if time_since_update < 3600:  # < 1 hour
                activity_status = "🟢 ACTIVE"
            elif time_since_update < 7200:  # < 2 hours  
                activity_status = "🟡 RECENT"
            else:
                activity_status = "🔴 STALE"
            
            print(f"   ⚡ Activity: {activity_status}")
        except:
            print("   ⚡ Activity: ❓ UNKNOWN")
    
    print()
    
    # Quick Actions
    print("🎮 QUICK ACTIONS")
    print("-" * 20)
    print("   📊 Live monitoring: tail -f output/venue.log")
    print("   📈 Detailed metrics: cat output/system_metrics.json")
    print("   💼 Trading data: cat output/prediction_trading_performance.json")
    print("   🚀 Restart venue: python3 launch_venue.py")
    print()
    
    return True

def main():
    """Main status checker"""
    try:
        success = check_venue_status()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Error checking venue status: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)