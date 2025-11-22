class ValuationAgent:
    def __init__(self):
        """
        Initialize ValuationAgent with no arguments.
        """
        pass
    
    def transform(self, financials: dict) -> dict:
        """
        Transform financial data into valuation features.
        
        Args:
            financials: Dictionary containing financial metrics
            
        Returns:
            Dictionary with valuation features
        """
        # Extract or compute revenue_ttm
        if 'annual_revenue_usd' in financials:
            revenue_ttm = float(financials['annual_revenue_usd'])
        elif 'monthly_revenue_usd' in financials:
            revenue_ttm = float(financials['monthly_revenue_usd']) * 12
        else:
            revenue_ttm = 0.0
            
        # Handle revenue_growth_mom (pass-through or default)
        revenue_growth_mom = float(financials.get('revenue_growth_mom', 0.0))
        
        # Handle gross_margin
        gross_margin = float(financials.get('gross_margin', 0.0))
        
        # Handle ebitda_margin (default to 0 if missing)
        ebitda_margin = float(financials.get('ebitda_margin', 0.0))
        
        # Calculate revenue_multiple_proxy using heuristic
        # Baseline 3-10 scaled by growth (higher growth = higher multiple)
        baseline_multiple = 5.0  # Midpoint of 3-10 range
        growth_factor = 1 + (revenue_growth_mom / 100)  # Convert percentage to factor
        # Cap the growth factor to prevent extreme multiples
        growth_factor = min(growth_factor, 2.0)  # Cap at 2x (100% growth)
        revenue_multiple_proxy = baseline_multiple * growth_factor
        # Ensure reasonable bounds for multiple
        revenue_multiple_proxy = max(1.0, min(revenue_multiple_proxy, 15.0))
        
        # Calculate valuation_proxy_current
        valuation_proxy_current = revenue_ttm * revenue_multiple_proxy
        
        return {
            'revenue_ttm': revenue_ttm,
            'revenue_growth_mom': revenue_growth_mom,
            'gross_margin': gross_margin,
            'ebitda_margin': ebitda_margin,
            'revenue_multiple_proxy': revenue_multiple_proxy,
            'valuation_proxy_current': valuation_proxy_current
        }
    
    @staticmethod
    def load() -> 'ValuationAgent':
        """
        Static method to create and return a ValuationAgent instance.
        
        Returns:
            ValuationAgent: A new ValuationAgent instance
        """
        return ValuationAgent()