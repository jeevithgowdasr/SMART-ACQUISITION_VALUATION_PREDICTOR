import joblib
import pandas as pd
import sys
import os

# Add the parent directory to the path to import from src.models
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from models.funding_agent import FundingAgent
from models.team_agent import TeamAgent
from models.synergy_agent import SynergyAgent
from models.valuation_agent import ValuationAgent

# Load models
print("Loading models...")
try:
    model = joblib.load("models/meta_model_crunchbase.joblib")
    valuation_model = joblib.load("models/valuation_model_crunchbase.joblib")
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    sys.exit(1)

# Test data
test_data = {
    "funding_json": {
        "rounds": [
            {"type": "Seed", "amount": "500000"},
            {"type": "Series A", "amount": "2000000"}
        ]
    },
    "team_json": {
        "founders": [
            {"experience_years": 5, "has_exit": True},
            {"experience_years": 3, "has_exit": False}
        ]
    },
    "acquirer_json": {
        "industry": "tech",
        "market": "saas",
        "tech_stack": ["python", "react"],
        "team_size": 50
    },
    "target_json": {
        "industry": "tech",
        "market": "saas",
        "tech_stack": ["python", "angular"],
        "team_size": 30
    },
    "financials_json": {
        "monthly_revenue_usd": 10000,
        "revenue_growth_mom": 5.0,
        "gross_margin": 0.7
    }
}

# Transform input data using agents
print("Transforming data...")
try:
    funding_features = FundingAgent().transform(test_data["funding_json"])
    team_features = TeamAgent().transform(test_data["team_json"])
    synergy_features = SynergyAgent().transform(test_data["acquirer_json"], test_data["target_json"])
    valuation_features = ValuationAgent().transform(test_data["financials_json"])
    
    print("Funding features:", funding_features)
    print("Team features:", team_features)
    print("Synergy features:", synergy_features)
    print("Valuation features:", valuation_features)
    
    # Combine features for M&A prediction
    mna_features = {**funding_features, **team_features, **synergy_features, **valuation_features}
    print("Combined features:", mna_features)
    
    # Define the feature columns for M&A prediction (same as training)
    meta_feature_columns = [
        'num_rounds', 'total_raised_usd', 'avg_round_size',
        'team_strength_score', 'founder_count', 'avg_experience', 'exits_count',
        'market_similarity', 'tech_similarity', 'revenue_synergy_score',
        'cost_synergy_score', 'overall_synergy_score'
    ]
    
    # Create a DataFrame with the correct column order for M&A prediction
    feature_values = [mna_features.get(col, 0) for col in meta_feature_columns]
    df_mna = pd.DataFrame([feature_values], columns=meta_feature_columns)
    print("M&A DataFrame:")
    print(df_mna)
    
    # Make M&A prediction
    mna_likelihood = model.predict_proba(df_mna)[0][1]  # Probability of positive class
    print(f"M&A likelihood: {mna_likelihood}")
    
    # Define the feature columns for valuation prediction (same as training)
    valuation_feature_columns = [
        'num_rounds', 'total_raised_usd', 'avg_round_size',
        'team_strength_score', 'founder_count', 'avg_experience', 'exits_count',
        'market_similarity', 'tech_similarity', 'revenue_synergy_score',
        'cost_synergy_score', 'overall_synergy_score',
        'revenue_ttm', 'revenue_growth_mom', 'gross_margin', 'ebitda_margin',
        'revenue_multiple_proxy', 'valuation_proxy_current'
    ]
    
    # Create DataFrame with valuation features
    valuation_feature_values = [mna_features.get(col, 0) for col in valuation_feature_columns]
    df_valuation = pd.DataFrame([valuation_feature_values], columns=valuation_feature_columns)
    print("Valuation DataFrame:")
    print(df_valuation)
    
    # Make valuation prediction
    valuation_forecast = valuation_model.predict(df_valuation)[0]
    print(f"Valuation forecast: ${valuation_forecast:,.2f}")
    
except Exception as e:
    print(f"Error during prediction: {e}")
    import traceback
    traceback.print_exc()