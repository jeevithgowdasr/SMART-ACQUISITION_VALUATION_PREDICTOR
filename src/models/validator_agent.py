import json
from typing import Dict, Any, List, Union


class ValidatorAgent:
    def __init__(self):
        """
        Initialize ValidatorAgent with no arguments.
        """
        pass
    
    def validate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize all required fields for agents.
        
        Args:
            input_data: Dictionary containing all input data
            
        Returns:
            Dictionary with validated and sanitized data
        """
        # Ensure input_data is a dict
        if not isinstance(input_data, dict):
            input_data = {}
        
        # Validate each required field
        funding_json = self._validate_funding(input_data.get("funding_json", {}))
        team_json = self._validate_team(input_data.get("team_json", {}))
        acquirer_json = self._validate_company(input_data.get("acquirer_json", {}))
        target_json = self._validate_company(input_data.get("target_json", {}))
        financials_json = self._validate_financials(input_data.get("financials_json", {}))
        
        return {
            "funding_json": funding_json,
            "team_json": team_json,
            "acquirer_json": acquirer_json,
            "target_json": target_json,
            "financials_json": financials_json
        }
    
    def _validate_funding(self, funding_data: Any) -> Dict[str, Any]:
        """
        Validate funding data.
        
        Args:
            funding_data: Funding data to validate
            
        Returns:
            Validated funding data
        """
        # Ensure funding_data is a dict
        if not isinstance(funding_data, dict):
            funding_data = {}
        
        # Validate rounds
        rounds = funding_data.get("rounds", [])
        if not isinstance(rounds, list):
            rounds = []
        
        # Validate each round
        validated_rounds = []
        for round_data in rounds:
            if not isinstance(round_data, dict):
                validated_rounds.append({
                    "amount": 0,
                    "type": "Unknown"
                })
                continue
                
            # Ensure amount exists
            amount = round_data.get("amount_usd")
            if amount is None:
                amount = round_data.get("amount", 0)
            
            # Ensure type exists
            round_type = round_data.get("type", "Unknown")
            
            validated_rounds.append({
                "amount": amount if isinstance(amount, (int, float)) else 0,
                "type": round_type if isinstance(round_type, str) else "Unknown"
            })
        
        return {
            "rounds": validated_rounds
        }
    
    def _validate_team(self, team_data: Any) -> Dict[str, Any]:
        """
        Validate team data.
        
        Args:
            team_data: Team data to validate
            
        Returns:
            Validated team data
        """
        # Ensure team_data is a dict
        if not isinstance(team_data, dict):
            team_data = {}
        
        # Validate founders
        founders = team_data.get("founders", [])
        if not isinstance(founders, list):
            founders = []
        
        # Validate each founder
        validated_founders = []
        for founder_data in founders:
            if not isinstance(founder_data, dict):
                validated_founders.append({
                    "experience_years": 0,
                    "has_exit": False
                })
                continue
                
            experience_years = founder_data.get("experience_years", 0)
            has_exit = founder_data.get("has_exit", False)
            
            validated_founders.append({
                "experience_years": experience_years if isinstance(experience_years, (int, float)) else 0,
                "has_exit": has_exit if isinstance(has_exit, bool) else False
            })
        
        return {
            "founders": validated_founders
        }
    
    def _validate_company(self, company_data: Any) -> Dict[str, Any]:
        """
        Validate company data (acquirer or target).
        
        Args:
            company_data: Company data to validate
            
        Returns:
            Validated company data
        """
        # Ensure company_data is a dict
        if not isinstance(company_data, dict):
            company_data = {}
        
        industry = company_data.get("industry", "Unknown")
        market = company_data.get("market", "Unknown")
        tech_stack = company_data.get("tech_stack", [])
        team_size = company_data.get("team_size", 0)
        
        return {
            "industry": industry if isinstance(industry, str) else "Unknown",
            "market": market if isinstance(market, str) else "Unknown",
            "tech_stack": tech_stack if isinstance(tech_stack, list) else [],
            "team_size": team_size if isinstance(team_size, (int, float)) else 0
        }
    
    def _validate_financials(self, financials_data: Any) -> Dict[str, Any]:
        """
        Validate financials data.
        
        Args:
            financials_data: Financials data to validate
            
        Returns:
            Validated financials data
        """
        # Ensure financials_data is a dict
        if not isinstance(financials_data, dict):
            financials_data = {}
        
        monthly_revenue = financials_data.get("monthly_revenue_usd", 0)
        annual_revenue = financials_data.get("annual_revenue_usd", 0)
        revenue_growth = financials_data.get("revenue_growth_mom", 0.0)
        gross_margin = financials_data.get("gross_margin", 0.0)
        ebitda_margin = financials_data.get("ebitda_margin", 0.0)
        
        return {
            "monthly_revenue_usd": monthly_revenue if isinstance(monthly_revenue, (int, float)) else 0,
            "annual_revenue_usd": annual_revenue if isinstance(annual_revenue, (int, float)) else 0,
            "revenue_growth_mom": revenue_growth if isinstance(revenue_growth, (int, float)) else 0.0,
            "gross_margin": gross_margin if isinstance(gross_margin, (int, float)) else 0.0,
            "ebitda_margin": ebitda_margin if isinstance(ebitda_margin, (int, float)) else 0.0
        }
    
    @staticmethod
    def load() -> 'ValidatorAgent':
        """
        Static method to create and return a ValidatorAgent instance.
        
        Returns:
            ValidatorAgent: A new ValidatorAgent instance
        """
        return ValidatorAgent()