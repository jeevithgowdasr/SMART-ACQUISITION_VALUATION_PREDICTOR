import json
import pandas as pd
import os
from typing import Dict, Any


class BusinessModelAgent:
    def __init__(self):
        """
        Initialize BusinessModelAgent with no arguments.
        This agent evaluates startup business models using insights from the VC evaluation dataset.
        """
        # Load the VC evaluation dataset
        self._load_vc_data()
    
    def _load_vc_data(self):
        """Load the VC evaluation dataset"""
        try:
            # Check if the dataset files exist in the project root
            csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'enhanced_training_data.csv')
            if os.path.exists(csv_path):
                self.vc_data = pd.read_csv(csv_path)
                # Filter for business model related evaluations
                self.business_model_data = self.vc_data[
                    self.vc_data['evaluation_aspect'] == 'business_model'
                ]
            else:
                self.vc_data = pd.DataFrame()
                self.business_model_data = pd.DataFrame()
        except Exception as e:
            print(f"Warning: Could not load VC evaluation data: {e}")
            self.vc_data = pd.DataFrame()
            self.business_model_data = pd.DataFrame()
    
    def transform(self, funding_json: dict, team_json: dict, financials_json: dict) -> dict:
        """
        Evaluate the business model based on funding, team, and financial data.
        
        Args:
            funding_json: Dictionary containing funding history
            team_json: Dictionary containing team information
            financials_json: Dictionary containing financial metrics
            
        Returns:
            Dictionary with business model evaluation scores
        """
        # Extract relevant features
        rounds = funding_json.get('rounds', [])
        num_rounds = len(rounds)
        
        # Fix: Properly handle string amounts in funding rounds
        total_raised = 0.0
        for round_info in rounds:
            amount = round_info.get('amount', 0)
            # Handle both string and numeric amounts
            if isinstance(amount, str):
                # Remove non-numeric characters and convert to float
                amount = ''.join(filter(str.isdigit, amount)) or '0'
                amount = float(amount)
            else:
                amount = float(amount)
            total_raised += amount
        
        # Team metrics
        founders = team_json.get('founders', [])
        founder_count = len(founders)
        avg_experience = sum(f.get('experience_years', 0) for f in founders) / max(1, len(founders))
        
        # Financial metrics
        monthly_revenue = financials_json.get('monthly_revenue_usd', 0)
        annual_revenue = financials_json.get('annual_revenue_usd', monthly_revenue * 12)
        gross_margin = financials_json.get('gross_margin', 0)
        
        # Calculate business model scores
        # Funding efficiency score (more rounds with less total funding might indicate efficiency)
        funding_efficiency = 1.0 if num_rounds > 0 else 0.0
        if num_rounds > 0:
            avg_round_size = total_raised / num_rounds
            # Normalize by a reasonable round size ($5M)
            funding_efficiency = min(1.0, avg_round_size / 5000000)
        
        # Team strength for business model execution
        team_strength = min(1.0, (founder_count * 0.3 + avg_experience * 0.7) / 10)
        
        # Revenue model sustainability (higher margin and revenue indicate better sustainability)
        revenue_sustainability = min(1.0, (gross_margin * 0.7 + (annual_revenue / 1000000) * 0.3))
        
        # Overall business model score
        business_model_score = (
            funding_efficiency * 0.3 +
            team_strength * 0.3 +
            revenue_sustainability * 0.4
        )
        
        return {
            "business_model_score": float(business_model_score),
            "funding_efficiency": float(funding_efficiency),
            "team_strength_for_execution": float(team_strength),
            "revenue_sustainability": float(revenue_sustainability),
            "num_funding_rounds": int(num_rounds),
            "total_raised_usd": float(total_raised),
            "founder_count": int(founder_count),
            "avg_founder_experience": float(avg_experience),
            "annual_revenue_usd": float(annual_revenue),
            "gross_margin": float(gross_margin)
        }
    
    def get_insights(self) -> dict:
        """
        Get insights from the VC evaluation dataset related to business models.
        
        Returns:
            Dictionary with business model insights
        """
        if self.business_model_data.empty:
            return {"insights": "No business model evaluation data available"}
        
        # Get sample completions for business model evaluations
        sample_completions = self.business_model_data['completion'].tolist()[:3]
        
        return {
            "insights": "Business model evaluation insights from VC practices",
            "key_patterns": [
                "Scalability through innovative approaches addressing market pain points",
                "Sustainable revenue models with subscription-based services",
                "Strong competitive advantages through patented technology",
                "Clear paths to profitability with diversified revenue streams"
            ],
            "sample_evaluations": sample_completions
        }
    
    @staticmethod
    def load() -> 'BusinessModelAgent':
        """
        Static method to create and return a BusinessModelAgent instance.
        
        Returns:
            BusinessModelAgent: A new BusinessModelAgent instance
        """
        return BusinessModelAgent()


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Sample data for testing
    funding_data = {
        "rounds": [
            {"type": "Seed", "amount": 1000000},
            {"type": "Series A", "amount": 5000000}
        ]
    }
    
    team_data = {
        "founders": [
            {"experience_years": 5, "has_exit": True},
            {"experience_years": 3, "has_exit": False}
        ]
    }
    
    financials_data = {
        "monthly_revenue_usd": 10000,
        "annual_revenue_usd": 120000,
        "revenue_growth_mom": 5.0,
        "gross_margin": 0.7
    }
    
    # Create and use the agent
    agent = BusinessModelAgent()
    result = agent.transform(funding_data, team_data, financials_data)
    print("Business Model Evaluation:")
    print(json.dumps(result, indent=2))
    
    # Get insights
    insights = agent.get_insights()
    print("\nBusiness Model Insights:")
    print(json.dumps(insights, indent=2))