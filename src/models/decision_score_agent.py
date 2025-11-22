import json
from typing import Dict, Any
import numpy as np

class DecisionScoreAgent:
    def __init__(self):
        """
        Initialize DecisionScoreAgent with no arguments.
        """
        pass
    
    def compute(self, features: Dict[str, Any]) -> Dict[str, float]:
        """
        Compute a final acquisition score from various features.
        
        Args:
            features: Dictionary containing various features
            
        Returns:
            Dictionary with acquisition score and components
        """
        # Step 1: Normalize relevant features
        valuation_proxy_current = features.get("valuation_proxy_current", 0)
        valuation_forecast_usd = features.get("valuation_forecast_usd", 0)
        
        # Calculate valuation ratio
        if valuation_proxy_current + 1 != 0:
            valuation_ratio = valuation_forecast_usd / (valuation_proxy_current + 1)
        else:
            valuation_ratio = 0
            
        # Clamp ratio between 0 and 2
        valuation_ratio = max(0, min(2, valuation_ratio))
        
        # Convert to normalized score
        if valuation_ratio <= 1.0:
            valuation_score = 1.0
        else:
            valuation_score = max(0, 2.0 - valuation_ratio)
        
        # Step 2: Handle missing values with better defaults
        # Enhanced M&A likelihood calculation that doesn't rely solely on the model
        mna_likelihood = self._calculate_balanced_mna_likelihood(features)
        overall_synergy_score = features.get("overall_synergy_score", 0.5)
        team_strength_score = features.get("team_strength_score", 0.5)
        combined_risk_score = features.get("combined_risk_score", 0.3)
        
        # Get benchmark gaps with defaults
        funding_benchmark_gap = features.get("funding_benchmark_gap", 0)
        team_experience_gap = features.get("team_experience_gap", 0)
        synergy_benchmark_gap = features.get("synergy_benchmark_gap", 0)
        valuation_multiple_gap = features.get("valuation_multiple_gap", 0)
        growth_benchmark_gap = features.get("growth_benchmark_gap", 0)
        revenue_ttm_gap = features.get("revenue_ttm_gap", 0)
        
        # Step 3: Compute benchmark_score
        gaps = [
            funding_benchmark_gap,
            team_experience_gap,
            synergy_benchmark_gap,
            valuation_multiple_gap,
            growth_benchmark_gap,
            revenue_ttm_gap
        ]
        
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        benchmark_score = max(0, min(1, (avg_gap + 1) / 2))
        
        # Step 4: Enhanced acquisition score components with dynamic weights
        mna_component = self._calculate_weighted_component(mna_likelihood, 0.35, features)
        synergy_component = 0.25 * overall_synergy_score
        valuation_component = 0.15 * valuation_score
        team_component = 0.15 * team_strength_score
        benchmark_component = 0.10 * benchmark_score
        
        acquisition_score = (
            mna_component +
            synergy_component +
            valuation_component +
            team_component +
            benchmark_component
        )
        
        # Step 5: Incorporate Risk with adjusted penalty
        risk_penalty = min(0.5, combined_risk_score)  # Cap risk penalty
        acquisition_score = acquisition_score * (1.0 - risk_penalty)
        
        # Step 6: Clamp result
        acquisition_score = max(0.0, min(1.0, acquisition_score))
        
        return {
            "acquisition_score": float(acquisition_score),
            "mna_likelihood": float(mna_likelihood),
            "synergy_component": float(synergy_component),
            "valuation_component": float(valuation_component),
            "team_component": float(team_component),
            "benchmark_component": float(benchmark_component),
            "risk_penalty": float(risk_penalty)
        }
    
    def _calculate_balanced_mna_likelihood(self, features: Dict[str, Any]) -> float:
        """
        Calculate a balanced M&A likelihood that considers multiple factors instead of relying solely on the model.
        """
        # Get the model prediction if available, but don't rely on it entirely
        model_prediction = features.get("mna_likelihood", 0.0)
        
        # Factors that influence acquisition likelihood
        funding_efficiency = features.get("funding_efficiency", 0.5)
        team_strength = features.get("team_strength_score", 0.5) / 10.0  # Normalize to 0-1
        synergy_score = features.get("overall_synergy_score", 0.5)
        revenue_growth = features.get("revenue_growth_mom", 0.1)
        gross_margin = features.get("gross_margin", 0.5)
        exits_count = features.get("exits_count", 0)
        founder_count = features.get("founder_count", 1)
        
        # Normalize revenue growth (assuming 0.05-0.5 is a reasonable range)
        normalized_growth = min(1.0, max(0.0, revenue_growth / 0.5))
        
        # Weighted combination of factors with balanced weights
        balanced_likelihood = (
            0.2 * model_prediction +  # Model prediction (reduced weight due to class imbalance)
            0.2 * funding_efficiency +
            0.2 * team_strength +
            0.15 * synergy_score +
            0.1 * normalized_growth +
            0.1 * gross_margin +
            0.03 * min(1.0, exits_count / 3.0) +  # Cap at 3 exits
            0.02 * min(1.0, founder_count / 5.0)   # Cap at 5 founders
        )
        
        # Ensure the result is between 0 and 1
        return max(0.0, min(1.0, balanced_likelihood))
    
    def _calculate_weighted_component(self, base_value: float, base_weight: float, features: Dict[str, Any]) -> float:
        """
        Calculate weighted component with dynamic adjustments based on other factors.
        """
        # Adjust weight based on confidence factors
        confidence_factor = 1.0
        
        # Increase weight if there's strong supporting evidence
        if features.get("overall_synergy_score", 0.5) > 0.7:
            confidence_factor += 0.1
        if features.get("team_strength_score", 0.5) > 7.0:  # Higher threshold
            confidence_factor += 0.1
            
        # Decrease weight if there are risk factors
        if features.get("combined_risk_score", 0.3) > 0.5:
            confidence_factor -= 0.1
            
        # Ensure confidence factor stays within reasonable bounds
        confidence_factor = max(0.8, min(1.2, confidence_factor))
        
        return base_weight * base_value * confidence_factor
    
    @staticmethod
    def load() -> 'DecisionScoreAgent':
        """
        Static method to create and return a DecisionScoreAgent instance.
        
        Returns:
            DecisionScoreAgent: A new DecisionScoreAgent instance
        """
        return DecisionScoreAgent()