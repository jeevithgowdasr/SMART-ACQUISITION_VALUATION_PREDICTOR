import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.models.team_agent import TeamAgent

def test_team_agent():
    print("Initializing TeamAgent...")
    agent = TeamAgent()
    print(f"Companies loaded: {len(agent.companies_df) if agent.companies_df is not None else 0}")
    print(f"Acquisitions loaded: {len(agent.acquisitions_df) if agent.acquisitions_df is not None else 0}")
    
    print("\nTesting competitor lookup...")
    competitors = agent.find_competitors("Facebook")
    print(f"Found {len(competitors)} competitors")
    if competitors:
        print(f"First competitor: {competitors[0]}")
    
    print("\nTesting acquisition lookup...")
    targets = agent.find_acquisition_targets("Facebook")
    print(f"Found {len(targets)} acquisition targets")
    if targets:
        print(f"First target: {targets[0]}")

if __name__ == "__main__":
    test_team_agent()