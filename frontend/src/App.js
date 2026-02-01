import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  Users, 
  Target, 
  DollarSign,
  BarChart3,
  Settings,
  Play,
  Pause,
  RefreshCw
} from 'lucide-react';
import './App.css';

// Import components
import MarketOverview from './components/MarketOverview';
import TradingPerformance from './components/TradingPerformance';
import AgentStatus from './components/AgentStatus';
import PredictionMarkets from './components/PredictionMarkets';
import SystemHealth from './components/SystemHealth';
import LiveFeed from './components/LiveFeed';

function App() {
  const [systemData, setSystemData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  // Load system data
  useEffect(() => {
    loadSystemData();
    const interval = setInterval(loadSystemData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadSystemData = async () => {
    setRefreshing(true);
    try {
      // In a real app, this would be an API call
      // For now, load from demo files
      const response = await fetch('/api/system-status');
      if (response.ok) {
        const data = await response.json();
        setSystemData(data);
        setIsConnected(true);
      } else {
        // Fallback to demo data
        loadDemoData();
      }
    } catch (error) {
      console.log('Loading demo data...');
      loadDemoData();
    }
    setLastUpdate(new Date());
    setRefreshing(false);
  };

  const loadDemoData = () => {
    // Demo data structure
    setSystemData({
      status: 'operational',
      uptime: '4.7h',
      metrics: {
        activeMarkets: 8,
        activeAgents: 15,
        totalPredictions: 147,
        accuracyRate: 0.68,
        totalPnL: 347.85,
        winRate: 0.75,
        executedTrades: 8,
        profitableTrades: 6
      },
      markets: [
        {
          id: 1,
          question: "Will BTC be above $105,000 by March 15, 2025?",
          type: "crypto_price",
          asset: "BTC",
          consensus: 0.74,
          confidence: 0.79,
          agentCount: 5,
          volume: 15420,
          status: "active"
        },
        {
          id: 2,
          question: "Will AI trading agents achieve >70% win rate this month?",
          type: "ai_performance",
          consensus: 0.62,
          confidence: 0.71,
          agentCount: 4,
          volume: 8900,
          status: "active"
        },
        {
          id: 3,
          question: "Will we see a major quantum computing breakthrough in 2025?",
          type: "tech_trends",
          consensus: 0.35,
          confidence: 0.68,
          agentCount: 6,
          volume: 12100,
          status: "active"
        }
      ],
      agents: [
        {
          id: 1,
          name: "crypto_specialist_1",
          type: "Crypto Specialist",
          reputation: 8650,
          accuracy: 0.82,
          trades: 23,
          status: "active",
          specialty: "BTC/ETH"
        },
        {
          id: 2,
          name: "market_maker_2",
          type: "Market Maker",
          reputation: 8020,
          accuracy: 0.76,
          trades: 31,
          status: "active",
          specialty: "Liquidity"
        },
        {
          id: 3,
          name: "trend_analyst",
          type: "Trend Analyst",
          reputation: 6720,
          accuracy: 0.69,
          trades: 18,
          status: "active",
          specialty: "Tech Trends"
        }
      ],
      recentTrades: [
        {
          id: 1,
          asset: "BTC-USDT",
          direction: "long",
          size: 0.021,
          confidence: 0.74,
          status: "executed",
          pnl: 45.20,
          timestamp: new Date(Date.now() - 3600000).toISOString()
        },
        {
          id: 2,
          asset: "ETH-USDT",
          direction: "short", 
          size: 0.018,
          confidence: 0.71,
          status: "pending",
          pnl: 0,
          timestamp: new Date(Date.now() - 1800000).toISOString()
        }
      ]
    });
    setIsConnected(true);
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatPercentage = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(value);
  };

  if (!systemData) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="text-center text-white">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p>Loading Prediction Venue Dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <TrendingUp className="h-8 w-8 text-blue-500 mr-3" />
              <div>
                <h1 className="text-xl font-bold text-white">
                  🏛️ Automated Prediction Trading Venue
                </h1>
                <p className="text-sm text-gray-400">
                  AI-Powered Prediction Market Exchange
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-gray-300">
                <div className={`w-2 h-2 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                {isConnected ? 'Connected' : 'Disconnected'}
              </div>
              
              <button 
                onClick={loadSystemData}
                className={`p-2 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors ${refreshing ? 'animate-spin' : ''}`}
                disabled={refreshing}
              >
                <RefreshCw className="h-4 w-4" />
              </button>
              
              <div className="text-sm text-gray-400">
                Updated: {lastUpdate?.toLocaleTimeString() || 'Never'}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Status Banner */}
        <div className="mb-6">
          <div className="bg-gradient-to-r from-blue-900 to-purple-900 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <Activity className="h-5 w-5 text-green-400 mr-2" />
                <span className="font-medium">System Status: </span>
                <span className="text-green-400 font-bold ml-1">OPERATIONAL</span>
              </div>
              <div className="flex items-center space-x-6 text-sm">
                <div>Uptime: <span className="font-bold">{systemData.uptime}</span></div>
                <div>Markets: <span className="font-bold">{systemData.metrics.activeMarkets}</span></div>
                <div>Agents: <span className="font-bold">{systemData.metrics.activeAgents}</span></div>
                <div>P&L: <span className={`font-bold ${systemData.metrics.totalPnL > 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {formatCurrency(systemData.metrics.totalPnL)}
                </span></div>
              </div>
            </div>
          </div>
        </div>

        {/* Key Metrics Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Win Rate</p>
                <p className="text-2xl font-bold text-green-400">
                  {formatPercentage(systemData.metrics.winRate)}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-400" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Accuracy</p>
                <p className="text-2xl font-bold text-blue-400">
                  {formatPercentage(systemData.metrics.accuracyRate)}
                </p>
              </div>
              <Target className="h-8 w-8 text-blue-400" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total P&L</p>
                <p className="text-2xl font-bold text-green-400">
                  {formatCurrency(systemData.metrics.totalPnL)}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-green-400" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Active Agents</p>
                <p className="text-2xl font-bold text-purple-400">
                  {systemData.metrics.activeAgents}
                </p>
              </div>
              <Users className="h-8 w-8 text-purple-400" />
            </div>
          </div>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            <PredictionMarkets markets={systemData.markets} />
            <TradingPerformance trades={systemData.recentTrades} metrics={systemData.metrics} />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <AgentStatus agents={systemData.agents} />
            <SystemHealth 
              uptime={systemData.uptime}
              status={systemData.status}
              metrics={systemData.metrics}
            />
            <LiveFeed trades={systemData.recentTrades} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;