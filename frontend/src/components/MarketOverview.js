import React from 'react';
import { TrendingUp, Target, DollarSign } from 'lucide-react';

const MarketOverview = ({ markets, metrics }) => {
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
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(value);
  };

  const totalVolume = markets?.reduce((sum, market) => sum + market.volume, 0) || 0;
  const avgConfidence = markets?.length ? 
    markets.reduce((sum, market) => sum + market.confidence, 0) / markets.length : 0;

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
      <h2 className="text-xl font-bold text-white mb-4">📊 Market Overview</h2>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-700/30 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Markets</p>
              <p className="text-2xl font-bold text-white">
                {markets?.length || 0}
              </p>
            </div>
            <Target className="h-6 w-6 text-blue-400" />
          </div>
        </div>

        <div className="bg-gray-700/30 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Volume</p>
              <p className="text-2xl font-bold text-green-400">
                {formatCurrency(totalVolume)}
              </p>
            </div>
            <DollarSign className="h-6 w-6 text-green-400" />
          </div>
        </div>

        <div className="bg-gray-700/30 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Avg Confidence</p>
              <p className="text-2xl font-bold text-purple-400">
                {formatPercentage(avgConfidence)}
              </p>
            </div>
            <TrendingUp className="h-6 w-6 text-purple-400" />
          </div>
        </div>

        <div className="bg-gray-700/30 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Success Rate</p>
              <p className="text-2xl font-bold text-green-400">
                {formatPercentage(metrics?.accuracyRate || 0)}
              </p>
            </div>
            <TrendingUp className="h-6 w-6 text-green-400" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketOverview;