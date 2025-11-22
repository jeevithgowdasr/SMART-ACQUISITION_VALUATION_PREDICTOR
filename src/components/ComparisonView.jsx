import React from 'react';

// Comparison card for two startups
const StartupComparisonCard = ({ title, startup1Value, startup2Value, description, format = 'number' }) => {
  const formatValue = (value) => {
    if (format === 'currency') {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value);
    } else if (format === 'percentage') {
      return `${(value * 100).toFixed(1)}%`;
    } else {
      return value?.toFixed(2) || 'N/A';
    }
  };

  const difference = startup1Value - startup2Value;
  const isStartup1Better = difference > 0;

  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-500 mb-4">{description}</p>
      
      <div className="grid grid-cols-3 gap-4 items-center">
        <div className="text-center">
          <div className="text-xl font-bold text-blue-600">{formatValue(startup1Value)}</div>
          <div className="text-xs text-gray-500">Startup 1</div>
        </div>
        
        <div className="text-center">
          <div className={`text-2xl ${isStartup1Better ? 'text-green-500' : 'text-red-500'}`}>
            {difference > 0 ? '↗' : difference < 0 ? '↘' : '→'}
          </div>
          <div className="text-xs text-gray-500">
            {difference > 0 ? '+' : ''}{formatValue(difference)}
          </div>
        </div>
        
        <div className="text-center">
          <div className="text-xl font-bold text-purple-600">{formatValue(startup2Value)}</div>
          <div className="text-xs text-gray-500">Startup 2</div>
        </div>
      </div>
    </div>
  );
};

// Radar chart for multi-dimensional comparison
const ComparisonRadarChart = ({ data, title }) => {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="grid grid-cols-2 gap-4">
        {data.map((item, index) => (
          <div key={index} className="p-3 rounded-lg border border-gray-200">
            <div className="flex justify-between">
              <span className="text-sm font-medium text-gray-700">{item.label}</span>
            </div>
            <div className="flex justify-between mt-2">
              <span className="text-sm text-blue-600">S1: {typeof item.startup1 === 'number' ? item.startup1.toFixed(2) : 'N/A'}</span>
              <span className="text-sm text-purple-600">S2: {typeof item.startup2 === 'number' ? item.startup2.toFixed(2) : 'N/A'}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div 
                className="bg-gradient-to-r from-blue-500 to-blue-300 h-2 rounded-full"
                style={{ width: `${Math.min(100, (item.startup1 || 0) * 50)}%` }}
              ></div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
              <div 
                className="bg-gradient-to-r from-purple-500 to-purple-300 h-2 rounded-full"
                style={{ width: `${Math.min(100, (item.startup2 || 0) * 50)}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const ComparisonView = ({ formData, result }) => {
  if (!formData || !result) return null;

  // Funding comparison data
  const fundingComparison = [
    {
      title: "Total Funding",
      startup1Value: parseFloat(formData.startup1.totalFunding) || 0,
      startup2Value: parseFloat(formData.startup2.totalFunding) || 0,
      description: "Total funding raised by each startup",
      format: 'currency'
    },
    {
      title: "Team Size",
      startup1Value: parseInt(formData.startup1.employees) || 0,
      startup2Value: parseInt(formData.startup2.employees) || 0,
      description: "Number of employees",
      format: 'number'
    },
    {
      title: "Founder Experience",
      startup1Value: parseInt(formData.startup1.founderExperience) || 0,
      startup2Value: parseInt(formData.startup2.founderExperience) || 0,
      description: "Average founder experience in years",
      format: 'number'
    }
  ];

  // Financial comparison data
  const financialComparison = [
    {
      title: "Revenue (TTM)",
      startup1Value: parseFloat(formData.revenueTTM) || 0,
      startup2Value: parseFloat(formData.targetRevenue) || 0,
      description: "Trailing twelve months revenue",
      format: 'currency'
    },
    {
      title: "Gross Margin",
      startup1Value: parseFloat(formData.grossMargin) || 0,
      startup2Value: parseFloat(formData.grossMargin) || 0,
      description: "Gross profit margin",
      format: 'percentage'
    },
    {
      title: "EBITDA Margin",
      startup1Value: parseFloat(formData.ebitdaMargin) || 0,
      startup2Value: parseFloat(formData.ebitdaMargin) || 0,
      description: "EBITDA margin",
      format: 'percentage'
    }
  ];

  // Valuation comparison
  const valuationComparison = [
    {
      label: "Valuation Forecast",
      startup1: result.valuation_forecast_usd || 0,
      startup2: (parseFloat(formData.targetRevenue) || 0) * 5 // Simple 5x revenue multiple for comparison
    },
    {
      label: "Revenue Multiple",
      startup1: (result.valuation_forecast_usd || 0) / (parseFloat(formData.revenueTTM) || 1),
      startup2: 5 // Industry benchmark
    }
  ];

  return (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Startup Comparison Analysis</h2>
        <p className="text-gray-600 mt-2">Side-by-side comparison of the two startups</p>
      </div>

      {/* Startup Names Header */}
      <div className="grid grid-cols-3 gap-6 mb-8">
        <div className="bg-blue-50 rounded-xl p-4 text-center">
          <h3 className="font-semibold text-blue-800">Startup 1</h3>
          <p className="text-blue-600">{formData.startup1.companyName || 'Target Company'}</p>
        </div>
        <div className="bg-gray-50 rounded-xl p-4 text-center">
          <h3 className="font-semibold text-gray-800">Comparison</h3>
          <p className="text-gray-600">vs</p>
        </div>
        <div className="bg-purple-50 rounded-xl p-4 text-center">
          <h3 className="font-semibold text-purple-800">Startup 2</h3>
          <p className="text-purple-600">{formData.startup2.companyName || 'Acquirer Company'}</p>
        </div>
      </div>

      {/* Funding Comparison */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Funding & Team Comparison</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {fundingComparison.map((item, index) => (
            <StartupComparisonCard
              key={index}
              title={item.title}
              startup1Value={item.startup1Value}
              startup2Value={item.startup2Value}
              description={item.description}
              format={item.format}
            />
          ))}
        </div>
      </div>

      {/* Financial Comparison */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Financial Comparison</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {financialComparison.map((item, index) => (
            <StartupComparisonCard
              key={index}
              title={item.title}
              startup1Value={item.startup1Value}
              startup2Value={item.startup2Value}
              description={item.description}
              format={item.format}
            />
          ))}
        </div>
      </div>

      {/* Valuation Comparison */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Valuation Comparison</h3>
        <ComparisonRadarChart data={valuationComparison} title="Valuation Metrics" />
      </div>

      {/* AI Insights */}
      {result.explanation && (
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl shadow-lg p-6 border border-blue-100">
          <div className="flex items-center mb-4">
            <span className="text-2xl mr-3">🤖</span>
            <h3 className="text-xl font-semibold text-gray-900">AI Comparison Insights</h3>
          </div>
          <div className="prose max-w-none">
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900">Recommendation: {result.explanation.decision}</h4>
              <p className="text-gray-700">Confidence: {(result.explanation.confidence * 100).toFixed(1)}%</p>
            </div>
            
            <div className="mb-4">
              <h4 className="font-semibold text-gray-900">Key Insights:</h4>
              <ul className="list-disc pl-5 space-y-1">
                {result.explanation.rationale?.slice(0, 3).map((point, index) => (
                  <li key={index} className="text-gray-700">{point}</li>
                ))}
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-900">Suggested Actions:</h4>
              <ul className="list-disc pl-5 space-y-1">
                {result.explanation.suggested_actions?.slice(0, 3).map((action, index) => (
                  <li key={index} className="text-gray-700">{action}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComparisonView;