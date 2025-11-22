class RiskAgent:
    def __init__(self):
        """
        Initialize RiskAgent with no arguments.
        """
        pass
    
    def transform(self, features: dict) -> dict:
        """
        Compute risk scores from existing metrics.
        
        Args:
            features: Dictionary containing features from other agents and models
            
        Returns:
            Dictionary with risk scores
        """
        # Compute funding risk
        funding_risk = self._compute_funding_risk(features)
        
        # Compute team risk
        team_risk = self._compute_team_risk(features)
        
        # Compute synergy risk
        synergy_risk = self._compute_synergy_risk(features)
        
        # Compute valuation risk
        valuation_risk = self._compute_valuation_risk(features)
        
        # Compute combined risk score
        combined_risk_score = self._compute_combined_risk_score(
            funding_risk, team_risk, synergy_risk, valuation_risk
        )
        
        return {
            "funding_risk": funding_risk,
            "team_risk": team_risk,
            "synergy_risk": synergy_risk,
            "valuation_risk": valuation_risk,
            "combined_risk_score": combined_risk_score
        }
    
    def _compute_funding_risk(self, features: dict) -> float:
        """
        Compute funding risk based on number of rounds, total raised, and round consistency.
        
        Args:
            features: Dictionary containing features
            
        Returns:
            Funding risk score (0.0-1.0)
        """
        # Get funding metrics with defaults
        num_rounds = features.get("num_rounds", 0)
        total_raised = features.get("total_raised_usd", 0)
        last_round_type = features.get("last_round_type", "")
        
        # High risk if few rounds or low total raised
        rounds_risk = max(0.0, 1.0 - min(num_rounds / 5.0, 1.0))  # Normalize by 5 rounds
        raised_risk = max(0.0, 1.0 - min(total_raised / 10000000.0, 1.0))  # Normalize by $10M
        
        # Round type consistency risk (simplified)
        inconsistent_round_risk = 0.0
        if isinstance(last_round_type, str):
            # High risk if last round is very early stage
            if last_round_type in ["Pre-seed", "Pre-Seed", "PreSeed"]:
                inconsistent_round_risk = 0.8
            elif last_round_type in ["Seed"]:
                inconsistent_round_risk = 0.5
            else:
                inconsistent_round_risk = 0.2
        
        # Combine risks (weighted average)
        funding_risk = (rounds_risk * 0.4 + raised_risk * 0.4 + inconsistent_round_risk * 0.2)
        
        # Ensure bounds
        return max(0.0, min(1.0, funding_risk))
    
    def _compute_team_risk(self, features: dict) -> float:
        """
        Compute team risk based on experience, founder count, and exits.
        
        Args:
            features: Dictionary containing features
            
        Returns:
            Team risk score (0.0-1.0)
        """
        # Get team metrics with defaults
        avg_experience = features.get("avg_experience", 0)
        founder_count = features.get("founder_count", 1)
        exits_count = features.get("exits_count", 0)
        
        # High risk if low experience
        experience_risk = max(0.0, 1.0 - min(avg_experience / 10.0, 1.0))  # Normalize by 10 years
        
        # High risk if few founders
        founder_risk = max(0.0, 1.0 - min(founder_count / 3.0, 1.0))  # Normalize by 3 founders
        
        # High risk if no exits
        exits_risk = 1.0 if exits_count == 0 else max(0.0, 1.0 - min(exits_count / 2.0, 1.0))
        
        # Combine risks (weighted average)
        team_risk = (experience_risk * 0.4 + founder_risk * 0.3 + exits_risk * 0.3)
        
        # Ensure bounds
        return max(0.0, min(1.0, team_risk))
    
    def _compute_synergy_risk(self, features: dict) -> float:
        """
        Compute synergy risk based on overall synergy score.
        
        Args:
            features: Dictionary containing features
            
        Returns:
            Synergy risk score (0.0-1.0)
        """
        # Get synergy metrics with defaults
        overall_synergy_score = features.get("overall_synergy_score", 0.5)
        
        # High risk if overall synergy score is low
        synergy_risk = max(0.0, 1.0 - overall_synergy_score)
        
        # Ensure bounds
        return max(0.0, min(1.0, synergy_risk))
    
    def _compute_valuation_risk(self, features: dict) -> float:
        """
        Compute valuation risk based on revenue multiple and forecast vs TTM.
        
        Args:
            features: Dictionary containing features
            
        Returns:
            Valuation risk score (0.0-1.0)
        """
        # Get valuation metrics with defaults
        revenue_multiple = features.get("revenue_multiple_proxy", 5.0)
        valuation_forecast = features.get("valuation_forecast_usd", 0)
        revenue_ttm = features.get("revenue_ttm", 1)
        
        # High risk if revenue multiple is too high
        multiple_risk = min(revenue_multiple / 15.0, 1.0)  # Normalize by 15x multiple
        
        # High risk if valuation forecast is far above revenue
        forecast_to_revenue_ratio = valuation_forecast / max(revenue_ttm, 1)
        forecast_risk = min(forecast_to_revenue_ratio / 20.0, 1.0)  # Normalize by 20x ratio
        
        # Combine risks (weighted average)
        valuation_risk = (multiple_risk * 0.5 + forecast_risk * 0.5)
        
        # Ensure bounds
        return max(0.0, min(1.0, valuation_risk))
    
    def _compute_combined_risk_score(self, funding_risk: float, team_risk: float, 
                                   synergy_risk: float, valuation_risk: float) -> float:
        """
        Compute combined risk score as weighted average of all risks.
        
        Args:
            funding_risk: Funding risk score
            team_risk: Team risk score
            synergy_risk: Synergy risk score
            valuation_risk: Valuation risk score
            
        Returns:
            Combined risk score (0.0-1.0)
        """
        combined_risk = (
            funding_risk * 0.25 +
            team_risk * 0.25 +
            synergy_risk * 0.25 +
            valuation_risk * 0.25
        )
        
        # Ensure bounds
        return max(0.0, min(1.0, combined_risk))
    
    @staticmethod
    def load() -> 'RiskAgent':
        """
        Static method to create and return a RiskAgent instance.
        
        Returns:
            RiskAgent: A new RiskAgent instance
        """
        return RiskAgent()