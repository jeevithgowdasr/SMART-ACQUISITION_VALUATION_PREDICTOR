class BenchmarkAgent:
    def __init__(self):
        """
        Initialize BenchmarkAgent with no arguments.
        """
        pass
    
    def transform(self, features: dict) -> dict:
        """
        Compare startup metrics against industry benchmarks.
        
        Args:
            features: Dictionary containing features from other agents and models
            
        Returns:
            Dictionary with benchmark gaps
        """
        # Industry benchmarks (hardcoded)
        avg_total_raised_usd = 5_000_000
        avg_team_experience_years = 7.0
        avg_synergy_score = 0.6
        avg_revenue_multiple = 5.0
        avg_revenue_growth_mom = 0.08  # 8%
        avg_ttm_revenue = 1_200_000
        
        # Get feature values with defaults
        total_raised_usd = features.get("total_raised_usd", 0)
        avg_experience = features.get("avg_experience", 0)
        overall_synergy_score = features.get("overall_synergy_score", 0)
        revenue_multiple_proxy = features.get("revenue_multiple_proxy", 0)
        revenue_growth_mom = features.get("revenue_growth_mom", 0)
        revenue_ttm = features.get("revenue_ttm", 0)
        
        # Compute benchmark gaps
        funding_benchmark_gap = self._compute_gap(total_raised_usd, avg_total_raised_usd)
        team_experience_gap = self._compute_gap(avg_experience, avg_team_experience_years)
        synergy_benchmark_gap = self._compute_gap(overall_synergy_score, avg_synergy_score)
        valuation_multiple_gap = self._compute_gap(revenue_multiple_proxy, avg_revenue_multiple)
        growth_benchmark_gap = self._compute_gap(revenue_growth_mom, avg_revenue_growth_mom)
        revenue_ttm_gap = self._compute_gap(revenue_ttm, avg_ttm_revenue)
        
        return {
            "funding_benchmark_gap": funding_benchmark_gap,
            "team_experience_gap": team_experience_gap,
            "synergy_benchmark_gap": synergy_benchmark_gap,
            "valuation_multiple_gap": valuation_multiple_gap,
            "growth_benchmark_gap": growth_benchmark_gap,
            "revenue_ttm_gap": revenue_ttm_gap
        }
    
    def _compute_gap(self, value: float, benchmark: float) -> float:
        """
        Compute normalized gap between value and benchmark.
        
        Args:
            value: Actual value
            benchmark: Benchmark value
            
        Returns:
            Normalized gap clamped between -1.0 and +1.0
        """
        if benchmark == 0:
            return 0.0
        
        gap = (value - benchmark) / benchmark
        
        # Clamp extreme values between -1.0 and +1.0
        return max(-1.0, min(1.0, gap))
    
    @staticmethod
    def load() -> 'BenchmarkAgent':
        """
        Static method to create and return a BenchmarkAgent instance.
        
        Returns:
            BenchmarkAgent: A new BenchmarkAgent instance
        """
        return BenchmarkAgent()