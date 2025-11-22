import React, { useState } from 'react';
import axios from 'axios';

const CompanyLookup = () => {
  const [companyName, setCompanyName] = useState('');
  const [industry, setIndustry] = useState('');
  const [acquirerName, setAcquirerName] = useState('');
  const [competitors, setCompetitors] = useState([]);
  const [targets, setTargets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('competitors');

  const API_BASE_URL = '/api';

  const searchCompetitors = async () => {
    if (!companyName) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/competitors/${encodeURIComponent(companyName)}`, {
        params: { industry: industry || undefined }
      });
      setCompetitors(response.data.competitors || []);
    } catch (error) {
      console.error('Error fetching competitors:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchAcquisitionTargets = async () => {
    if (!acquirerName) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/acquisition-targets/${encodeURIComponent(acquirerName)}`);
      setTargets(response.data.targets || []);
    } catch (error) {
      console.error('Error fetching acquisition targets:', error);
    } finally {
      setLoading(false);
    }
  };

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
    <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Company Lookup</h2>
        <p className="text-gray-600 mt-1">Find competitors and acquisition targets from Crunchbase data</p>
      </div>

      {/* Tab Navigation */}
      <div className="flex border-b border-gray-200 mb-6">
        <button
          onClick={() => setActiveTab('competitors')}
          className={`px-4 py-2 font-medium text-sm ${
            activeTab === 'competitors'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Competitors
        </button>
        <button
          onClick={() => setActiveTab('acquisitions')}
          className={`px-4 py-2 font-medium text-sm ${
            activeTab === 'acquisitions'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Acquisition Targets
        </button>
      </div>

      {/* Competitors Tab */}
      {activeTab === 'competitors' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="companyName" className="block text-sm font-medium text-gray-700 mb-1">
                Company Name
              </label>
              <input
                type="text"
                id="companyName"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter company name"
              />
            </div>
            <div>
              <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-1">
                Industry (Optional)
              </label>
              <select
                id="industry"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Industries</option>
                <option value="Technology">Technology</option>
                <option value="Healthcare">Healthcare</option>
                <option value="Finance">Finance</option>
                <option value="Consumer">Consumer</option>
                <option value="Energy">Energy</option>
                <option value="Manufacturing">Manufacturing</option>
              </select>
            </div>
          </div>
          <button
            onClick={searchCompetitors}
            disabled={loading || !companyName}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Searching...
              </>
            ) : (
              'Find Competitors'
            )}
          </button>

          {competitors.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Competitors Found</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {competitors.map((competitor, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="font-medium text-gray-900">{competitor.name}</div>
                    <div className="text-sm text-gray-500 mt-1">{competitor.domain || 'No domain'}</div>
                    <div className="mt-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {formatCurrency(competitor.funding_total_usd || 0)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Acquisitions Tab */}
      {activeTab === 'acquisitions' && (
        <div className="space-y-6">
          <div>
            <label htmlFor="acquirerName" className="block text-sm font-medium text-gray-700 mb-1">
              Acquirer Company Name
            </label>
            <input
              type="text"
              id="acquirerName"
              value={acquirerName}
              onChange={(e) => setAcquirerName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter acquirer company name"
            />
          </div>
          <button
            onClick={searchAcquisitionTargets}
            disabled={loading || !acquirerName}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Searching...
              </>
            ) : (
              'Find Acquisition Targets'
            )}
          </button>

          {targets.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Past Acquisitions</h3>
              <div className="space-y-4">
                {targets.map((target, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between">
                      <div>
                        <div className="font-medium text-gray-900">{target.name}</div>
                        <div className="text-sm text-gray-500">{target.acquired_at || 'Date unknown'}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-medium text-gray-900">
                          {formatCurrency(target.price_amount || 0)}
                        </div>
                        <div className="text-sm text-gray-500">
                          {formatCurrency(convertToINR(target.price_amount || 0), 'INR')}
                        </div>
                      </div>
                    </div>
                    <div className="text-sm text-gray-500 mt-2">{target.domain || 'No domain'}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default CompanyLookup;