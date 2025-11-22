import pandas as pd
import sys
import os
import json

# Add the parent directory to the path to import from src.models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.funding_agent import FundingAgent
from models.team_agent import TeamAgent
from models.synergy_agent import SynergyAgent
from models.valuation_agent import ValuationAgent


def build_features():
    # Load the raw startup data
    df = pd.read_csv('data/raw/startups.csv')
    
    # Initialize agents
    funding_agent = FundingAgent()
    team_agent = TeamAgent()
    synergy_agent = SynergyAgent()
    val_agent = ValuationAgent()
    
    # Process each row to generate features
    feature_rows = []
    
    for _, row in df.iterrows():
        startup_id = row['startup_id']
        funding_json = row['funding_json']
        team_json = row['team_json']
        
        # Parse the acquirer and target JSON strings
        acquirer_json = json.loads(row['acquirer_json']) if isinstance(row['acquirer_json'], str) else row['acquirer_json']
        target_json = json.loads(row['target_json']) if isinstance(row['target_json'], str) else row['target_json']
        
        # Parse the financials JSON
        financials_json = json.loads(row['financials_json']) if isinstance(row['financials_json'], str) else row['financials_json']
        
        # Generate features using the agents
        funding_features = funding_agent.transform(funding_json)
        team_features = team_agent.transform(team_json)
        synergy_features = synergy_agent.transform(acquirer_json, target_json)
        valuation_features = val_agent.transform(financials_json)
        
        # Combine all features into one dictionary
        combined_features = {
            'startup_id': startup_id,
            **funding_features,
            **team_features,
            **synergy_features,
            **valuation_features
        }
        
        feature_rows.append(combined_features)
    
    # Convert to DataFrame and save
    features_df = pd.DataFrame(feature_rows)
    features_df.to_csv('data/processed/features.csv', index=False)
    
    print("Feature file created successfully!")


if __name__ == "__main__":
    build_features()