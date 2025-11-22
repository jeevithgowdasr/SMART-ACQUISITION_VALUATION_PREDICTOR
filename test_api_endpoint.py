import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.api.app import app
from src.models.team_agent import TeamAgent
import uvicorn

def test_endpoint():
    # Test if team_agent is properly initialized
    from src.api.app import team_agent
    print(f"Team agent in API: {team_agent}")
    print(f"Companies loaded: {len(team_agent.companies_df) if team_agent.companies_df is not None else 0}")
    
    # Test the find_competitors method directly
    competitors = team_agent.find_competitors("Facebook")
    print(f"Competitors found: {len(competitors)}")

if __name__ == "__main__":
    test_endpoint()