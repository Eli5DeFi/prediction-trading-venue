import React, { useState } from 'react';
import { Users, Activity, Target, TrendingUp, Star, BarChart3 } from 'lucide-react';

const AgentStatus = ({ agents }) => {
  const [selectedAgent, setSelectedAgent] = useState(null);

  const formatPercentage = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 0,
      maximumFractionDigits: 1
    }).format(value);
  };

  const getAgentTypeIcon = (type) => {
    switch (type.toLowerCase()) {
      case 'crypto specialist':
        return '₿';
      case 'market maker':
        return '💱';
      case 'trend analyst':
        return '📈';
      case 'arbitrage hunter':
        return '⚡';
      default:
        return '🤖';
    }
  };

  const getAgentTypeColor = (type) => {
    switch (type.toLowerCase()) {
      case 'crypto specialist':
        return 'text-orange-400 bg-orange-400/10 border-orange-400/20';
      case 'market maker':
        return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'trend analyst':
        return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      case 'arbitrage hunter':
        return 'text-green-400 bg-green-400/10 border-green-400/20';
      default:
        return 'text-gray-400 bg-gray-400/10 border-gray-400/20';
    }
  };

  const getReputationColor = (reputation) => {
    if (reputation >= 8000) return 'text-green-400';
    if (reputation >= 6000) return 'text-yellow-400';
    if (reputation >= 4000) return 'text-orange-400';
    return 'text-red-400';
  };

  const getAccuracyColor = (accuracy) => {
    if (accuracy >= 0.75) return 'text-green-400';
    if (accuracy >= 0.65) return 'text-yellow-400';
    if (accuracy >= 0.55) return 'text-orange-400';
    return 'text-red-400';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'text-green-400 bg-green-400/10';
      case 'idle':
        return 'text-yellow-400 bg-yellow-400/10';
      case 'offline':
        return 'text-red-400 bg-red-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getReputationLevel = (reputation) => {
    if (reputation >= 9000) return { level: 'Elite', icon: Star };
    if (reputation >= 7500) return { level: 'Expert', icon: TrendingUp };
    if (reputation >= 6000) return { level: 'Advanced', icon: BarChart3 };
    if (reputation >= 4000) return { level: 'Intermediate', icon: Activity };
    return { level: 'Beginner', icon: Users };
  };

  // Calculate summary stats
  const totalAgents = agents?.length || 0;
  const activeAgents = agents?.filter(agent => agent.status === 'active').length || 0;
  const averageAccuracy = agents?.length ? 
    agents.reduce((sum, agent) => sum + agent.accuracy, 0) / agents.length : 0;
  const averageReputation = agents?.length ?
    agents.reduce((sum, agent) => sum + agent.reputation, 0) / agents.length : 0;

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          🤖 AI Agent Network
          <span className="ml-3 text-sm font-normal text-gray-400">
            {activeAgents}/{totalAgents} Active
          </span>
        </h2>
      </div>

      <div className="p-6">
        {/* Summary Stats */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-700/30 rounded-lg p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-xs">Avg Accuracy</p>
                <p className={`text-sm font-bold ${getAccuracyColor(averageAccuracy)}`}>
                  {formatPercentage(averageAccuracy)}
                </p>
              </div>
              <Target className="h-4 w-4 text-gray-400" />
            </div>
          </div>

          <div className="bg-gray-700/30 rounded-lg p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-xs">Avg Reputation</p>
                <p className={`text-sm font-bold ${getReputationColor(averageReputation)}`}>
                  {Math.round(averageReputation)}
                </p>
              </div>
              <Star className="h-4 w-4 text-gray-400" />
            </div>
          </div>
        </div>

        {/* Agent List */}
        <div className="space-y-3">
          {agents?.map((agent) => {
            const reputationLevel = getReputationLevel(agent.reputation);
            const ReputationIcon = reputationLevel.icon;
            
            return (
              <div
                key={agent.id}
                className={`border rounded-lg p-4 transition-all duration-200 hover:bg-gray-700/30 cursor-pointer ${
                  selectedAgent === agent.id ? 'border-blue-500 bg-blue-500/10' : 'border-gray-600'
                }`}
                onClick={() => setSelectedAgent(selectedAgent === agent.id ? null : agent.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {/* Agent Type Icon */}
                    <div className={`w-10 h-10 rounded-lg border flex items-center justify-center text-sm font-bold ${getAgentTypeColor(agent.type)}`}>
                      {getAgentTypeIcon(agent.type)}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="font-medium text-white text-sm">
                          {agent.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </h3>
                        <div className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                          {agent.status}
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-3 text-xs text-gray-400 mt-1">
                        <span>{agent.type}</span>
                        <span>•</span>
                        <span>{agent.specialty}</span>
                        <span>•</span>
                        <span>{agent.trades} trades</span>
                      </div>
                    </div>
                  </div>

                  {/* Performance Metrics */}
                  <div className="text-right">
                    <div className="flex items-center space-x-1 mb-1">
                      <ReputationIcon className={`h-3 w-3 ${getReputationColor(agent.reputation)}`} />
                      <span className={`text-xs font-medium ${getReputationColor(agent.reputation)}`}>
                        {agent.reputation}
                      </span>
                    </div>
                    <div className={`text-xs font-medium ${getAccuracyColor(agent.accuracy)}`}>
                      {formatPercentage(agent.accuracy)} accuracy
                    </div>
                  </div>
                </div>

                {/* Expanded Agent Details */}
                {selectedAgent === agent.id && (
                  <div className="mt-4 pt-4 border-t border-gray-600">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <h4 className="font-medium text-gray-300 mb-2">Performance Metrics</h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-gray-400">Reputation:</span>
                            <div className="flex items-center">
                              <span className={`font-medium ${getReputationColor(agent.reputation)}`}>
                                {agent.reputation}
                              </span>
                              <span className="text-xs text-gray-500 ml-1">
                                ({reputationLevel.level})
                              </span>
                            </div>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Accuracy:</span>
                            <span className={`font-medium ${getAccuracyColor(agent.accuracy)}`}>
                              {formatPercentage(agent.accuracy)}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Total Trades:</span>
                            <span className="text-white font-medium">{agent.trades}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Specialty:</span>
                            <span className="text-white font-medium">{agent.specialty}</span>
                          </div>
                        </div>
                      </div>

                      <div>
                        <h4 className="font-medium text-gray-300 mb-2">Agent Configuration</h4>
                        <div className="space-y-2">
                          <div className="flex justify-between">
                            <span className="text-gray-400">Type:</span>
                            <span className="text-white font-medium">{agent.type}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Status:</span>
                            <span className={`font-medium capitalize ${getStatusColor(agent.status).split(' ')[0]}`}>
                              {agent.status}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Prediction Weight:</span>
                            <span className="text-white font-medium">
                              {Math.round(agent.reputation / 100)}%
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-400">Risk Tolerance:</span>
                            <span className="text-white font-medium">Medium</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Performance Bars */}
                    <div className="mt-4 space-y-3">
                      <div>
                        <div className="flex justify-between text-xs text-gray-400 mb-1">
                          <span>Accuracy</span>
                          <span>{formatPercentage(agent.accuracy)}</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full transition-all duration-500 ${
                              agent.accuracy >= 0.75 ? 'bg-green-500' : 
                              agent.accuracy >= 0.65 ? 'bg-yellow-500' : 
                              agent.accuracy >= 0.55 ? 'bg-orange-500' : 'bg-red-500'
                            }`}
                            style={{ width: `${agent.accuracy * 100}%` }}
                          />
                        </div>
                      </div>

                      <div>
                        <div className="flex justify-between text-xs text-gray-400 mb-1">
                          <span>Reputation Level</span>
                          <span>{agent.reputation}/10000</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full transition-all duration-500 ${
                              agent.reputation >= 8000 ? 'bg-green-500' : 
                              agent.reputation >= 6000 ? 'bg-yellow-500' : 
                              agent.reputation >= 4000 ? 'bg-orange-500' : 'bg-red-500'
                            }`}
                            style={{ width: `${agent.reputation / 100}%` }}
                          />
                        </div>
                      </div>
                    </div>

                    {/* Recent Activity */}
                    <div className="mt-4 pt-3 border-t border-gray-600">
                      <h5 className="text-xs font-medium text-gray-300 mb-2">Recent Activity</h5>
                      <div className="space-y-1 text-xs text-gray-400">
                        <div>• Participated in BTC prediction market (2 hours ago)</div>
                        <div>• Generated trading signal: LONG ETH-USDT (4 hours ago)</div>
                        <div>• Updated reputation score: +120 points (6 hours ago)</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {(!agents || agents.length === 0) && (
          <div className="text-center py-8 text-gray-400">
            <Users className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>No active agents</p>
            <p className="text-sm">Agents are deployed automatically to prediction markets</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgentStatus;