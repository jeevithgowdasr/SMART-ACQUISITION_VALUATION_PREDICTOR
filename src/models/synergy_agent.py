class SynergyAgent:
    def __init__(self):
        pass
    
    def transform(self, acquirer: dict, target: dict) -> dict:
        # Calculate market similarity
        market_similarity = self._calculate_string_similarity(
            acquirer.get('market', ''), 
            target.get('market', '')
        )
        
        # Calculate industry similarity
        industry_similarity = self._calculate_string_similarity(
            acquirer.get('industry', ''), 
            target.get('industry', '')
        )
        
        # Combined market similarity (average of market and industry)
        market_sim = (market_similarity + industry_similarity) / 2
        
        # Calculate tech similarity using Jaccard index
        tech_sim = self._calculate_jaccard_similarity(
            acquirer.get('tech_stack', []), 
            target.get('tech_stack', [])
        )
        
        # Calculate revenue synergy score
        acquirer_team_size = acquirer.get('team_size', 1)
        target_team_size = target.get('team_size', 1)
        revenue_synergy = market_sim + (acquirer_team_size + target_team_size) / 100
        
        # Calculate cost synergy score based on team size ratio
        if target_team_size > 0:
            team_size_ratio = acquirer_team_size / target_team_size
            # Higher ratio means more potential for cost savings
            cost_synergy = min(team_size_ratio / 2, 1.0) if team_size_ratio >= 1 else team_size_ratio / 2
        else:
            cost_synergy = 0.0
        
        # Calculate overall synergy score with weighted sum
        overall_synergy = (
            market_sim * 0.35 + 
            tech_sim * 0.35 + 
            revenue_synergy * 0.15 + 
            cost_synergy * 0.15
        )
        
        return {
            'market_similarity': float(market_sim),
            'tech_similarity': float(tech_sim),
            'revenue_synergy_score': float(revenue_synergy),
            'cost_synergy_score': float(cost_synergy),
            'overall_synergy_score': float(overall_synergy)
        }
    
    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings."""
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0
            
        str1, str2 = str1.lower(), str2.lower()
        if str1 == str2:
            return 1.0
        elif str1 in str2 or str2 in str1:
            return 0.8
        else:
            return 0.0
    
    def _calculate_jaccard_similarity(self, list1: list, list2: list) -> float:
        """Calculate Jaccard similarity between two lists."""
        if not list1 and not list2:
            return 1.0
        if not list1 or not list2:
            return 0.0
            
        set1, set2 = set(list1), set(list2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def load() -> 'SynergyAgent':
        return SynergyAgent()