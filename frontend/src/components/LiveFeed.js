import React, { useState, useEffect } from 'react';
import { Activity, TrendingUp, TrendingDown, Users, DollarSign, Target, Zap, Clock } from 'lucide-react';

const LiveFeed = ({ trades }) => {
  const [feedItems, setFeedItems] = useState([]);

  useEffect(() => {
    // Generate live feed items based on trades and system events
    const generateFeedItems = () => {
      const items = [];
      const now = new Date();

      // Add recent trades to feed
      if (trades) {
        trades.forEach((trade, index) => {
          items.push({
            id: `trade-${trade.id}`,
            type: 'trade',
            timestamp: new Date(trade.timestamp),
            icon: trade.direction === 'long' ? TrendingUp : TrendingDown,
            color: trade.direction === 'long' ? 'text-green-400' : 'text-red-400',
            title: `${trade.direction.toUpperCase()} ${trade.asset}`,
            description: `Size: ${(trade.size * 100).toFixed(1)}% • Confidence: ${(trade.confidence * 100).toFixed(0)}%`,
            status: trade.status
          });
        });
      }

      // Add system events
      const systemEvents = [
        {
          id: 'market-creation-1',
          type: 'market',
          timestamp: new Date(now.getTime() - 3 * 60 * 1000), // 3 minutes ago
          icon: Target,
          color: 'text-blue-400',
          title: 'New Prediction Market Created',
          description: 'BTC price prediction market with 5 agents deployed',
          status: 'completed'
        },
        {
          id: 'consensus-1',
          type: 'consensus',
          timestamp: new Date(now.getTime() - 8 * 60 * 1000), // 8 minutes ago
          icon: Users,
          color: 'text-purple-400',
          title: 'Consensus Reached',
          description: 'ETH market: 74% confidence, executable signal generated',
          status: 'executed'
        },
        {
          id: 'agent-update-1',
          type: 'agent',
          timestamp: new Date(now.getTime() - 12 * 60 * 1000), // 12 minutes ago
          icon: Zap,
          color: 'text-yellow-400',
          title: 'Agent Reputation Updated',
          description: 'crypto_specialist_1 gained +150 reputation points',
          status: 'completed'
        },
        {
          id: 'system-cycle-1',
          type: 'system',
          timestamp: new Date(now.getTime() - 35 * 60 * 1000), // 35 minutes ago
          icon: Activity,
          color: 'text-green-400',
          title: 'Venue Cycle Completed',
          description: 'Market scan, agent coordination, and signal generation cycle #9',
          status: 'completed'
        }
      ];

      items.push(...systemEvents);

      // Sort by timestamp (most recent first)
      return items.sort((a, b) => b.timestamp - a.timestamp);
    };

    setFeedItems(generateFeedItems());
  }, [trades]);

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now - timestamp) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'executed':
      case 'completed':
        return 'text-green-400 bg-green-400/10';
      case 'pending':
        return 'text-yellow-400 bg-yellow-400/10';
      case 'failed':
        return 'text-red-400 bg-red-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'trade':
        return 'bg-blue-500';
      case 'market':
        return 'bg-purple-500';
      case 'consensus':
        return 'bg-green-500';
      case 'agent':
        return 'bg-yellow-500';
      case 'system':
        return 'bg-gray-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-white flex items-center">
            📡 Live Activity Feed
          </h2>
          <div className="flex items-center text-sm text-gray-400">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse" />
            Live
          </div>
        </div>
      </div>

      <div className="p-6">
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {feedItems.map((item) => {
            const ItemIcon = item.icon;
            
            return (
              <div 
                key={item.id}
                className="flex items-start space-x-3 p-3 bg-gray-700/20 rounded-lg border border-gray-600 hover:bg-gray-700/40 transition-colors"
              >
                {/* Timeline indicator */}
                <div className="flex flex-col items-center">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${getTypeColor(item.type)}`}>
                    <ItemIcon className="h-4 w-4 text-white" />
                  </div>
                  <div className="w-0.5 h-6 bg-gray-600 mt-2" />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="text-sm font-medium text-white truncate">
                      {item.title}
                    </h3>
                    <div className="flex items-center space-x-2 ml-2">
                      <span className="text-xs text-gray-400 flex items-center">
                        <Clock className="h-3 w-3 mr-1" />
                        {formatTimeAgo(item.timestamp)}
                      </span>
                      <div className={`px-2 py-0.5 rounded-full text-xs font-medium ${getStatusColor(item.status)}`}>
                        {item.status}
                      </div>
                    </div>
                  </div>
                  
                  <p className="text-sm text-gray-400 leading-relaxed">
                    {item.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {feedItems.length === 0 && (
          <div className="text-center py-8 text-gray-400">
            <Activity className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>No recent activity</p>
            <p className="text-sm">System events will appear here as they occur</p>
          </div>
        )}

        {/* Feed Controls */}
        <div className="mt-4 pt-4 border-t border-gray-600">
          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center space-x-4 text-gray-400">
              <span>📊 {feedItems.filter(item => item.type === 'market').length} Markets</span>
              <span>💼 {feedItems.filter(item => item.type === 'trade').length} Trades</span>
              <span>🤖 {feedItems.filter(item => item.type === 'agent').length} Agent Updates</span>
            </div>
            <button className="text-blue-400 hover:text-blue-300 font-medium">
              View All Activity
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveFeed;