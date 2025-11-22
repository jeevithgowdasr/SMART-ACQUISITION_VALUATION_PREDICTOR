import React, { useState } from 'react';

const Header = ({ activeTab, setActiveTab }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'form', label: 'Full Analysis', icon: '🔍' },
    { id: 'funding', label: 'Funding Agent', icon: '💰' },
    { id: 'team', label: 'Team Agent', icon: '👥' },
    { id: 'synergy', label: 'Synergy Agent', icon: '🔗' },
    { id: 'valuation', label: 'Valuation Agent', icon: '📈' },
    { id: 'risk', label: 'Risk Agent', icon: '⚠️' },
    { id: 'decision', label: 'Decision Agent', icon: '🧠' }
  ];

  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-700 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="bg-white p-2 rounded-lg shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Smart Acquirer</h1>
              <p className="text-xs text-blue-100">AI-Powered M&A Analysis Platform</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 transform hover:scale-105 ${
                  activeTab === item.id
                    ? 'bg-white text-blue-600 shadow-md'
                    : 'text-blue-100 hover:bg-blue-500 hover:bg-opacity-30'
                }`}
              >
                <span className="mr-1">{item.icon}</span>
                {item.label}
              </button>
            ))}
          </nav>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-white p-2 rounded-md hover:bg-blue-500 hover:bg-opacity-30"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-blue-500 border-opacity-30">
            <div className="grid grid-cols-2 gap-2">
              {navItems.map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveTab(item.id);
                    setIsMenuOpen(false);
                  }}
                  className={`px-3 py-2 rounded-lg text-sm font-medium text-left transition-all duration-300 ${
                    activeTab === item.id
                      ? 'bg-white text-blue-600 shadow-md'
                      : 'text-blue-100 hover:bg-blue-500 hover:bg-opacity-30'
                  }`}
                >
                  <span className="mr-1">{item.icon}</span>
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;