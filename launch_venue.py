#!/usr/bin/env python3
"""
🚀 AUTOMATED PREDICTION TRADING VENUE LAUNCHER

One-command launcher for the complete prediction trading ecosystem.
Starts all components and monitors the entire system.

Author: Ether (Crypto Trading Swarm Agent)
"""

import asyncio
import json
import logging
import signal
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Import our venue components
from scripts.venue_manager import AutomatedPredictionVenue
from scripts.trading_integration import PredictionTradingBridge

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('output/venue.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class VenueLauncher:
    """🚀 Complete venue system launcher and coordinator"""
    
    def __init__(self):
        self.venue = None
        self.trading_bridge = None
        self.running = False
        self.startup_time = datetime.now()
        
        # Create output directory
        Path("output").mkdir(exist_ok=True)
        
        logger.info("🚀 Venue Launcher initialized")

    async def start_venue_system(self):
        """Start the complete prediction trading venue system"""
        logger.info("🏛️ STARTING AUTOMATED PREDICTION TRADING VENUE SYSTEM")
        logger.info("=" * 60)
        
        try:
            # 1. Initialize venue manager
            logger.info("🏭 Initializing prediction market venue...")
            self.venue = AutomatedPredictionVenue()
            
            # 2. Initialize trading bridge
            logger.info("🌉 Initializing trading integration...")
            self.trading_bridge = PredictionTradingBridge()
            
            # 3. Set up signal handlers for graceful shutdown
            self.setup_signal_handlers()
            
            # 4. Start monitoring dashboard (optional)
            await self.start_dashboard()
            
            # 5. Display system status
            await self.display_startup_status()
            
            logger.info("✅ VENUE SYSTEM FULLY OPERATIONAL")
            logger.info("=" * 60)
            
            # 6. Main operation loop
            self.running = True
            await self.run_main_loop()
            
        except Exception as e:
            logger.error(f"❌ Failed to start venue system: {e}")
            raise

    async def run_main_loop(self):
        """Main operational loop coordinating all components"""
        cycle_count = 0
        
        while self.running:
            cycle_start = datetime.now()
            cycle_count += 1
            
            logger.info(f"🔄 Starting venue cycle #{cycle_count}")
            
            try:
                # 1. Run venue prediction cycle
                logger.info("🏛️ Running prediction market cycle...")
                await self.venue.run_venue_cycle()
                
                # 2. Get prediction consensus
                logger.info("📊 Gathering prediction consensus...")
                consensus_data = await self.get_consensus_data()
                
                # 3. Process trading signals
                if consensus_data:
                    logger.info(f"⚡ Processing {len(consensus_data)} consensus signals...")
                    trading_signals = await self.trading_bridge.process_prediction_signals(consensus_data)
                    
                    # 4. Execute trades
                    if trading_signals:
                        logger.info(f"💼 Executing {len(trading_signals)} trading signals...")
                        execution_results = await self.trading_bridge.execute_prediction_trades(trading_signals)
                        await self.log_execution_results(execution_results)
                
                # 5. Monitor active trades
                await self.trading_bridge.monitor_prediction_trades()
                
                # 6. Update system metrics
                await self.update_system_metrics(cycle_count)
                
                cycle_duration = (datetime.now() - cycle_start).total_seconds()
                logger.info(f"✅ Cycle #{cycle_count} completed in {cycle_duration:.1f}s")
                
                # Wait for next cycle (30 minutes)
                await asyncio.sleep(30 * 60)
                
            except KeyboardInterrupt:
                logger.info("⏹️ Received shutdown signal...")
                break
            except Exception as e:
                logger.error(f"❌ Cycle #{cycle_count} failed: {e}")
                logger.info("⏳ Waiting 60s before retry...")
                await asyncio.sleep(60)

    async def get_consensus_data(self) -> List[Dict]:
        """Extract consensus data from venue for trading bridge"""
        # This would normally get data from the venue
        # For now, return empty list (venue will populate this)
        return []

    async def log_execution_results(self, results: Dict):
        """Log trading execution results"""
        logger.info(f"📈 Execution Results:")
        logger.info(f"   ✅ Successful: {results['successful']}")
        logger.info(f"   ❌ Failed: {results['failed']}")
        logger.info(f"   💰 Volume: ${results['total_volume']:,.2f}")

    async def update_system_metrics(self, cycle_count: int):
        """Update and save system-wide metrics"""
        uptime = datetime.now() - self.startup_time
        
        metrics = {
            'system_status': 'operational',
            'uptime_hours': uptime.total_seconds() / 3600,
            'cycles_completed': cycle_count,
            'last_update': datetime.now().isoformat(),
            'venue_stats': getattr(self.venue, 'venue_stats', {}),
            'trading_performance': getattr(self.trading_bridge, 'performance_metrics', {})
        }
        
        # Save system metrics
        with open('output/system_metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2, default=str)

    async def start_dashboard(self):
        """Start monitoring dashboard (placeholder)"""
        logger.info("📊 Dashboard would start at http://localhost:8080")
        logger.info("   (Dashboard implementation coming soon)")

    async def display_startup_status(self):
        """Display system startup status"""
        status = f"""
🏛️ AUTOMATED PREDICTION TRADING VENUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 System Status: OPERATIONAL
⏰ Started: {self.startup_time.strftime('%Y-%m-%d %H:%M:%S')}
🏭 Venue Manager: ✅ Active
🌉 Trading Bridge: ✅ Active
📊 Dashboard: 🔄 Starting...

🎯 Target Performance:
   • 3-5% profit per trade
   • 55-65% win rate
   • <2% risk per position

🤖 AI Agent Network:
   • Prediction specialists
   • Market makers
   • Arbitrage hunters
   • Consensus builders

💱 Supported Assets:
   • BTC-USDT, ETH-USDT, SOL-USDT
   • ARB-USDT, AVAX-USDT

📈 Revenue Streams:
   • Market making fees (0.2%)
   • Trading commissions (30%)
   • Prediction consensus data
   • Agent tokenization

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 VENUE IS NOW OPERATIONAL - MONITORING MARKETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        logger.info(status)

    def setup_signal_handlers(self):
        """Set up graceful shutdown signal handlers"""
        def signal_handler(signum, frame):
            logger.info(f"📯 Received signal {signum}")
            self.shutdown()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def shutdown(self):
        """Graceful shutdown of venue system"""
        logger.info("⏹️ SHUTTING DOWN VENUE SYSTEM...")
        self.running = False
        
        # Save final metrics
        final_metrics = {
            'shutdown_time': datetime.now().isoformat(),
            'total_uptime': (datetime.now() - self.startup_time).total_seconds(),
            'shutdown_reason': 'user_requested'
        }
        
        with open('output/shutdown_metrics.json', 'w') as f:
            json.dump(final_metrics, f, indent=2, default=str)
        
        logger.info("✅ Venue system shutdown complete")

async def main():
    """🚀 Main launcher entry point"""
    launcher = VenueLauncher()
    
    print("🏛️ AUTOMATED PREDICTION TRADING VENUE")
    print("====================================")
    print("Starting complete prediction trading ecosystem...")
    print()
    
    try:
        await launcher.start_venue_system()
    except KeyboardInterrupt:
        logger.info("⏹️ Shutdown requested by user")
    except Exception as e:
        logger.error(f"❌ System error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    # Ensure we're in the right directory
    venue_dir = Path(__file__).parent
    if venue_dir.name != "prediction-trading-venue":
        print("❌ Please run from the prediction-trading-venue directory")
        sys.exit(1)
    
    # Run the launcher
    exit_code = asyncio.run(main())
    sys.exit(exit_code)