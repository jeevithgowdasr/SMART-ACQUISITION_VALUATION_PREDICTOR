import React, { useState } from 'react';
import ComparisonView from './ComparisonView';

// Simple bar chart component
const BarChart = ({ data, title, color = "from-blue-500 to-purple-600" }) => {
  const maxValue = Math.max(...data.map(item => item.value), 1);
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="space-y-4">
        {data.map((item, index) => (
          <div key={index} className="group">
            <div className="flex justify-between mb-1">
              <span className="text-sm font-medium text-gray-700">{item.label}</span>
              <span className="text-sm font-medium text-gray-900">{item.value}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div 
                className={`bg-gradient-to-r ${color} h-2.5 rounded-full transition-all duration-1000 ease-out`}
                style={{ width: `${(item.value / maxValue) * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Radar chart component for multi-dimensional data
const RadarChart = ({ data, title }) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="grid grid-cols-2 gap-4">
        {data.map((item, index) => (
          <div key={index} className="text-center">
            <div className="text-2xl font-bold text-blue-600">{item.value}</div>
            <div className="text-xs text-gray-500 mt-1">{item.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Comparison card component
const ComparisonCard = ({ title, currentValue, benchmarkValue, description }) => {
  const difference = currentValue - benchmarkValue;
  const isPositive = difference > 0;
  
  // For benchmark gaps, we want to show how the startup compares to the benchmark
  // Positive gap means better than benchmark, negative means worse
  const getStatusColor = (value) => {
    if (value > 0.2) return 'text-green-600'; // Significantly better
    if (value > 0) return 'text-green-500';   // Better
    if (value < -0.2) return 'text-red-600';  // Significantly worse
    if (value < 0) return 'text-red-500';     // Worse
    return 'text-gray-500';                   // Neutral
  };
  
  const getStatusText = (value) => {
    if (value > 0.2) return 'Significantly Better';
    if (value > 0) return 'Better';
    if (value < -0.2) return 'Significantly Worse';
    if (value < 0) return 'Worse';
    return 'On Par';
  };
  
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-500 mb-4">{description}</p>
      <div className="flex flex-col items-center">
        <div className={`text-3xl font-bold ${getStatusColor(currentValue)}`}>
          {currentValue >= 0 ? '+' : ''}{(currentValue * 100).toFixed(1)}%
        </div>
        <div className="text-sm text-gray-500 mt-1">
          {getStatusText(currentValue)}
        </div>
        <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full ${getStatusColor(currentValue)}`}
            style={{ 
              width: `${Math.min(100, Math.abs(currentValue) * 100)}%`,
              marginLeft: currentValue < 0 ? `${100 - Math.min(100, Math.abs(currentValue) * 100)}%` : '0'
            }}
          ></div>
        </div>
        <div className="flex justify-between w-full mt-2 text-xs text-gray-500">
          <span>-100%</span>
          <span>Benchmark</span>
          <span>+100%</span>
        </div>
      </div>
    </div>
  );
};

// Team Details Component
const TeamDetails = ({ teamDetails }) => {
  if (!teamDetails) return null;

  // Format currency in both USD and INR
  const formatCurrency = (amount, currency = 'USD') => {
    if (currency === 'INR') {
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(amount);
    } else {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(amount);
    }
  };

  // Convert USD to INR (approximate rate)
  const convertToINR = (usdAmount) => {
    const exchangeRate = 83; // Approximate exchange rate
    return usdAmount * exchangeRate;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
      <div className="flex items-center mb-4">
        <span className="text-2xl mr-3">👥</span>
        <h3 className="text-xl font-semibold text-gray-900">Team Analysis</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-sm text-blue-800 font-medium">Team Strength Score</div>
          <div className="text-xl font-bold text-blue-600">{teamDetails.team_strength_score?.toFixed(2) || 'N/A'}</div>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="text-sm text-purple-800 font-medium">Founder Count</div>
          <div className="text-xl font-bold text-purple-600">{teamDetails.founder_count || 'N/A'}</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-sm text-green-800 font-medium">Avg Experience</div>
          <div className="text-xl font-bold text-green-600">{teamDetails.avg_experience?.toFixed(1) || 'N/A'} years</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <div className="text-sm text-yellow-800 font-medium">Team Size</div>
          <div className="text-xl font-bold text-yellow-600">{teamDetails.estimated_team_size || 'N/A'} employees</div>
        </div>
      </div>

      {teamDetails.founder_details && teamDetails.founder_details.length > 0 && (
        <div>
          <h4 className="font-medium text-gray-900 mb-3">Founder Details</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {teamDetails.founder_details.map((founder, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-3">
                <div className="flex justify-between">
                  <span className="font-medium text-gray-900">Founder {index + 1}</span>
                  {founder.has_exit && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Previous Exit
                    </span>
                  )}
                </div>
                <div className="text-sm text-gray-600 mt-1">
                  {founder.experience} years of experience
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Valuation Display Component
const ValuationDisplay = ({ usdValue, inrValue }) => {
  return (
    <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100">
      <div className="flex items-center mb-4">
        <span className="text-2xl mr-3">💰</span>
        <h3 className="text-xl font-semibold text-gray-900">Valuation Forecast</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="text-sm text-gray-500 mb-1">USD Value</div>
          <div className="text-2xl font-bold text-gray-900">
            {new Intl.NumberFormat('en-US', {
              style: 'currency',
              currency: 'USD',
              minimumFractionDigits: 0,
              maximumFractionDigits: 0,
            }).format(usdValue || 0)}
          </div>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm">
          <div className="text-sm text-gray-500 mb-1">INR Value</div>
          <div className="text-2xl font-bold text-gray-900">
            {new Intl.NumberFormat('en-IN', {
              style: 'currency',
              currency: 'INR',
              minimumFractionDigits: 0,
              maximumFractionDigits: 0,
            }).format(inrValue || 0)}
          </div>
        </div>
      </div>
    </div>
  );
};

const ResultsDisplay = ({ result, onReset, formData }) => {
  const [viewMode, setViewMode] = useState('summary'); // 'summary' or 'comparison'

  if (!result) {
    return (
      <div className="bg-white rounded-2xl shadow-xl p-8 text-center border border-gray-100 animate-fadeIn">
        <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-gray-100">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 className="mt-4 text-xl font-medium text-gray-900">No results to display</h3>
        <p className="mt-2 text-gray-500">Please run an analysis to see results</p>
        <button
          onClick={onReset}
          className="mt-6 inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105 shadow-sm"
        >
          Back to Form
        </button>
      </div>
    );
  }

  // Helper function to format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  // Helper function to format percentage
  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  // Key metrics data with enhanced acquisition likelihood display
  const keyMetrics = [
    {
      title: "Acquisition Likelihood",
      value: formatPercentage(result.mna_likelihood),
      icon: "🎯",
      color: "from-green-400 to-emerald-600",
      description: "Probability of successful acquisition",
      detail: `Based on ${result.decision_score?.mna_likelihood !== undefined ? 'ML model prediction' : 'comprehensive analysis'}`
    },
    {
      title: "Valuation Forecast",
      value: formatCurrency(result.valuation_forecast_usd),
      icon: "💰",
      color: "from-blue-400 to-indigo-600",
      description: "Predicted company valuation",
      detail: `INR: ${new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(result.valuation_forecast_inr || 0)}`
    },
    {
      title: "Decision Score",
      value: result.decision_score?.acquisition_score ? result.decision_score.acquisition_score.toFixed(2) : 'N/A',
      icon: "🧠",
      color: "from-purple-400 to-violet-600",
      description: "Overall acquisition recommendation",
      detail: result.explanation?.decision || 'Not available'
    }
  ];

  // Synergy data for bar chart
  const synergyData = [
    { label: "Market Similarity", value: result.synergy_details?.market_similarity || 0 },
    { label: "Technology Similarity", value: result.synergy_details?.tech_similarity || 0 },
    { label: "Revenue Synergy", value: result.synergy_details?.revenue_synergy_score || 0 },
    { label: "Cost Synergy", value: result.synergy_details?.cost_synergy_score || 0 },
    { label: "Overall Synergy", value: result.synergy_details?.overall_synergy_score || 0 }
  ];

  // Risk assessment data
  const riskData = [
    { label: "Funding Risk", value: result.risk?.funding_risk || 0 },
    { label: "Team Risk", value: result.risk?.team_risk || 0 },
    { label: "Synergy Risk", value: result.risk?.synergy_risk || 0 },
    { label: "Valuation Risk", value: result.risk?.valuation_risk || 0 },
    { label: "Combined Risk", value: result.risk?.combined_risk_score || 0 }
  ];

  // Business model evaluation
  const businessModelData = [
    { label: "Business Model Score", value: result.business_model_evaluation?.business_model_score || 0 },
    { label: "Funding Efficiency", value: result.business_model_evaluation?.funding_efficiency || 0 },
    { label: "Team Strength", value: result.business_model_evaluation?.team_strength_for_execution || 0 },
    { label: "Revenue Sustainability", value: result.business_model_evaluation?.revenue_sustainability || 0 }
  ];

  // Benchmarks comparison
  const benchmarkComparisons = [
    {
      title: "Funding Benchmark",
      currentValue: result.benchmarks?.funding_benchmark_gap || 0,
      benchmarkValue: 0,
      description: "Gap between current funding and industry benchmark"
    },
    {
      title: "Team Experience",
      currentValue: result.benchmarks?.team_experience_gap || 0,
      benchmarkValue: 0,
      description: "Gap between team experience and industry standard"
    },
    {
      title: "Synergy Benchmark",
      currentValue: result.benchmarks?.synergy_benchmark_gap || 0,
      benchmarkValue: 0,
      description: "Synergy score compared to industry average"
    },
    {
      title: "Valuation Multiple",
      currentValue: result.benchmarks?.valuation_multiple_gap || 0,
      benchmarkValue: 0,
      description: "Valuation multiple compared to peers"
    },
    {
      title: "Growth Benchmark",
      currentValue: result.benchmarks?.growth_benchmark_gap || 0,
      benchmarkValue: 0,
      description: "Revenue growth compared to industry average"
    },
    {
      title: "Revenue TTM",
      currentValue: result.benchmarks?.revenue_ttm_gap || 0,
      benchmarkValue: 0,
      description: "Trailing twelve months revenue compared to benchmark"
    }
  ];

  // Decision components
  const decisionComponents = [
    { label: "M&A Likelihood", value: result.decision_score?.mna_likelihood || 0 },
    { label: "Synergy Component", value: result.decision_score?.synergy_component || 0 },
    { label: "Valuation Component", value: result.decision_score?.valuation_component || 0 },
    { label: "Team Component", value: result.decision_score?.team_component || 0 },
    { label: "Benchmark Component", value: result.decision_score?.benchmark_component || 0 },
    { label: "Risk Penalty", value: result.decision_score?.risk_penalty || 0 }
  ];

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header with back button and view toggle */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Analysis Results</h2>
          <p className="text-gray-600 mt-1">AI-powered insights for your M&A decision</p>
        </div>
        <div className="flex space-x-3">
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('summary')}
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                viewMode === 'summary' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Summary
            </button>
            <button
              onClick={() => setViewMode('comparison')}
              className={`px-4 py-2 text-sm font-medium rounded-md ${
                viewMode === 'comparison' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Comparison
            </button>
          </div>
          <button
            onClick={onReset}
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105 shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Back to Form
          </button>
        </div>
      </div>

      {/* View Content */}
      {viewMode === 'comparison' && formData ? (
        <ComparisonView formData={formData} result={result} />
      ) : (
        <>
          {/* Key Metrics Overview with enhanced details */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {keyMetrics.map((metric, index) => (
              <div 
                key={metric.title}
                className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
              >
                <div className="flex items-center">
                  <div className={`rounded-xl bg-gradient-to-r ${metric.color} p-3 text-white text-xl`}>
                    {metric.icon}
                  </div>
                  <div className="ml-4">
                    <h3 className="text-sm font-medium text-gray-500">{metric.title}</h3>
                    <p className="text-2xl font-bold text-gray-900 mt-1">{metric.value}</p>
                  </div>
                </div>
                <p className="mt-3 text-sm text-gray-500">{metric.description}</p>
                {metric.detail && (
                  <p className="mt-2 text-xs text-gray-400">{metric.detail}</p>
                )}
              </div>
            ))}
          </div>

          {/* Acquisition Likelihood Insights */}
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-6 border border-green-100">
            <div className="flex items-center mb-4">
              <span className="text-2xl mr-3">🎯</span>
              <h3 className="text-xl font-semibold text-gray-900">Acquisition Likelihood Analysis</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Key Factors</h4>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li className="flex justify-between">
                    <span>Synergy Score:</span>
                    <span className="font-medium">{formatPercentage(result.synergy_details?.overall_synergy_score || 0)}</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Team Strength:</span>
                    <span className="font-medium">{(result.team_details?.team_strength_score || 0).toFixed(2)}</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Funding Efficiency:</span>
                    <span className="font-medium">{formatPercentage(result.business_model_evaluation?.funding_efficiency || 0)}</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Revenue Growth:</span>
                    <span className="font-medium">{formatPercentage(result.financials_json?.revenue_growth_mom || result.revenue_growth_mom || 0)}</span>
                  </li>
                </ul>
              </div>
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Decision Insights</h4>
                <p className="text-sm text-gray-700 mb-3">
                  {result.explanation?.rationale?.[0] || 'Based on comprehensive analysis of multiple factors'}
                </p>
                <div className="flex items-center">
                  <span className="text-sm font-medium text-gray-900 mr-2">Recommendation:</span>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    result.explanation?.decision === 'ACQUIRE' 
                      ? 'bg-green-100 text-green-800' 
                      : result.explanation?.decision === 'INVESTIGATE' 
                        ? 'bg-yellow-100 text-yellow-800' 
                        : 'bg-red-100 text-red-800'
                  }`}>
                    {result.explanation?.decision || 'INVESTIGATE'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Valuation Display with INR */}
          <ValuationDisplay 
            usdValue={result.valuation_forecast_usd} 
            inrValue={result.valuation_forecast_inr} 
          />

          {/* Team Details */}
          <TeamDetails teamDetails={result.team_details} />

          {/* Detailed Results - Charts and Comparisons */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Synergy Analysis Chart */}
            <BarChart 
              data={synergyData.map(item => ({ ...item, value: parseFloat((item.value * 100).toFixed(1)) }))}
              title="Synergy Analysis"
              color="from-blue-500 to-purple-600"
            />

            {/* Risk Assessment Chart */}
            <BarChart 
              data={riskData.map(item => ({ ...item, value: parseFloat((item.value * 100).toFixed(1)) }))}
              title="Risk Assessment"
              color="from-red-500 to-orange-500"
            />

            {/* Business Model Evaluation */}
            <RadarChart 
              data={businessModelData.map(item => ({ ...item, value: parseFloat((item.value * 100).toFixed(1)) }))}
              title="Business Model Evaluation"
            />

            {/* Decision Components */}
            <BarChart 
              data={decisionComponents.map(item => ({ ...item, value: parseFloat((item.value * 100).toFixed(1)) }))}
              title="Decision Components"
              color="from-green-500 to-teal-500"
            />
          </div>

          {/* Benchmark Comparisons */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Benchmark Comparisons</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {benchmarkComparisons.map((benchmark, index) => (
                <ComparisonCard 
                  key={index}
                  title={benchmark.title}
                  currentValue={benchmark.currentValue}
                  benchmarkValue={benchmark.benchmarkValue}
                  description={benchmark.description}
                />
              ))}
            </div>
          </div>

          {/* AI Explanation */}
          {result.explanation && (
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl shadow-lg p-6 border border-blue-100">
              <div className="flex items-center mb-4">
                <span className="text-2xl mr-3">🤖</span>
                <h3 className="text-xl font-semibold text-gray-900">AI Insights & Recommendations</h3>
              </div>
              <div className="prose max-w-none">
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-900">Decision: {result.explanation.decision}</h4>
                  <p className="text-gray-700">Confidence: {formatPercentage(result.explanation.confidence)}</p>
                </div>
                
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-900">Rationale:</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {result.explanation.rationale.map((point, index) => (
                      <li key={index} className="text-gray-700">{point}</li>
                    ))}
                  </ul>
                </div>
                
                <div className="mb-4">
                  <h4 className="font-semibold text-gray-900">Key Drivers:</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
                    {result.explanation.key_drivers.map((driver, index) => (
                      <div key={index} className="bg-white p-3 rounded-lg border border-gray-200">
                        <div className="font-medium text-gray-900">{driver.name}</div>
                        <div className="text-sm text-gray-600">Value: {driver.value}</div>
                        <div className={`text-sm ${driver.impact === 'positive' ? 'text-green-600' : 'text-red-600'}`}>
                          Impact: {driver.impact}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-semibold text-gray-900">Suggested Actions:</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {result.explanation.suggested_actions.map((action, index) => (
                      <li key={index} className="text-gray-700">{action}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Business Model Insights */}
          {result.business_model_insights && (
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
              <div className="flex items-center mb-4">
                <span className="text-2xl mr-3">💼</span>
                <h3 className="text-xl font-semibold text-gray-900">Business Model Insights</h3>
              </div>
              <div className="prose max-w-none">
                <p className="text-gray-700 mb-4">{result.business_model_insights.insights}</p>
                
                <h4 className="font-semibold text-gray-900 mb-2">Key Patterns:</h4>
                <ul className="list-disc pl-5 space-y-1 mb-4">
                  {result.business_model_insights.key_patterns?.map((pattern, index) => (
                    <li key={index} className="text-gray-700">{pattern}</li>
                  ))}
                </ul>
                
                <h4 className="font-semibold text-gray-900 mb-2">Sample Evaluations:</h4>
                <div className="space-y-3">
                  {result.business_model_insights.sample_evaluations?.map((evaluation, index) => (
                    <div key={index} className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-gray-700">{evaluation}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ResultsDisplay;