import React from 'react';
import { Activity, Server, Zap, AlertCircle, CheckCircle, Clock } from 'lucide-react';

const SystemHealth = ({ uptime, status, metrics }) => {
  const getHealthStatus = () => {
    // Calculate overall health based on metrics
    const factors = [];
    
    // Uptime factor (good if > 1 hour)
    const uptimeHours = parseFloat(uptime) || 0;
    if (uptimeHours >= 1) factors.push(1);
    else factors.push(uptimeHours);
    
    // Accuracy factor
    if (metrics?.accuracyRate) factors.push(metrics.accuracyRate);
    
    // Win rate factor  
    if (metrics?.winRate) factors.push(metrics.winRate);
    
    const score = factors.length > 0 ? factors.reduce((a, b) => a + b, 0) / factors.length : 0;
    
    if (score >= 0.8) return { status: 'Excellent', color: 'text-green-400', icon: CheckCircle };
    if (score >= 0.6) return { status: 'Good', color: 'text-blue-400', icon: CheckCircle };
    if (score >= 0.4) return { status: 'Fair', color: 'text-yellow-400', icon: AlertCircle };
    return { status: 'Poor', color: 'text-red-400', icon: AlertCircle };
  };

  const health = getHealthStatus();
  const HealthIcon = health.icon;

  const systemComponents = [
    {
      name: 'Prediction Engine',
      status: 'operational',
      uptime: '99.8%',
      lastCheck: '30s ago'
    },
    {
      name: 'Trading Bridge', 
      status: 'operational',
      uptime: '99.5%',
      lastCheck: '1m ago'
    },
    {
      name: 'Agent Coordinator',
      status: 'operational', 
      uptime: '100%',
      lastCheck: '15s ago'
    },
    {
      name: 'Risk Manager',
      status: 'operational',
      uptime: '99.9%',
      lastCheck: '45s ago'
    }
  ];

  const getComponentStatusColor = (status) => {
    switch (status) {
      case 'operational':
        return 'text-green-400 bg-green-400/10';
      case 'warning':
        return 'text-yellow-400 bg-yellow-400/10';
      case 'error':
        return 'text-red-400 bg-red-400/10';
      default:
        return 'text-gray-400 bg-gray-400/10';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700">
      <div className="p-6 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white flex items-center">
          🛡️ System Health
        </h2>
      </div>

      <div className="p-6 space-y-6">
        {/* Overall Health Status */}
        <div className="bg-gray-700/30 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-white">Overall Health</h3>
            <div className="flex items-center">
              <HealthIcon className={`h-4 w-4 mr-2 ${health.color}`} />
              <span className={`font-medium ${health.color}`}>
                {health.status}
              </span>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Status:</span>
              <span className="text-green-400 font-medium capitalize">{status}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Uptime:</span>
              <span className="text-white font-medium">{uptime}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Active Markets:</span>
              <span className="text-white font-medium">{metrics?.activeMarkets || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Active Agents:</span>
              <span className="text-white font-medium">{metrics?.activeAgents || 0}</span>
            </div>
          </div>
        </div>

        {/* System Components */}
        <div>
          <h3 className="font-medium text-white mb-3">System Components</h3>
          <div className="space-y-2">
            {systemComponents.map((component, index) => (
              <div 
                key={index}
                className="flex items-center justify-between p-3 bg-gray-700/20 rounded-lg border border-gray-600"
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-2 h-2 rounded-full ${
                    component.status === 'operational' ? 'bg-green-400' : 
                    component.status === 'warning' ? 'bg-yellow-400' : 'bg-red-400'
                  }`} />
                  <span className="text-white font-medium text-sm">{component.name}</span>
                </div>
                
                <div className="flex items-center space-x-3 text-xs text-gray-400">
                  <span>↗ {component.uptime}</span>
                  <span className="flex items-center">
                    <Clock className="h-3 w-3 mr-1" />
                    {component.lastCheck}
                  </span>
                  <div className={`px-2 py-1 rounded-full font-medium ${getComponentStatusColor(component.status)}`}>
                    {component.status}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Performance Metrics */}
        <div>
          <h3 className="font-medium text-white mb-3">Performance Indicators</h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">CPU Usage</span>
                <span className="text-white">23%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '23%' }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Memory Usage</span>
                <span className="text-white">67%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '67%' }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-400">Network I/O</span>
                <span className="text-white">45%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '45%' }} />
              </div>
            </div>
          </div>
        </div>

        {/* Recent Events */}
        <div>
          <h3 className="font-medium text-white mb-3">Recent System Events</h3>
          <div className="space-y-2 text-sm">
            <div className="flex items-center text-green-400">
              <CheckCircle className="h-3 w-3 mr-2" />
              <span>Market creation cycle completed successfully (2m ago)</span>
            </div>
            <div className="flex items-center text-blue-400">
              <Activity className="h-3 w-3 mr-2" />
              <span>5 new prediction signals generated (8m ago)</span>
            </div>
            <div className="flex items-center text-green-400">
              <CheckCircle className="h-3 w-3 mr-2" />
              <span>Trading execution completed: 2 trades (15m ago)</span>
            </div>
            <div className="flex items-center text-blue-400">
              <Zap className="h-3 w-3 mr-2" />
              <span>Agent reputation scores updated (22m ago)</span>
            </div>
          </div>
        </div>

        {/* System Configuration */}
        <div className="border-t border-gray-600 pt-4">
          <h3 className="font-medium text-white mb-3">Configuration</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Execution Threshold:</span>
              <span className="text-white font-mono">70%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Max Position Size:</span>
              <span className="text-white font-mono">2.5%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Cycle Interval:</span>
              <span className="text-white font-mono">30m</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Risk Tolerance:</span>
              <span className="text-white font-mono">Medium</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemHealth;