import json
from typing import Dict, Any, Union


class FundingAgent:
    def __init__(self):
        pass
    
    def transform(self, funding_json: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(funding_json, str):
            funding_data = json.loads(funding_json)
        else:
            funding_data = funding_json
            
        rounds = funding_data.get('rounds', [])
        num_rounds = len(rounds)
        
        total_raised_usd = 0.0
        for round_info in rounds:
            amount = round_info.get('amount', 0)
            if isinstance(amount, str):
                amount = ''.join(filter(str.isdigit, amount)) or '0'
            total_raised_usd += float(amount)
        
        avg_round_size = 0.0 if num_rounds == 0 else total_raised_usd / num_rounds
        
        last_round_type = "None"
        if rounds:
            last_round = rounds[-1]
            last_round_type = last_round.get('type', 'Unknown')
        
        return {
            'num_rounds': num_rounds,
            'total_raised_usd': total_raised_usd,
            'avg_round_size': avg_round_size,
            'last_round_type': last_round_type
        }
    
    @classmethod
    def load(cls) -> 'FundingAgent':
        return cls()