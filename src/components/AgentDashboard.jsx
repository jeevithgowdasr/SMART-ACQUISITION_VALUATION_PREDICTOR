import React from 'react';
import CompanyLookup from './CompanyLookup';

const AgentDashboard = ({ onAgentSelect }) => {
  const agents = [
    {
      id: 'funding',
      name: 'Funding Agent',
      description: 'Analyzes funding patterns and investment history to predict growth potential',
      icon: '💰',
      color: 'from-yellow-400 to-orange-500',
      metrics: ['Funding Rounds', 'Total Raised', 'Avg Round Size']
    },
    {
      id: 'team',
      name: 'Team Agent',
      description: 'Evaluates team strength, founder experience, and organizational structure',
      icon: '👥',
      color: 'from-blue-400 to-indigo-500',
      metrics: ['Team Size', 'Founder Experience', 'Exit History']
    },
    {
      id: 'synergy',
      name: 'Synergy Agent',
      description: 'Calculates potential synergies between acquirer and target companies',
      icon: '🔗',
      color: 'from-green-400 to-teal-500',
      metrics: ['Market Fit', 'Tech Synergy', 'Revenue Boost']
    },
    {
      id: 'valuation',
      name: 'Valuation Agent',
      description: 'Provides accurate valuation forecasts based on financial metrics',
      icon: '📈',
      color: 'from-purple-400 to-pink-500',
      metrics: ['Revenue Multiple', 'EBITDA Margin', 'Growth Rate']
    },
    {
      id: 'risk',
      name: 'Risk Agent',
      description: 'Assesses acquisition risks and potential issues',
      icon: '⚠️',
      color: 'from-red-400 to-orange-500',
      metrics: ['Funding Risk', 'Team Risk', 'Valuation Risk']
    },
    {
      id: 'benchmark',
      name: 'Benchmark Agent',
      description: 'Compares startup metrics against industry benchmarks',
      icon: '📊',
      color: 'from-indigo-400 to-purple-500',
      metrics: ['Funding Gap', 'Experience Gap', 'Synergy Gap']
    }
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl shadow-xl p-8 text-white">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl font-bold mb-4">Smart Acquirer AI Agents</h1>
          <p className="text-xl mb-6 opacity-90">
            Advanced AI-powered analysis for startup acquisition decisions
          </p>
          <button
            onClick={() => onAgentSelect('form')}
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-blue-600 bg-white hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white transition-all duration-300 transform hover:scale-105"
          >
            Run Full Analysis
            <svg xmlns="http://www.w3.org/2000/svg" className="ml-2 -mr-1 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-300">
          <div className="flex items-center">
            <div className="rounded-full bg-blue-100 p-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Avg. Valuation</p>
              <p className="text-2xl font-bold text-gray-900">$2.7M</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-300">
          <div className="flex items-center">
            <div className="rounded-full bg-green-100 p-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Success Rate</p>
              <p className="text-2xl font-bold text-gray-900">68%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-300">
          <div className="flex items-center">
            <div className="rounded-full bg-purple-100 p-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Team Size</p>
              <p className="text-2xl font-bold text-gray-900">50+</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow duration-300">
          <div className="flex items-center">
            <div className="rounded-full bg-yellow-100 p-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Growth Rate</p>
              <p className="text-2xl font-bold text-gray-900">15%</p>
            </div>
          </div>
        </div>
      </div>

      {/* AI Agents Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">AI Agents</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <div 
              key={agent.id}
              className="bg-white rounded-xl shadow-md border border-gray-100 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 cursor-pointer"
              onClick={() => onAgentSelect(agent.id)}
            >
              <div className="p-6">
                <div className="flex items-start">
                  <div className={`rounded-xl bg-gradient-to-r ${agent.color} p-3 text-white text-2xl`}>
                    {agent.icon}
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-gray-900">{agent.name}</h3>
                    <p className="text-gray-600 text-sm mt-1">{agent.description}</p>
                  </div>
                </div>
                <div className="mt-4">
                  <h4 className="text-xs font-medium text-gray-500 uppercase tracking-wider">Key Metrics</h4>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {agent.metrics.map((metric, index) => (
                      <span 
                        key={index}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                      >
                        {metric}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Company Lookup Section */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl shadow-lg p-8 border border-indigo-100">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Company Lookup</h2>
            <p className="text-gray-600 mt-2">Find competitors and acquisition targets</p>
          </div>
          <CompanyLookup />
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard;