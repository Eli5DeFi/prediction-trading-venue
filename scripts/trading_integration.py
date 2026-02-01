#!/usr/bin/env python3
"""
⚡ PREDICTION VENUE → CRYPTO TRADING INTEGRATION

Connects the automated prediction trading venue with our existing crypto trading system.
Converts prediction consensus into executable trading signals for our trading agents.

Author: Ether (Crypto Trading Swarm Agent) 
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

# Add crypto-trading skill to path
sys.path.append('/Users/eli5defi/clawd/skills/crypto-trading')

# Import our existing trading components
try:
    from scripts.trading_engine import TradingEngine
    from scripts.risk_manager import RiskManager
    from scripts.position_manager import PositionManager
    TRADING_SYSTEM_AVAILABLE = True
except ImportError:
    TRADING_SYSTEM_AVAILABLE = False
    logging.warning("⚠️ Crypto trading system not available - using mock implementation")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PredictionTradingBridge:
    """
    🌉 Bridge between prediction venue and trading execution
    
    Converts prediction market consensus into actionable trading signals
    that can be executed by our crypto trading system.
    """
    
    def __init__(self, venue_config_path: str = "config/venue_config.json"):
        self.venue_config = self.load_config(venue_config_path)
        self.trading_config = self.load_trading_config()
        
        # Initialize trading system components
        if TRADING_SYSTEM_AVAILABLE:
            self.trading_engine = TradingEngine(self.trading_config)
            self.risk_manager = RiskManager(self.trading_config)
            self.position_manager = PositionManager(self.trading_config)
        else:
            self.trading_engine = MockTradingEngine()
            self.risk_manager = MockRiskManager()
            self.position_manager = MockPositionManager()
        
        # Track prediction-driven trades
        self.prediction_trades = []
        self.performance_metrics = {
            'total_signals': 0,
            'executed_trades': 0,
            'profitable_trades': 0,
            'total_pnl': 0.0,
            'accuracy_rate': 0.0,
            'avg_hold_time': 0.0
        }
        
        logger.info("🌉 Prediction Trading Bridge initialized")

    def load_config(self, config_path: str) -> Dict:
        """Load venue configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"❌ Config file not found: {config_path}")
            return {}

    def load_trading_config(self) -> Dict:
        """Load crypto trading system configuration"""
        trading_config_path = "/Users/eli5defi/clawd/skills/crypto-trading/config/trading_config.json"
        try:
            with open(trading_config_path, 'r') as f:
                config = json.load(f)
            logger.info("✅ Loaded crypto trading system config")
            return config
        except FileNotFoundError:
            logger.warning("⚠️ Using default trading config")
            return self.get_default_trading_config()

    def get_default_trading_config(self) -> Dict:
        """Default trading configuration for prediction integration"""
        return {
            "risk_management": {
                "max_position_size": 0.02,
                "stop_loss": 0.015,
                "take_profit": 0.03
            },
            "execution": {
                "order_type": "market",
                "slippage_tolerance": 0.005
            },
            "portfolio": {
                "max_positions": 5,
                "correlation_limit": 0.7
            }
        }

    async def process_prediction_signals(self, consensus_data: List[Dict]) -> List[Dict]:
        """
        🔄 Main processing function: Convert prediction consensus to trading signals
        
        Args:
            consensus_data: List of market consensus from prediction venue
            
        Returns:
            List of executable trading signals
        """
        logger.info(f"🔄 Processing {len(consensus_data)} prediction signals...")
        
        trading_signals = []
        
        for consensus in consensus_data:
            try:
                # Validate consensus data
                if not self.validate_consensus(consensus):
                    continue
                
                # Convert to trading signal
                signal = await self.create_trading_signal(consensus)
                if signal:
                    trading_signals.append(signal)
                    
            except Exception as e:
                logger.error(f"❌ Failed to process consensus for {consensus.get('asset', 'unknown')}: {e}")
        
        logger.info(f"✅ Generated {len(trading_signals)} trading signals from predictions")
        return trading_signals

    def validate_consensus(self, consensus: Dict) -> bool:
        """Validate prediction consensus data"""
        required_fields = ['asset', 'signal_strength', 'confidence', 'agent_count']
        
        for field in required_fields:
            if field not in consensus:
                logger.warning(f"⚠️ Missing field {field} in consensus data")
                return False
        
        # Check confidence threshold
        min_confidence = self.venue_config.get('trading', {}).get('execution_threshold', 0.7)
        if consensus['confidence'] < min_confidence:
            logger.debug(f"🚫 Consensus confidence {consensus['confidence']:.2%} below threshold {min_confidence:.2%}")
            return False
        
        # Check minimum agents
        min_agents = self.venue_config.get('agents', {}).get('min_agents_per_market', 3)
        if consensus['agent_count'] < min_agents:
            logger.debug(f"🚫 Insufficient agents: {consensus['agent_count']} < {min_agents}")
            return False
        
        return True

    async def create_trading_signal(self, consensus: Dict) -> Optional[Dict]:
        """Create executable trading signal from consensus data"""
        asset = consensus['asset']
        signal_strength = consensus['signal_strength']  # -1.0 to 1.0
        confidence = consensus['confidence']
        
        # Map asset to trading pair
        trading_pair = self.map_asset_to_pair(asset)
        if not trading_pair:
            logger.warning(f"⚠️ No trading pair found for asset: {asset}")
            return None
        
        # Determine direction and size
        direction = 'long' if signal_strength > 0 else 'short'
        position_size = self.calculate_position_size(signal_strength, confidence)
        
        # Risk assessment
        risk_assessment = await self.assess_trade_risk(trading_pair, direction, position_size)
        if not risk_assessment['approved']:
            logger.warning(f"🚫 Trade rejected by risk management: {risk_assessment['reason']}")
            return None
        
        # Create signal
        signal = {
            'id': f"pred_{asset}_{int(datetime.now().timestamp())}",
            'source': 'prediction_venue',
            'timestamp': datetime.now().isoformat(),
            'trading_pair': trading_pair,
            'direction': direction,
            'size': position_size,
            'confidence': confidence,
            'signal_strength': abs(signal_strength),
            'entry_type': 'market',
            'stop_loss': risk_assessment['stop_loss'],
            'take_profit': risk_assessment['take_profit'],
            'reasoning': f"Prediction consensus: {signal_strength:.2%} signal with {confidence:.1%} confidence from {consensus['agent_count']} agents",
            'prediction_data': consensus,
            'expiry': (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        logger.info(f"✅ Created trading signal: {direction} {trading_pair} (size: {position_size:.1%})")
        return signal

    def map_asset_to_pair(self, asset: str) -> Optional[str]:
        """Map prediction asset to trading pair"""
        asset_mapping = {
            'BTC': 'BTC-USDT',
            'ETH': 'ETH-USDT', 
            'SOL': 'SOL-USDT',
            'ARB': 'ARB-USDT',
            'AVAX': 'AVAX-USDT'
        }
        return asset_mapping.get(asset.upper())

    def calculate_position_size(self, signal_strength: float, confidence: float) -> float:
        """Calculate position size based on signal strength and confidence"""
        base_size = self.venue_config.get('trading', {}).get('max_position_size', 0.025)
        
        # Scale by signal strength and confidence
        strength_factor = abs(signal_strength)  # 0.0 to 1.0
        confidence_factor = confidence           # 0.0 to 1.0
        
        # Position sizing formula: base * strength * confidence
        position_size = base_size * strength_factor * confidence_factor
        
        # Apply minimum and maximum bounds
        min_size = base_size * 0.25  # 25% of base minimum
        max_size = base_size * 1.0   # 100% of base maximum
        
        return max(min_size, min(position_size, max_size))

    async def assess_trade_risk(self, trading_pair: str, direction: str, size: float) -> Dict:
        """Assess trade risk using our risk management system"""
        try:
            # Check portfolio exposure
            current_exposure = await self.get_current_exposure(trading_pair)
            max_exposure = self.trading_config.get('portfolio', {}).get('max_positions', 5)
            
            if current_exposure >= max_exposure:
                return {
                    'approved': False,
                    'reason': f"Maximum exposure reached: {current_exposure}/{max_exposure}"
                }
            
            # Check position limits
            max_position = self.trading_config.get('risk_management', {}).get('max_position_size', 0.02)
            if size > max_position:
                return {
                    'approved': False,
                    'reason': f"Position size {size:.2%} exceeds limit {max_position:.2%}"
                }
            
            # Calculate stop loss and take profit
            stop_loss_pct = self.trading_config.get('risk_management', {}).get('stop_loss', 0.015)
            take_profit_pct = self.trading_config.get('risk_management', {}).get('take_profit', 0.03)
            
            return {
                'approved': True,
                'reason': 'Trade approved',
                'stop_loss': stop_loss_pct,
                'take_profit': take_profit_pct
            }
            
        except Exception as e:
            logger.error(f"❌ Risk assessment failed: {e}")
            return {
                'approved': False,
                'reason': f"Risk assessment error: {e}"
            }

    async def execute_prediction_trades(self, trading_signals: List[Dict]) -> Dict:
        """Execute trading signals and track performance"""
        logger.info(f"💼 Executing {len(trading_signals)} prediction-based trades...")
        
        execution_results = {
            'successful': 0,
            'failed': 0,
            'total_volume': 0.0,
            'trades': []
        }
        
        for signal in trading_signals:
            try:
                # Execute trade using our trading engine
                result = await self.execute_single_trade(signal)
                
                if result['success']:
                    execution_results['successful'] += 1
                    execution_results['total_volume'] += result.get('volume', 0)
                    execution_results['trades'].append(result)
                    
                    # Track prediction trade
                    self.track_prediction_trade(signal, result)
                    
                    logger.info(f"✅ Executed: {signal['direction']} {signal['trading_pair']}")
                else:
                    execution_results['failed'] += 1
                    logger.warning(f"❌ Failed: {signal['trading_pair']} - {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                execution_results['failed'] += 1
                logger.error(f"❌ Execution error for {signal['trading_pair']}: {e}")
        
        # Update performance metrics
        self.update_performance_metrics(execution_results)
        
        logger.info(f"✅ Execution complete: {execution_results['successful']} successful, {execution_results['failed']} failed")
        return execution_results

    async def execute_single_trade(self, signal: Dict) -> Dict:
        """Execute a single trading signal"""
        try:
            # Prepare trade parameters
            trade_params = {
                'symbol': signal['trading_pair'],
                'side': signal['direction'],
                'size': signal['size'],
                'order_type': signal.get('entry_type', 'market'),
                'stop_loss': signal.get('stop_loss'),
                'take_profit': signal.get('take_profit'),
                'source': 'prediction_venue'
            }
            
            # Execute through trading engine
            result = await self.trading_engine.execute_trade(trade_params)
            
            return {
                'success': True,
                'trade_id': result.get('trade_id'),
                'executed_price': result.get('price'),
                'volume': result.get('volume', 0),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def track_prediction_trade(self, signal: Dict, execution_result: Dict):
        """Track prediction-based trade for performance analysis"""
        trade_record = {
            'id': signal['id'],
            'prediction_data': signal['prediction_data'],
            'execution_data': execution_result,
            'opened_at': datetime.now(),
            'status': 'open',
            'pnl': 0.0
        }
        
        self.prediction_trades.append(trade_record)

    def update_performance_metrics(self, execution_results: Dict):
        """Update overall performance metrics"""
        self.performance_metrics['total_signals'] += len(execution_results.get('trades', []))
        self.performance_metrics['executed_trades'] += execution_results['successful']
        
        # Calculate accuracy rate
        if self.performance_metrics['total_signals'] > 0:
            self.performance_metrics['accuracy_rate'] = (
                self.performance_metrics['executed_trades'] / 
                self.performance_metrics['total_signals']
            )

    async def get_current_exposure(self, trading_pair: str) -> int:
        """Get current exposure for trading pair (mock implementation)"""
        return 0  # In real implementation, query position manager

    async def monitor_prediction_trades(self):
        """Monitor open prediction trades and update performance"""
        logger.info("📊 Monitoring prediction trade performance...")
        
        for trade in self.prediction_trades:
            if trade['status'] == 'open':
                # Check if trade should be closed
                current_pnl = await self.calculate_trade_pnl(trade)
                trade['pnl'] = current_pnl
                
                # Update if profitable
                if current_pnl > 0:
                    self.performance_metrics['profitable_trades'] += 1
                    trade['status'] = 'profitable'
        
        # Save updated metrics
        await self.save_performance_metrics()

    async def calculate_trade_pnl(self, trade: Dict) -> float:
        """Calculate current P&L for a trade (mock implementation)"""
        # In real implementation, get current price and calculate P&L
        return 0.0

    async def save_performance_metrics(self):
        """Save performance metrics to file"""
        metrics_file = Path("output/prediction_trading_performance.json")
        metrics_file.parent.mkdir(exist_ok=True)
        
        metrics_data = {
            'metrics': self.performance_metrics,
            'last_updated': datetime.now().isoformat(),
            'active_trades': len([t for t in self.prediction_trades if t['status'] == 'open'])
        }
        
        with open(metrics_file, 'w') as f:
            json.dump(metrics_data, f, indent=2, default=str)

# Mock implementations for when trading system is not available

class MockTradingEngine:
    async def execute_trade(self, trade_params: Dict) -> Dict:
        logger.info(f"🎭 MOCK EXECUTION: {trade_params['side']} {trade_params['symbol']}")
        return {
            'trade_id': f"mock_{int(datetime.now().timestamp())}",
            'price': 100.0,
            'volume': trade_params['size'] * 1000
        }

class MockRiskManager:
    async def assess_risk(self, trade_params: Dict) -> Dict:
        return {'approved': True, 'reason': 'Mock approval'}

class MockPositionManager:
    async def get_positions(self) -> List:
        return []

async def main():
    """🌉 Main integration runner"""
    bridge = PredictionTradingBridge()
    
    logger.info("🌉 Starting Prediction Trading Bridge...")
    
    # Example: Process some mock consensus data
    mock_consensus = [
        {
            'asset': 'BTC',
            'signal_strength': 0.75,
            'confidence': 0.82,
            'agent_count': 5,
            'prediction_data': {
                'question': 'Will BTC be above $100k by March 2025?',
                'consensus': 'bullish'
            }
        },
        {
            'asset': 'ETH', 
            'signal_strength': -0.45,
            'confidence': 0.73,
            'agent_count': 4,
            'prediction_data': {
                'question': 'Will ETH outperform BTC this month?',
                'consensus': 'bearish'
            }
        }
    ]
    
    # Process signals
    trading_signals = await bridge.process_prediction_signals(mock_consensus)
    
    # Execute trades
    if trading_signals:
        results = await bridge.execute_prediction_trades(trading_signals)
        logger.info(f"📊 Execution summary: {results}")
    
    # Monitor performance
    await bridge.monitor_prediction_trades()
    
    logger.info("✅ Bridge cycle completed")

if __name__ == "__main__":
    asyncio.run(main())