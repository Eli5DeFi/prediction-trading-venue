import React, { useState } from 'react';
import { TrendingUp, TrendingDown, DollarSign, Target, Clock, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const TradingPerformance = ({ trades, metrics }) => {
  const [activeTab, setActiveTab] = useState('overview');

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  const formatPercentage = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(value);
  };

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffInMinutes = Math.floor((now - time) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  // Mock historical data for charts
  const performanceData = [
    { time: '00:00', pnl: 0, trades: 0 },
    { time: '06:00', pnl: 45.20, trades: 2 },
    { time: '12:00', pnl: 123.50, trades: 5 },
    { time: '18:00', pnl: 278.90, trades: 7 },
    { time: '24:00', pnl: 347.85, trades: 8 }
  ];

  const winRateData = [
    { period: 'Week 1', winRate: 0.60, trades: 10 },
    { period: 'Week 2', winRate: 0.70, trades: 12 },
    { period: 'Week 3', winRate: 0.65, trades: 8 },
    { period: 'Week 4', winRate: 0.75, trades: 15 }
  ];

  const getTradeStatusColor = (status) => {
    switch (status) {
      case 'executed': return 'text-green-400 bg-green-400/10';
      case 'pending': return 'text-yellow-400 bg-yellow-400/10';
      case 'failed': return 'text-red-400 bg-red-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getDirectionIcon = (direction) => {
    return direction === 'long' ? ArrowUpRight : ArrowDownRight;
  };

  const getDirectionColor = (direction) => {
    return direction === 'long' ? 'text-green-400' : 'text-red-400';
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Target },
    { id: 'trades', label: 'Recent Trades', icon: DollarSign },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp }
  ];

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-white flex items-center">
            💼 Trading Performance
          </h2>
          
          {/* Tab Navigation */}
          <div className="flex bg-gray-700 rounded-lg p-1">
            {tabs.map((tab) => {
              const TabIcon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors flex items-center ${
                    activeTab === tab.id
                      ? 'bg-blue-600 text-white'
                      : 'text-gray-300 hover:text-white hover:bg-gray-600'
                  }`}
                >
                  <TabIcon className="h-4 w-4 mr-1.5" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Key Metrics Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-xs">Total P&L</p>
                    <p className="text-lg font-bold text-green-400">
                      {formatCurrency(metrics?.totalPnL || 0)}
                    </p>
                  </div>
                  <DollarSign className="h-5 w-5 text-green-400" />
                </div>
              </div>

              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-xs">Win Rate</p>
                    <p className="text-lg font-bold text-blue-400">
                      {formatPercentage(metrics?.winRate || 0)}
                    </p>
                  </div>
                  <Target className="h-5 w-5 text-blue-400" />
                </div>
              </div>

              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-xs">Executed</p>
                    <p className="text-lg font-bold text-white">
                      {metrics?.executedTrades || 0}
                    </p>
                  </div>
                  <TrendingUp className="h-5 w-5 text-gray-400" />
                </div>
              </div>

              <div className="bg-gray-700/50 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-xs">Profitable</p>
                    <p className="text-lg font-bold text-green-400">
                      {metrics?.profitableTrades || 0}
                    </p>
                  </div>
                  <TrendingUp className="h-5 w-5 text-green-400" />
                </div>
              </div>
            </div>

            {/* P&L Chart */}
            <div>
              <h3 className="text-lg font-medium text-white mb-4">Daily P&L Progression</h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis 
                      dataKey="time" 
                      stroke="#9CA3AF"
                      fontSize={12}
                    />
                    <YAxis 
                      stroke="#9CA3AF"
                      fontSize={12}
                      tickFormatter={(value) => `$${value}`}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }}
                      labelStyle={{ color: '#F3F4F6' }}
                      formatter={(value, name) => [
                        name === 'pnl' ? formatCurrency(value) : value,
                        name === 'pnl' ? 'P&L' : 'Trades'
                      ]}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="pnl" 
                      stroke="#10B981" 
                      strokeWidth={2}
                      dot={{ fill: '#10B981', strokeWidth: 2, r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Recent Trades Tab */}
        {activeTab === 'trades' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-medium text-white">Recent Trades</h3>
              <span className="text-sm text-gray-400">
                Last {trades?.length || 0} trades
              </span>
            </div>

            <div className="space-y-3">
              {trades?.map((trade) => {
                const DirectionIcon = getDirectionIcon(trade.direction);
                const directionColor = getDirectionColor(trade.direction);
                
                return (
                  <div 
                    key={trade.id}
                    className="bg-gray-700/30 rounded-lg p-4 border border-gray-600"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded-lg ${directionColor.replace('text-', 'bg-').replace('400', '400/20')}`}>
                          <DirectionIcon className={`h-4 w-4 ${directionColor}`} />
                        </div>
                        
                        <div>
                          <div className="flex items-center space-x-2">
                            <span className="font-medium text-white font-mono">
                              {trade.asset}
                            </span>
                            <span className={`text-sm font-medium ${directionColor}`}>
                              {trade.direction.toUpperCase()}
                            </span>
                          </div>
                          <div className="flex items-center space-x-4 text-sm text-gray-400 mt-1">
                            <span>Size: {formatPercentage(trade.size)}</span>
                            <span>Confidence: {formatPercentage(trade.confidence)}</span>
                            <span className="flex items-center">
                              <Clock className="h-3 w-3 mr-1" />
                              {formatTimeAgo(trade.timestamp)}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="text-right">
                        <div className={`inline-flex px-2 py-1 rounded-full text-xs font-medium ${getTradeStatusColor(trade.status)}`}>
                          {trade.status.toUpperCase()}
                        </div>
                        {trade.pnl !== 0 && (
                          <div className={`text-sm font-bold mt-1 ${trade.pnl > 0 ? 'text-green-400' : 'text-red-400'}`}>
                            {trade.pnl > 0 ? '+' : ''}{formatCurrency(trade.pnl)}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {!trades || trades.length === 0 && (
              <div className="text-center py-8 text-gray-400">
                <DollarSign className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>No recent trades</p>
                <p className="text-sm">Trades will appear as predictions are executed</p>
              </div>
            )}
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-white mb-4">Win Rate Trends</h3>
              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={winRateData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis 
                      dataKey="period" 
                      stroke="#9CA3AF"
                      fontSize={12}
                    />
                    <YAxis 
                      stroke="#9CA3AF"
                      fontSize={12}
                      tickFormatter={(value) => formatPercentage(value)}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }}
                      labelStyle={{ color: '#F3F4F6' }}
                      formatter={(value, name) => [
                        name === 'winRate' ? formatPercentage(value) : value,
                        name === 'winRate' ? 'Win Rate' : 'Trades'
                      ]}
                    />
                    <Bar 
                      dataKey="winRate" 
                      fill="#3B82F6"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-300 mb-3">Performance Stats</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Best Trade:</span>
                    <span className="text-green-400 font-medium">+$89.50</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Worst Trade:</span>
                    <span className="text-red-400 font-medium">-$23.10</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Avg Trade:</span>
                    <span className="text-white font-medium">$43.48</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Avg Hold Time:</span>
                    <span className="text-white font-medium">18.4h</span>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="font-medium text-gray-300 mb-3">Risk Metrics</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Max Drawdown:</span>
                    <span className="text-red-400 font-medium">-2.1%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Sharpe Ratio:</span>
                    <span className="text-white font-medium">1.45</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Risk per Trade:</span>
                    <span className="text-white font-medium">1.8%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">R:R Ratio:</span>
                    <span className="text-green-400 font-medium">2.1:1</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TradingPerformance;