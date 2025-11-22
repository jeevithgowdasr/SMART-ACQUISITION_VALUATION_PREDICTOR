import React, { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';
import AgentDashboard from './components/AgentDashboard';
import { FundingAgentResults, TeamAgentResults, SynergyAgentResults, ValuationAgentResults, RiskAgentResults, DecisionAgentResults, BenchmarkAgentResults } from './components/AgentResults';
import './App.css';

const API_BASE_URL = '/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [predictionResult, setPredictionResult] = useState(null);
  const [agentResults, setAgentResults] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState(null); // Store form data for comparison

  const handlePredictionSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    setFormData(formData); // Store form data for comparison view
    
    try {
      // Transform form data to match backend expected format
      // Enhanced team data processing
      const startup1TeamMembers = formData.startup1.teamMembers || [];
      const startup2TeamMembers = formData.startup2.teamMembers || [];
      
      const payload = {
        funding_json: {
          rounds: [
            {
              type: formData.startup1.fundingRound || "Series A",
              amount: parseFloat(formData.startup1.totalFunding) || 0
            }
          ]
        },
        team_json: {
          founders: startup1TeamMembers.map(member => ({
            experience_years: parseInt(member.experience) || 0,
            has_exit: member.hasExit === 'yes',
            role: member.role || 'Employee',
            education: member.education || ''
          })),
          estimated_team_size: parseInt(formData.startup1.employees) || 0
        },
        acquirer_json: {
          industry: formData.acquirerIndustry || "Technology",
          revenue: parseFloat(formData.acquirerRevenue) || 0
        },
        target_json: {
          industry: formData.targetIndustry || "Technology",
          revenue: parseFloat(formData.targetRevenue) || 0
        },
        financials_json: {
          revenue_ttm: parseFloat(formData.revenueTTM) || 0,
          revenue_growth_mom: parseFloat(formData.revenueGrowth) || 0,
          gross_margin: parseFloat(formData.grossMargin) || 0,
          ebitda_margin: parseFloat(formData.ebitdaMargin) || 0
        }
      };

      const response = await axios.post(`${API_BASE_URL}/predict`, payload);
      setPredictionResult(response.data);
      setActiveTab('analysis');
    } catch (err) {
      console.error('Prediction failed:', err);
      setError(err.response?.data?.detail || err.message || 'An error occurred during prediction');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAgentExecution = async (agentType) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // For demo purposes, we'll use the same payload but focus on specific agent results
      const payload = {
        funding_json: {
          rounds: [{ type: "Series A", amount: 1000000 }]
        },
        team_json: {
          founders: [
            { 
              experience_years: 5, 
              has_exit: false,
              role: "Founder",
              education: "MBA"
            },
            { 
              experience_years: 10, 
              has_exit: true,
              role: "CTO",
              education: "PhD"
            }
          ],
          estimated_team_size: 50
        },
        acquirer_json: { industry: "Technology", revenue: 100000000 },
        target_json: { industry: "Technology", revenue: 5000000 },
        financials_json: {
          revenue_ttm: 2000000,
          revenue_growth_mom: 0.15,
          gross_margin: 0.75,
          ebitda_margin: 0.20
        }
      };

      const response = await axios.post(`${API_BASE_URL}/predict`, payload);
      
      // Store results for the specific agent
      setAgentResults(prev => ({
        ...prev,
        [agentType]: response.data
      }));
      
      setActiveTab(agentType);
    } catch (err) {
      console.error(`${agentType} execution failed:`, err);
      setError(err.response?.data?.detail || err.message || `An error occurred during ${agentType} execution`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setPredictionResult(null);
    setAgentResults({});
    setFormData(null);
    setError(null);
    // Navigate back to the form when resetting from analysis view
    setActiveTab('form');
  };

  const handleBackToForm = () => {
    // Navigate back to the main form
    setActiveTab('form');
  };

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return <AgentDashboard onAgentSelect={setActiveTab} />;
      case 'analysis':
        return (
          <ResultsDisplay 
            result={predictionResult}
            formData={formData}
            onReset={handleReset}
          />
        );
      case 'form':
        return (
          <PredictionForm 
            onSubmit={handlePredictionSubmit}
            isLoading={isLoading}
          />
        );
      case 'funding':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Funding Agent Results</h2>
              <button
                onClick={handleBackToForm}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105"
              >
                Back to Form
              </button>
            </div>
            <FundingAgentResults result={agentResults.funding || predictionResult} />
          </div>
        );
      case 'team':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Team Agent Results</h2>
              <button
                onClick={handleBackToForm}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105"
              >
                Back to Form
              </button>
            </div>
            <TeamAgentResults result={agentResults.team || predictionResult} />
          </div>
        );
      case 'synergy':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Synergy Agent Results</h2>
              <button
                onClick={handleBackToForm}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105"
              >
                Back to Form
              </button>
            </div>
            <SynergyAgentResults result={agentResults.synergy || predictionResult} />
          </div>
        );
      case 'valuation':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Valuation Agent Results</h2>
              <button
                onClick={handleBackToForm}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105"
              >
                Back to Form
              </button>
            </div>
            <ValuationAgentResults result={agentResults.valuation || predictionResult} />
          </div>
        );
      case 'risk':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Risk Agent Results</h2>
              <button
                onClick={handleBackToForm}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105"
              >
                Back to Form
              </button>
            </div>
            <RiskAgentResults result={agentResults.risk || predictionResult} />
          </div>
        );
      case 'decision':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Decision Agent Results</h2>
              <button
                onClick={handleBackToForm}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105"
              >
                Back to Form
              </button>
            </div>
            <DecisionAgentResults result={agentResults.decision || predictionResult} />
          </div>
        );
      case 'benchmark':
        return (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Benchmark Agent Results</h2>
              <button
                onClick={handleBackToForm}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 transform hover:scale-105"
              >
                Back to Form
              </button>
            </div>
            <BenchmarkAgentResults result={agentResults.benchmark || predictionResult} />
          </div>
        );
      default:
        return (
          <PredictionForm 
            onSubmit={handlePredictionSubmit}
            isLoading={isLoading}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="container mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg animate-shake">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-red-800 font-medium">Error</h3>
                <p className="text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}
        
        {renderActiveTab()}
      </main>
    </div>
  );
}

export default App;