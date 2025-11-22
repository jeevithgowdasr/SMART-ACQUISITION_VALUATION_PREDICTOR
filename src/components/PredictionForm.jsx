import React, { useState } from 'react';

const PredictionForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    // Startup 1 (Target Company)
    startup1: {
      companyName: '',
      totalFunding: '',
      employees: '',
      founderExperience: '',
      hasExit: 'no',
      fundingRound: 'Series A',
      // Enhanced team member data
      teamMembers: [
        { name: '', experience: '', role: 'Founder', education: '', hasExit: 'no' }
      ]
    },
    // Startup 2 (Acquirer Company)
    startup2: {
      companyName: '',
      totalFunding: '',
      employees: '',
      founderExperience: '',
      hasExit: 'no',
      fundingRound: 'Series A',
      // Enhanced team member data
      teamMembers: [
        { name: '', experience: '', role: 'Founder', education: '', hasExit: 'no' }
      ]
    },
    // Industry & Financial Information
    acquirerIndustry: 'Technology',
    targetIndustry: 'Technology',
    acquirerRevenue: '',
    targetRevenue: '',
    revenueTTM: '',
    revenueGrowth: '',
    grossMargin: '',
    ebitdaMargin: ''
  });

  const handleChange = (e, startup = null, field = null, index = null) => {
    const { name, value } = e.target;
    
    if (field === 'teamMembers' && index !== null) {
      // Handle team member changes
      setFormData(prev => ({
        ...prev,
        [startup]: {
          ...prev[startup],
          teamMembers: prev[startup].teamMembers.map((member, i) => 
            i === index ? { ...member, [name]: value } : member
          )
        }
      }));
    } else if (startup) {
      setFormData(prev => ({
        ...prev,
        [startup]: {
          ...prev[startup],
          [name]: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const addTeamMember = (startup) => {
    setFormData(prev => ({
      ...prev,
      [startup]: {
        ...prev[startup],
        teamMembers: [
          ...prev[startup].teamMembers,
          { name: '', experience: '', role: 'Employee', education: '', hasExit: 'no' }
        ]
      }
    }));
  };

  const removeTeamMember = (startup, index) => {
    setFormData(prev => ({
      ...prev,
      [startup]: {
        ...prev[startup],
        teamMembers: prev[startup].teamMembers.filter((_, i) => i !== index)
      }
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  // Form sections with enhanced styling
  const formSections = [
    {
      title: "Target Company (Startup to be Acquired)",
      icon: "🎯",
      startup: "startup1",
      fields: [
        { id: "companyName", label: "Company Name", type: "text", placeholder: "Enter company name" },
        { id: "totalFunding", label: "Total Funding Raised (USD)", type: "number", placeholder: "e.g., 1000000" },
        { id: "employees", label: "Number of Employees", type: "number", placeholder: "e.g., 50" },
        { id: "founderExperience", label: "Founder Experience (Years)", type: "number", placeholder: "e.g., 10" },
        { id: "hasExit", label: "Founder Previous Exit", type: "select", options: [
          { value: "no", label: "No" },
          { value: "yes", label: "Yes" }
        ]},
        { id: "fundingRound", label: "Latest Funding Round", type: "select", options: [
          { value: "Pre-Seed", label: "Pre-Seed" },
          { value: "Seed", label: "Seed" },
          { value: "Series A", label: "Series A" },
          { value: "Series B", label: "Series B" },
          { value: "Series C", label: "Series C" },
          { value: "Series D+", label: "Series D+" }
        ]}
      ]
    },
    {
      title: "Acquirer Company",
      icon: "🏢",
      startup: "startup2",
      fields: [
        { id: "companyName", label: "Company Name", type: "text", placeholder: "Enter company name" },
        { id: "totalFunding", label: "Total Funding Raised (USD)", type: "number", placeholder: "e.g., 50000000" },
        { id: "employees", label: "Number of Employees", type: "number", placeholder: "e.g., 500" },
        { id: "founderExperience", label: "Founder Experience (Years)", type: "number", placeholder: "e.g., 15" },
        { id: "hasExit", label: "Founder Previous Exit", type: "select", options: [
          { value: "no", label: "No" },
          { value: "yes", label: "Yes" }
        ]},
        { id: "fundingRound", label: "Latest Funding Round", type: "select", options: [
          { value: "Pre-Seed", label: "Pre-Seed" },
          { value: "Seed", label: "Seed" },
          { value: "Series A", label: "Series A" },
          { value: "Series B", label: "Series B" },
          { value: "Series C", label: "Series C" },
          { value: "Series D+", label: "Series D+" }
        ]}
      ]
    },
    {
      title: "Industry & Financial Information",
      icon: "📊",
      fields: [
        { id: "acquirerIndustry", label: "Acquirer Industry", type: "select", options: [
          { value: "Technology", label: "Technology" },
          { value: "Healthcare", label: "Healthcare" },
          { value: "Finance", label: "Finance" },
          { value: "Consumer", label: "Consumer" },
          { value: "Energy", label: "Energy" },
          { value: "Manufacturing", label: "Manufacturing" }
        ]},
        { id: "targetIndustry", label: "Target Industry", type: "select", options: [
          { value: "Technology", label: "Technology" },
          { value: "Healthcare", label: "Healthcare" },
          { value: "Finance", label: "Finance" },
          { value: "Consumer", label: "Consumer" },
          { value: "Energy", label: "Energy" },
          { value: "Manufacturing", label: "Manufacturing" }
        ]},
        { id: "acquirerRevenue", label: "Acquirer Revenue (USD)", type: "number", placeholder: "e.g., 100000000" },
        { id: "targetRevenue", label: "Target Revenue (USD)", type: "number", placeholder: "e.g., 5000000" },
        { id: "revenueTTM", label: "Revenue (TTM) USD", type: "number", placeholder: "e.g., 2000000" },
        { id: "revenueGrowth", label: "Revenue Growth (MoM %)", type: "number", placeholder: "e.g., 15" },
        { id: "grossMargin", label: "Gross Margin (%)", type: "number", placeholder: "e.g., 75" },
        { id: "ebitdaMargin", label: "EBITDA Margin (%)", type: "number", placeholder: "e.g., 20" }
      ]
    }
  ];

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6 md:p-8 border border-gray-100 animate-fadeIn">
      <div className="mb-8 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">M&A Analysis: Compare Two Startups</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Enter details for both the target company (to be acquired) and the acquirer company to get AI-powered acquisition analysis
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {formSections.map((section, index) => (
          <div 
            key={section.title}
            className="border border-gray-200 rounded-xl p-6 bg-gradient-to-br from-gray-50 to-white shadow-sm hover:shadow-md transition-all duration-300"
          >
            <div className="flex items-center mb-6">
              <span className="text-2xl mr-3">{section.icon}</span>
              <h3 className="text-xl font-semibold text-gray-900">{section.title}</h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {section.fields.map((field) => (
                <div key={field.id} className="animate-slideUp">
                  <label htmlFor={field.id} className="block text-sm font-medium text-gray-700 mb-2">
                    {field.label}
                  </label>
                  
                  {field.type === "select" ? (
                    <select
                      id={field.id}
                      name={field.id}
                      value={section.startup ? formData[section.startup][field.id] : formData[field.id]}
                      onChange={(e) => handleChange(e, section.startup)}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 bg-white"
                    >
                      {field.options.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <input
                      type={field.type}
                      id={field.id}
                      name={field.id}
                      value={section.startup ? formData[section.startup][field.id] : formData[field.id]}
                      onChange={(e) => handleChange(e, section.startup)}
                      placeholder={field.placeholder}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-300"
                    />
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
        
        {/* Enhanced Team Member Sections */}
        {['startup1', 'startup2'].map((startup) => (
          <div 
            key={`${startup}-team`}
            className="border border-gray-200 rounded-xl p-6 bg-gradient-to-br from-blue-50 to-indigo-50 shadow-sm hover:shadow-md transition-all duration-300"
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center">
                <span className="text-2xl mr-3">👥</span>
                <h3 className="text-xl font-semibold text-gray-900">
                  {startup === 'startup1' ? 'Target Company' : 'Acquirer Company'} Team Members
                </h3>
              </div>
              <button
                type="button"
                onClick={() => addTeamMember(startup)}
                className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Add Member
              </button>
            </div>
            
            <div className="space-y-4">
              {formData[startup].teamMembers.map((member, index) => (
                <div key={index} className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4 bg-white rounded-lg border border-gray-200">
                  <div className="md:col-span-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                    <input
                      type="text"
                      name="name"
                      value={member.name}
                      onChange={(e) => handleChange(e, startup, 'teamMembers', index)}
                      placeholder="Team member name"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div className="md:col-span-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Experience (Years)</label>
                    <input
                      type="number"
                      name="experience"
                      value={member.experience}
                      onChange={(e) => handleChange(e, startup, 'teamMembers', index)}
                      placeholder="e.g., 5"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div className="md:col-span-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                    <select
                      name="role"
                      value={member.role}
                      onChange={(e) => handleChange(e, startup, 'teamMembers', index)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="Founder">Founder</option>
                      <option value="CTO">CTO</option>
                      <option value="CEO">CEO</option>
                      <option value="COO">COO</option>
                      <option value="CFO">CFO</option>
                      <option value="Employee">Employee</option>
                    </select>
                  </div>
                  <div className="md:col-span-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Education</label>
                    <input
                      type="text"
                      name="education"
                      value={member.education}
                      onChange={(e) => handleChange(e, startup, 'teamMembers', index)}
                      placeholder="e.g., MBA, PhD"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div className="md:col-span-1 flex items-end">
                    <div className="flex items-center w-full">
                      <label className="block text-sm font-medium text-gray-700 mr-2">Previous Exit?</label>
                      <select
                        name="hasExit"
                        value={member.hasExit}
                        onChange={(e) => handleChange(e, startup, 'teamMembers', index)}
                        className="w-full px-2 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="no">No</option>
                        <option value="yes">Yes</option>
                      </select>
                      {formData[startup].teamMembers.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeTeamMember(startup, index)}
                          className="ml-2 p-2 text-red-600 hover:text-red-800 focus:outline-none"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
        
        <div className="flex justify-center pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-700 hover:from-blue-700 hover:to-purple-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing with AI Agents...
              </>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" className="mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5" />
                </svg>
                Run Full AI Analysis
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PredictionForm;