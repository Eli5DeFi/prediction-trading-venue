import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Users, Volume2, Clock, CheckCircle } from 'lucide-react';

const PredictionMarkets = ({ markets }) => {
  const [selectedMarket, setSelectedMarket] = useState(null);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  };

  const formatPercentage = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'percent',
      minimumFractionDigits: 0,
      maximumFractionDigits: 1
    }).format(value);
  };

  const getMarketTypeIcon = (type) => {
    switch (type) {
      case 'crypto_price':
        return '₿';
      case 'ai_performance':
        return '🤖';
      case 'tech_trends':
        return '🔬';
      default:
        return '📊';
    }
  };

  const getMarketTypeColor = (type) => {
    switch (type) {
      case 'crypto_price':
        return 'text-orange-400 bg-orange-400/10';
      case 'ai_performance':
        return 'text-blue-400 bg-blue-400/10';
      case 'tech_trends':
        return 'text-purple-400 bg-purple-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  const getConsensusColor = (consensus, confidence) => {
    const strength = confidence * Math.abs(consensus);
    if (strength >= 0.7) return 'text-green-400';
    if (strength >= 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getConsensusDirection = (consensus) => {
    if (consensus > 0.6) return { icon: TrendingUp, text: 'Bullish', color: 'text-green-400' };
    if (consensus < 0.4) return { icon: TrendingDown, text: 'Bearish', color: 'text-red-400' };
    return { icon: TrendingUp, text: 'Neutral', color: 'text-gray-400' };
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          📊 Live Prediction Markets
          <span className="ml-3 text-sm font-normal text-gray-400">
            {markets?.length || 0} Active
          </span>
        </h2>
      </div>

      <div className="p-6">
        <div className="space-y-4">
          {markets?.map((market) => {
            const direction = getConsensusDirection(market.consensus);
            const DirectionIcon = direction.icon;
            
            return (
              <div 
                key={market.id}
                className={`border rounded-lg p-4 transition-all duration-200 hover:bg-gray-700/50 cursor-pointer ${
                  selectedMarket === market.id ? 'border-blue-500 bg-blue-500/10' : 'border-gray-600'
                }`}
                onClick={() => setSelectedMarket(selectedMarket === market.id ? null : market.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    {/* Market Header */}
                    <div className="flex items-center mb-3">
                      <span className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold mr-3 ${getMarketTypeColor(market.type)}`}>
                        {getMarketTypeIcon(market.type)}
                      </span>
                      <div>
                        <h3 className="font-medium text-white text-sm leading-tight">
                          {market.question}
                        </h3>
                        <div className="flex items-center mt-1 space-x-3 text-xs text-gray-400">
                          <span className="flex items-center">
                            <Users className="h-3 w-3 mr-1" />
                            {market.agentCount} agents
                          </span>
                          <span className="flex items-center">
                            <Volume2 className="h-3 w-3 mr-1" />
                            {formatCurrency(market.volume)}
                          </span>
                          <span className="flex items-center">
                            <CheckCircle className="h-3 w-3 mr-1" />
                            {market.status}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Consensus Display */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center">
                          <DirectionIcon className={`h-4 w-4 mr-2 ${direction.color}`} />
                          <span className={`font-medium ${direction.color}`}>
                            {direction.text}
                          </span>
                        </div>
                        
                        <div className="text-sm">
                          <span className="text-gray-400">Consensus: </span>
                          <span className={`font-bold ${getConsensusColor(market.consensus, market.confidence)}`}>
                            {formatPercentage(market.consensus)}
                          </span>
                        </div>
                        
                        <div className="text-sm">
                          <span className="text-gray-400">Confidence: </span>
                          <span className={`font-bold ${getConsensusColor(market.consensus, market.confidence)}`}>
                            {formatPercentage(market.confidence)}
                          </span>
                        </div>
                      </div>

                      {/* Execution Status */}
                      <div className="flex items-center">
                        {market.confidence >= 0.7 ? (
                          <div className="flex items-center text-green-400">
                            <CheckCircle className="h-4 w-4 mr-1" />
                            <span className="text-xs font-medium">EXECUTABLE</span>
                          </div>
                        ) : (
                          <div className="flex items-center text-yellow-400">
                            <Clock className="h-4 w-4 mr-1" />
                            <span className="text-xs font-medium">MONITORING</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Expanded Details */}
                    {selectedMarket === market.id && (
                      <div className="mt-4 pt-4 border-t border-gray-600">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <h4 className="font-medium text-gray-300 mb-2">Market Details</h4>
                            <div className="space-y-1">
                              <div className="flex justify-between">
                                <span className="text-gray-400">Type:</span>
                                <span className="text-white capitalize">{market.type.replace('_', ' ')}</span>
                              </div>
                              {market.asset && (
                                <div className="flex justify-between">
                                  <span className="text-gray-400">Asset:</span>
                                  <span className="text-white font-mono">{market.asset}</span>
                                </div>
                              )}
                              <div className="flex justify-between">
                                <span className="text-gray-400">Volume:</span>
                                <span className="text-white">{formatCurrency(market.volume)}</span>
                              </div>
                            </div>
                          </div>
                          
                          <div>
                            <h4 className="font-medium text-gray-300 mb-2">Consensus Metrics</h4>
                            <div className="space-y-1">
                              <div className="flex justify-between">
                                <span className="text-gray-400">Signal Strength:</span>
                                <span className={`font-bold ${getConsensusColor(market.consensus, market.confidence)}`}>
                                  {formatPercentage(Math.abs(market.consensus))}
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Agent Count:</span>
                                <span className="text-white">{market.agentCount}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Execution Threshold:</span>
                                <span className="text-gray-300">70%</span>
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* Confidence Bar */}
                        <div className="mt-4">
                          <div className="flex justify-between text-xs text-gray-400 mb-1">
                            <span>Confidence Level</span>
                            <span>{formatPercentage(market.confidence)}</span>
                          </div>
                          <div className="w-full bg-gray-700 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full transition-all duration-500 ${
                                market.confidence >= 0.7 ? 'bg-green-500' : 
                                market.confidence >= 0.5 ? 'bg-yellow-500' : 'bg-red-500'
                              }`}
                              style={{ width: `${market.confidence * 100}%` }}
                            />
                          </div>
                          <div className="flex justify-between text-xs text-gray-400 mt-1">
                            <span>Low</span>
                            <span className="text-gray-500">|</span>
                            <span>70% Threshold</span>
                            <span className="text-gray-500">|</span>
                            <span>High</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {(!markets || markets.length === 0) && (
          <div className="text-center py-8 text-gray-400">
            <TrendingUp className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>No active prediction markets</p>
            <p className="text-sm">Markets are created automatically every 6 hours</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictionMarkets;