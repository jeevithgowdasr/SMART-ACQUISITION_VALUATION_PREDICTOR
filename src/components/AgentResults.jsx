// Team Agent Results
export const TeamAgentResults = ({ result }) => {
  if (!result) return null;

  // Format team data for visualization
  const teamData = [
    { label: "Founder Count", value: result.team_details?.founder_count || 0 },
    { label: "Avg. Experience (Years)", value: result.team_details?.avg_experience || 0 },
    { label: "Team Size", value: result.team_details?.estimated_team_size || 0 },
    { label: "Team Strength Score", value: result.team_details?.team_strength_score || 0 },
    { label: "Team Composition Score", value: result.team_details?.team_composition_score || 0 }
  ];

  // Experience distribution data
  const experienceData = result.team_details?.experience_distribution ? [
    { label: "Junior", value: result.team_details.experience_distribution.junior || 0 },
    { label: "Mid-level", value: result.team_details.experience_distribution.mid_level || 0 },
    { label: "Senior", value: result.team_details.experience_distribution.senior || 0 },
    { label: "Executive", value: result.team_details.experience_distribution.executive || 0 }
  ] : [];

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Team Agent Analysis</h2>
        <p className="text-gray-600">Evaluation of team strength and member experience</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <BarChart 
          data={teamData}
          title="Team Metrics"
          color="from-blue-500 to-indigo-500"
        />
        
        {experienceData.length > 0 && (
          <BarChart 
            data={experienceData}
            title="Experience Distribution"
            color="from-purple-500 to-pink-500"
          />
        )}
      </div>
      
      {/* Team Member Details */}
      {result.team_details?.founder_details && result.team_details.founder_details.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Team Member Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {result.team_details.founder_details.map((member, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium text-gray-900">{member.name || `Member ${index + 1}`}</h4>
                  {member.has_exit && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Previous Exit
                    </span>
                  )}
                </div>
                <div className="space-y-1 text-sm text-gray-600">
                  <p><span className="font-medium">Role:</span> {member.role || 'N/A'}</p>
                  <p><span className="font-medium">Experience:</span> {member.experience || 0} years</p>
                  <p><span className="font-medium">Level:</span> {member.experience_level || 'N/A'}</p>
                  {member.education && (
                    <p><span className="font-medium">Education:</span> {member.education}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Team Insights</h3>
        <p className="text-gray-700">
          The team consists of {result.team_details?.founder_count || 0} key members with an average of 
          {(result.team_details?.avg_experience || 0).toFixed(1)} years of experience. Team strength score 
          is {(result.team_details?.team_strength_score || 0).toFixed(1)} and composition score is 
          {(result.team_details?.team_composition_score || 0).toFixed(1)}.
        </p>
        {result.team_details?.experience_distribution && (
          <p className="text-gray-700 mt-2">
            Experience distribution: {result.team_details.experience_distribution.junior || 0} junior, 
            {result.team_details.experience_distribution.mid_level || 0} mid-level, 
            {result.team_details.experience_distribution.senior || 0} senior, and 
            {result.team_details.experience_distribution.executive || 0} executive members.
          </p>
        )}
      </div>
    </div>
  );
};

// Funding Agent Results
export const FundingAgentResults = ({ result }) => {
  if (!result) return null;

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  // Funding data for visualization
  const fundingData = [
    { label: "Total Funding", value: result.funding_json?.total_raised_usd || result.financials_json?.total_raised_usd || 0 },
    { label: "Number of Rounds", value: result.funding_json?.num_rounds || 0 },
    { label: "Avg Round Size", value: result.funding_json?.avg_round_size || 0 }
  ];

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Funding Agent Analysis</h2>
        <p className="text-gray-600">Evaluation of funding history and investment patterns</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl p-6 border border-yellow-100 text-center">
          <div className="text-3xl font-bold text-yellow-600">
            {formatCurrency(result.funding_json?.total_raised_usd || result.financials_json?.total_raised_usd || 0)}
          </div>
          <div className="text-gray-600 mt-1">Total Funding Raised</div>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100 text-center">
          <div className="text-3xl font-bold text-blue-600">
            {result.funding_json?.num_rounds || 0}
          </div>
          <div className="text-gray-600 mt-1">Funding Rounds</div>
        </div>
        
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-100 text-center">
          <div className="text-3xl font-bold text-purple-600">
            {formatCurrency(result.funding_json?.avg_round_size || 0)}
          </div>
          <div className="text-gray-600 mt-1">Avg Round Size</div>
        </div>
      </div>
      
      <BarChart 
        data={fundingData.map(item => ({ ...item, value: item.label.includes('Funding') || item.label.includes('Size') ? item.value / 100000 : item.value }))}
        title="Funding Metrics"
        color="from-yellow-500 to-orange-500"
      />
      
      {/* Funding Rounds Details */}
      {result.funding_json?.rounds && result.funding_json.rounds.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Funding Rounds</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Round Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {result.funding_json.rounds.map((round, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{round.type || 'N/A'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatCurrency(round.amount || 0)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{round.date || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl p-6 border border-yellow-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Funding Insights</h3>
        <p className="text-gray-700">
          The company has raised a total of {formatCurrency(result.funding_json?.total_raised_usd || 0)} across 
          {result.funding_json?.num_rounds || 0} funding rounds with an average round size of 
          {formatCurrency(result.funding_json?.avg_round_size || 0)}.
        </p>
      </div>
    </div>
  );
};

// Synergy Agent Results
export const SynergyAgentResults = ({ result }) => {
  if (!result) return null;

  // Format percentage
  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  // Synergy data for visualization
  const synergyData = [
    { label: "Market Similarity", value: result.synergy_details?.market_similarity || 0 },
    { label: "Technology Similarity", value: result.synergy_details?.tech_similarity || 0 },
    { label: "Revenue Synergy", value: result.synergy_details?.revenue_synergy_score || 0 },
    { label: "Cost Synergy", value: result.synergy_details?.cost_synergy_score || 0 },
    { label: "Overall Synergy", value: result.synergy_details?.overall_synergy_score || 0 }
  ];

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Synergy Agent Analysis</h2>
        <p className="text-gray-600">Evaluation of acquisition synergies between companies</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {synergyData.map((item, index) => (
          <div key={index} className="bg-white rounded-xl shadow-md p-4 border border-gray-100 text-center">
            <div className="text-2xl font-bold text-green-600">{formatPercentage(item.value)}</div>
            <div className="text-xs text-gray-500 mt-1">{item.label}</div>
          </div>
        ))}
      </div>
      
      <BarChart 
        data={synergyData.map(item => ({ ...item, value: item.value * 100 }))}
        title="Synergy Metrics"
        color="from-green-500 to-teal-500"
      />
      
      <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-xl p-6 border border-green-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Synergy Insights</h3>
        <p className="text-gray-700">
          The overall synergy score is {formatPercentage(result.synergy_details?.overall_synergy_score || 0)} with 
          market similarity at {formatPercentage(result.synergy_details?.market_similarity || 0)}, 
          technology similarity at {formatPercentage(result.synergy_details?.tech_similarity || 0)}, 
          revenue synergy at {formatPercentage(result.synergy_details?.revenue_synergy_score || 0)}, and 
          cost synergy at {formatPercentage(result.synergy_details?.cost_synergy_score || 0)}.
        </p>
      </div>
    </div>
  );
};

// Valuation Agent Results
export const ValuationAgentResults = ({ result }) => {
  if (!result) return null;

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

  // Valuation data for visualization
  const valuationData = [
    { label: "Revenue TTM", value: result.valuation_forecast_usd ? result.valuation_forecast_usd / 5 : (result.financials_json?.revenue_ttm || 0) },
    { label: "Gross Margin", value: (result.financials_json?.gross_margin || 0) * 100 },
    { label: "EBITDA Margin", value: (result.financials_json?.ebitda_margin || 0) * 100 },
    { label: "Revenue Growth", value: (result.financials_json?.revenue_growth_mom || 0) }
  ];

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Valuation Agent Analysis</h2>
        <p className="text-gray-600">AI-powered valuation forecast and financial metrics</p>
      </div>
      
      {/* Valuation Forecast Display */}
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100">
        <div className="flex items-center mb-4">
          <span className="text-2xl mr-3">💰</span>
          <h3 className="text-xl font-semibold text-gray-900">Valuation Forecast</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <div className="text-sm text-gray-500 mb-1">USD Value</div>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(result.valuation_forecast_usd || 0)}
            </div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <div className="text-sm text-gray-500 mb-1">INR Value</div>
            <div className="text-2xl font-bold text-gray-900">
              {formatCurrency(result.valuation_forecast_inr || convertToINR(result.valuation_forecast_usd || 0), 'INR')}
            </div>
          </div>
        </div>
        
        <div className="mt-4 text-sm text-gray-600">
          <p>Based on revenue of {formatCurrency(result.financials_json?.revenue_ttm || 0)} and a multiple of {(result.financials_json?.revenue_multiple_proxy || 5).toFixed(2)}x</p>
        </div>
      </div>
      
      {/* Financial Metrics Visualization */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <BarChart 
          data={valuationData}
          title="Key Financial Metrics"
          color="from-green-500 to-teal-500"
        />
        
        {/* Valuation Components */}
        <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Valuation Components</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Revenue Multiple</span>
              <span className="font-medium text-gray-900">{(result.financials_json?.revenue_multiple_proxy || 0).toFixed(2)}x</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Gross Margin</span>
              <span className="font-medium text-gray-900">{(result.financials_json?.gross_margin || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">EBITDA Margin</span>
              <span className="font-medium text-gray-900">{(result.financials_json?.ebitda_margin || 0).toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Revenue Growth (MoM)</span>
              <span className="font-medium text-gray-900">{(result.financials_json?.revenue_growth_mom || 0).toFixed(2)}%</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Valuation Insights */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Valuation Insights</h3>
        <p className="text-gray-700">
          The valuation forecast of {formatCurrency(result.valuation_forecast_usd || 0)} is based on a 
          revenue multiple of {(result.financials_json?.revenue_multiple_proxy || 0).toFixed(2)}x applied to 
          trailing twelve months revenue of {formatCurrency(result.financials_json?.revenue_ttm || 0)}.
        </p>
        <p className="text-gray-700 mt-2">
          With a gross margin of {(result.financials_json?.gross_margin || 0).toFixed(1)}% and EBITDA margin of 
          {(result.financials_json?.ebitda_margin || 0).toFixed(1)}%, this represents a {result.valuation_forecast_usd && result.financials_json?.revenue_ttm ? 
          ((result.valuation_forecast_usd / result.financials_json.revenue_ttm).toFixed(2)) : '0'}x revenue multiple.
        </p>
      </div>
    </div>
  );
};

// Risk Agent Results
export const RiskAgentResults = ({ result }) => {
  if (!result) return null;

  // Format percentage
  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  // Risk data for visualization
  const riskData = [
    { label: "Funding Risk", value: result.risk?.funding_risk || 0 },
    { label: "Team Risk", value: result.risk?.team_risk || 0 },
    { label: "Synergy Risk", value: result.risk?.synergy_risk || 0 },
    { label: "Valuation Risk", value: result.risk?.valuation_risk || 0 },
    { label: "Combined Risk", value: result.risk?.combined_risk_score || 0 }
  ];

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Risk Agent Analysis</h2>
        <p className="text-gray-600">Evaluation of acquisition risks and potential issues</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {riskData.map((item, index) => (
          <div key={index} className="bg-white rounded-xl shadow-md p-4 border border-gray-100 text-center">
            <div className="text-2xl font-bold text-red-600">{formatPercentage(item.value)}</div>
            <div className="text-xs text-gray-500 mt-1">{item.label}</div>
          </div>
        ))}
      </div>
      
      <BarChart 
        data={riskData.map(item => ({ ...item, value: item.value * 100 }))}
        title="Risk Metrics"
        color="from-red-500 to-orange-500"
      />
      
      <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-xl p-6 border border-red-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Risk Insights</h3>
        <p className="text-gray-700">
          The combined risk score is {formatPercentage(result.risk?.combined_risk_score || 0)} with 
          funding risk at {formatPercentage(result.risk?.funding_risk || 0)}, 
          team risk at {formatPercentage(result.risk?.team_risk || 0)}, 
          synergy risk at {formatPercentage(result.risk?.synergy_risk || 0)}, and 
          valuation risk at {formatPercentage(result.risk?.valuation_risk || 0)}.
        </p>
      </div>
    </div>
  );
};

// Decision Agent Results
export const DecisionAgentResults = ({ result }) => {
  if (!result) return null;

  // Format percentage
  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  // Decision components data
  const decisionComponents = [
    { label: "M&A Likelihood", value: result.decision_score?.mna_likelihood || 0 },
    { label: "Synergy Component", value: result.decision_score?.synergy_component || 0 },
    { label: "Valuation Component", value: result.decision_score?.valuation_component || 0 },
    { label: "Team Component", value: result.decision_score?.team_component || 0 },
    { label: "Benchmark Component", value: result.decision_score?.benchmark_component || 0 },
    { label: "Risk Penalty", value: result.decision_score?.risk_penalty || 0 }
  ];

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Decision Agent Analysis</h2>
        <p className="text-gray-600">AI-powered acquisition decision recommendation</p>
      </div>
      
      {/* Decision Score Display */}
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-100">
        <div className="flex items-center mb-4">
          <span className="text-2xl mr-3">🧠</span>
          <h3 className="text-xl font-semibold text-gray-900">Decision Score</h3>
        </div>
        
        <div className="text-center">
          <div className="text-5xl font-bold text-purple-600">
            {result.decision_score?.acquisition_score ? result.decision_score.acquisition_score.toFixed(2) : 'N/A'}
          </div>
          <div className="text-gray-600 mt-2">Overall Acquisition Recommendation</div>
        </div>
      </div>
      
      {/* Decision Components Visualization */}
      <BarChart 
        data={decisionComponents.map(item => ({ ...item, value: item.value * 100 }))}
        title="Decision Components"
        color="from-purple-500 to-indigo-500"
      />
      
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-100 text-center">
          <div className="text-3xl font-bold text-green-600">
            {formatPercentage(result.mna_likelihood)}
          </div>
          <div className="text-gray-600 mt-1">M&A Likelihood</div>
        </div>
        
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100 text-center">
          <div className="text-3xl font-bold text-blue-600">
            {formatCurrency(result.valuation_forecast_usd || 0)}
          </div>
          <div className="text-gray-600 mt-1">Valuation Forecast</div>
        </div>
        
        <div className="bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl p-6 border border-yellow-100 text-center">
          <div className="text-3xl font-bold text-yellow-600">
            {formatPercentage(result.synergy_details?.overall_synergy_score || 0)}
          </div>
          <div className="text-gray-600 mt-1">Synergy Score</div>
        </div>
      </div>
      
      {/* Decision Insights */}
      <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Decision Insights</h3>
        <p className="text-gray-700">
          Based on the AI analysis, the acquisition decision score is 
          {result.decision_score?.acquisition_score ? result.decision_score.acquisition_score.toFixed(2) : 'N/A'} 
          with an M&A likelihood of {formatPercentage(result.mna_likelihood)}, 
          a valuation forecast of {formatCurrency(result.valuation_forecast_usd || 0)}, and 
          a synergy score of {formatPercentage(result.synergy_details?.overall_synergy_score || 0)}.
        </p>
        {result.explanation?.decision && (
          <div className="mt-3">
            <span className="font-medium">Recommendation: </span>
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              result.explanation.decision === 'ACQUIRE' 
                ? 'bg-green-100 text-green-800' 
                : result.explanation.decision === 'INVESTIGATE' 
                  ? 'bg-yellow-100 text-yellow-800' 
                  : 'bg-red-100 text-red-800'
            }`}>
              {result.explanation.decision}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

// Benchmark Agent Results
export const BenchmarkAgentResults = ({ result }) => {
  if (!result) return null;

  // Format percentage
  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  // Benchmark data for visualization
  const benchmarkData = [
    { 
      label: "Funding Benchmark", 
      value: result.benchmarks?.funding_benchmark_gap || 0,
      description: "Gap between current funding and industry benchmark ($5M)",
      benchmark: 5000000
    },
    { 
      label: "Team Experience", 
      value: result.benchmarks?.team_experience_gap || 0,
      description: "Gap between team experience and industry standard (7 years)",
      benchmark: 7
    },
    { 
      label: "Synergy Benchmark", 
      value: result.benchmarks?.synergy_benchmark_gap || 0,
      description: "Synergy score compared to industry average (0.6)",
      benchmark: 0.6
    },
    { 
      label: "Valuation Multiple", 
      value: result.benchmarks?.valuation_multiple_gap || 0,
      description: "Valuation multiple compared to peers (5.0x)",
      benchmark: 5.0
    },
    { 
      label: "Growth Benchmark", 
      value: result.benchmarks?.growth_benchmark_gap || 0,
      description: "Revenue growth compared to industry average (8%)",
      benchmark: 0.08
    },
    { 
      label: "Revenue TTM", 
      value: result.benchmarks?.revenue_ttm_gap || 0,
      description: "Trailing twelve months revenue compared to benchmark ($1.2M)",
      benchmark: 1200000
    }
  ];

  // Get status color based on benchmark gap
  const getStatusColor = (value) => {
    if (value > 0.2) return 'from-green-500 to-green-600';
    if (value > 0) return 'from-green-400 to-green-500';
    if (value < -0.2) return 'from-red-500 to-red-600';
    if (value < 0) return 'from-red-400 to-red-500';
    return 'from-gray-400 to-gray-500';
  };

  // Get status text based on benchmark gap
  const getStatusText = (value) => {
    if (value > 0.2) return 'Significantly Above Benchmark';
    if (value > 0) return 'Above Benchmark';
    if (value < -0.2) return 'Significantly Below Benchmark';
    if (value < 0) return 'Below Benchmark';
    return 'At Benchmark';
  };

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Benchmark Agent Analysis</h2>
        <p className="text-gray-600">Comparison of startup metrics against industry benchmarks</p>
      </div>
      
      {/* Key Insights */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Benchmark Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {benchmarkData.map((item, index) => (
            <div key={index} className="bg-white rounded-lg p-4 shadow-sm border border-gray-100">
              <div className="flex justify-between items-start">
                <h4 className="font-medium text-gray-900">{item.label}</h4>
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${getStatusColor(item.value)} text-white`}>
                  {formatPercentage(item.value)}
                </span>
              </div>
              <p className="text-sm text-gray-600 mt-2">{item.description}</p>
              <div className="mt-3 w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full bg-gradient-to-r ${getStatusColor(item.value)}`}
                  style={{ 
                    width: `${Math.min(100, Math.abs(item.value) * 100)}%`,
                    marginLeft: item.value < 0 ? `${100 - Math.min(100, Math.abs(item.value) * 100)}%` : '0'
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Detailed Benchmark Analysis */}
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Benchmark Analysis</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Metric</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Current Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Benchmark</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gap</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Funding</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  ${new Intl.NumberFormat('en-US').format(result.funding_json?.total_raised_usd || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">$5,000,000</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${result.benchmarks?.funding_benchmark_gap > 0 ? 'text-green-600' : result.benchmarks?.funding_benchmark_gap < 0 ? 'text-red-600' : 'text-gray-500'}`}>
                  {formatPercentage(result.benchmarks?.funding_benchmark_gap || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {getStatusText(result.benchmarks?.funding_benchmark_gap || 0)}
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Team Experience</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {(result.team_details?.avg_experience || 0).toFixed(1)} years
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">7.0 years</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${result.benchmarks?.team_experience_gap > 0 ? 'text-green-600' : result.benchmarks?.team_experience_gap < 0 ? 'text-red-600' : 'text-gray-500'}`}>
                  {formatPercentage(result.benchmarks?.team_experience_gap || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {getStatusText(result.benchmarks?.team_experience_gap || 0)}
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Synergy Score</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {(result.synergy_details?.overall_synergy_score || 0).toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">0.60</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${result.benchmarks?.synergy_benchmark_gap > 0 ? 'text-green-600' : result.benchmarks?.synergy_benchmark_gap < 0 ? 'text-red-600' : 'text-gray-500'}`}>
                  {formatPercentage(result.benchmarks?.synergy_benchmark_gap || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {getStatusText(result.benchmarks?.synergy_benchmark_gap || 0)}
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Valuation Multiple</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {(result.financials_json?.revenue_multiple_proxy || 0).toFixed(2)}x
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">5.00x</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${result.benchmarks?.valuation_multiple_gap > 0 ? 'text-green-600' : result.benchmarks?.valuation_multiple_gap < 0 ? 'text-red-600' : 'text-gray-500'}`}>
                  {formatPercentage(result.benchmarks?.valuation_multiple_gap || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {getStatusText(result.benchmarks?.valuation_multiple_gap || 0)}
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Revenue Growth</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatPercentage(result.financials_json?.revenue_growth_mom || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">8.0%</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${result.benchmarks?.growth_benchmark_gap > 0 ? 'text-green-600' : result.benchmarks?.growth_benchmark_gap < 0 ? 'text-red-600' : 'text-gray-500'}`}>
                  {formatPercentage(result.benchmarks?.growth_benchmark_gap || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {getStatusText(result.benchmarks?.growth_benchmark_gap || 0)}
                </td>
              </tr>
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Revenue TTM</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  ${new Intl.NumberFormat('en-US').format(result.financials_json?.revenue_ttm || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">$1,200,000</td>
                <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${result.benchmarks?.revenue_ttm_gap > 0 ? 'text-green-600' : result.benchmarks?.revenue_ttm_gap < 0 ? 'text-red-600' : 'text-gray-500'}`}>
                  {formatPercentage(result.benchmarks?.revenue_ttm_gap || 0)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {getStatusText(result.benchmarks?.revenue_ttm_gap || 0)}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      {/* Benchmark Summary */}
      <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-xl p-6 border border-green-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Benchmark Summary</h3>
        <p className="text-gray-700">
          This startup is performing {getStatusText((result.benchmarks?.funding_benchmark_gap || 0) + 
          (result.benchmarks?.team_experience_gap || 0) + 
          (result.benchmarks?.synergy_benchmark_gap || 0) + 
          (result.benchmarks?.valuation_multiple_gap || 0) + 
          (result.benchmarks?.growth_benchmark_gap || 0) + 
          (result.benchmarks?.revenue_ttm_gap || 0)) / 6} compared to industry benchmarks on average.
        </p>
        <p className="text-gray-700 mt-2">
          The benchmark component in the decision score contributes {formatPercentage(result.decision_score?.benchmark_component || 0)} 
          to the overall acquisition recommendation.
        </p>
      </div>
    </div>
  );
};

// Simple bar chart component for reuse
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
              <span className="text-sm font-medium text-gray-900">{typeof item.value === 'number' ? item.value.toFixed(2) : item.value}</span>
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