import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import sys
import os
import logging
import math

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the path to import from src.models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.funding_agent import FundingAgent
from models.team_agent import TeamAgent
from models.synergy_agent import SynergyAgent
from models.valuation_agent import ValuationAgent
from models.reasoning_agent import ReasoningAgent
from models.decision_score_agent import DecisionScoreAgent
from models.risk_agent import RiskAgent
from models.benchmark_agent import BenchmarkAgent
from models.business_model_agent import BusinessModelAgent


class StartupInput(BaseModel):
    funding_json: dict
    team_json: dict
    acquirer_json: dict
    target_json: dict
    financials_json: dict


# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load the trained models when the app starts
model = None
valuation_model = None
# Try to load Crunchbase-trained models first, fallback to original models
if os.path.exists("models/meta_model_crunchbase.joblib"):
    model = joblib.load("models/meta_model_crunchbase.joblib")
    print("Loaded Crunchbase-trained meta model")
elif os.path.exists("models/meta_model.joblib"):
    model = joblib.load("models/meta_model.joblib")
    print("Loaded original meta model")
    
if os.path.exists("models/valuation_model_crunchbase.joblib"):
    valuation_model = joblib.load("models/valuation_model_crunchbase.joblib")
    print("Loaded Crunchbase-trained valuation model")
elif os.path.exists("models/valuation_model.joblib"):
    valuation_model = joblib.load("models/valuation_model.joblib")
    print("Loaded original valuation model")

# Load reasoning agent
reasoning_agent = ReasoningAgent()

# Load decision agent
decision_agent = DecisionScoreAgent()

# Load business model agent
business_model_agent = BusinessModelAgent()

# Load team agent with enhanced features
team_agent = TeamAgent()


@app.post("/predict")
def predict(startup: StartupInput):
    # Check if models are loaded
    if model is None or valuation_model is None or reasoning_agent is None or decision_agent is None:
        return {"error": "Models not loaded"}
    
    # Transform input data using agents
    funding_features = FundingAgent().transform(startup.funding_json)
    team_features = team_agent.transform(startup.team_json)
    synergy_features = SynergyAgent().transform(startup.acquirer_json, startup.target_json)
    valuation_features = ValuationAgent().transform(startup.financials_json)
    business_model_features = business_model_agent.transform(startup.funding_json, startup.team_json, startup.financials_json)
    
    # Combine features for M&A prediction
    mna_features = {**funding_features, **team_features, **synergy_features, **valuation_features}
    
    # Define the feature columns for M&A prediction (same as training)
    meta_feature_columns = [
        'num_rounds', 'total_raised_usd', 'avg_round_size',
        'team_strength_score', 'founder_count', 'avg_experience', 'exits_count',
        'market_similarity', 'tech_similarity', 'revenue_synergy_score',
        'cost_synergy_score', 'overall_synergy_score'
    ]
    
    # Create DataFrame with the features for M&A prediction
    feature_values = [mna_features.get(col, 0) for col in meta_feature_columns]
    df_mna = pd.DataFrame([feature_values], columns=meta_feature_columns)
    
    # Debug: Log the features being sent to the model
    logger.info("M&A Features being sent to model:")
    for i, col in enumerate(meta_feature_columns):
        logger.info(f"  {col}: {feature_values[i]}")
    
    # Make M&A prediction
    try:
        mna_likelihood = model.predict_proba(df_mna)[0][1]  # Probability of positive class
        logger.info(f"M&A likelihood from model: {mna_likelihood}")
    except Exception as e:
        logger.error(f"Error in M&A prediction: {e}")
        mna_likelihood = 0.5  # Default value if model fails
    
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
    
    # Debug: Log some key valuation features
    logger.info("Key Valuation Features:")
    key_val_features = ['revenue_ttm', 'revenue_growth_mom', 'gross_margin']
    for col in key_val_features:
        idx = valuation_feature_columns.index(col)
        logger.info(f"  {col}: {valuation_feature_values[idx]}")
    
    # Make valuation prediction
    try:
        valuation_forecast = valuation_model.predict(df_valuation)[0]
        logger.info(f"Valuation forecast from model: ${valuation_forecast:,.2f}")
    except Exception as e:
        logger.error(f"Error in valuation prediction: {e}")
        valuation_forecast = 1000000  # Default value if model fails
    
    # Combine all features for decision scoring and reasoning
    combined_features = {
        **funding_features,
        **team_features,
        **synergy_features,
        **valuation_features,
        **business_model_features
    }
    
    # Run BenchmarkAgent and RiskAgent
    benchmark_features = BenchmarkAgent().transform(combined_features)
    risk_features = RiskAgent().transform(combined_features)
    
    # Merge everything into full feature dict
    full_feature_dict = {
        **funding_features,
        **team_features,
        **synergy_features,
        **valuation_features,
        **business_model_features,
        **benchmark_features,
        **risk_features,
        "mna_likelihood": float(mna_likelihood),
        "valuation_forecast_usd": float(valuation_forecast)
    }
    
    # Compute decision score
    decision_output = decision_agent.compute(full_feature_dict)
    
    # Get explanation from reasoning agent
    explanation = reasoning_agent.explain(full_feature_dict)
    
    # Get business model insights
    business_model_insights = business_model_agent.get_insights()
    
    # Return response with all components
    return {
        "mna_likelihood": float(mna_likelihood),
        "valuation_forecast_usd": float(valuation_forecast),
        "valuation_forecast_inr": team_agent.convert_to_rupees(float(valuation_forecast)),
        "funding_json": funding_features,  # Include funding features
        "financials_json": valuation_features,  # Include financials features
        "synergy_details": {
            "market_similarity": float(synergy_features.get('market_similarity', 0)),
            "tech_similarity": float(synergy_features.get('tech_similarity', 0)),
            "revenue_synergy_score": float(synergy_features.get('revenue_synergy_score', 0)),
            "cost_synergy_score": float(synergy_features.get('cost_synergy_score', 0)),
            "overall_synergy_score": float(synergy_features.get('overall_synergy_score', 0))
        },
        "business_model_evaluation": business_model_features,
        "business_model_insights": business_model_insights,
        "risk": risk_features,
        "benchmarks": benchmark_features,
        "decision_score": decision_output,
        "explanation": explanation,
        "team_details": {
            "founder_count": team_features.get('founder_count', 0),
            "avg_experience": team_features.get('avg_experience', 0),
            "exits_count": team_features.get('exits_count', 0),
            "estimated_team_size": team_features.get('estimated_team_size', 0),
            "team_strength_score": team_features.get('team_strength_score', 0),
            "founder_details": team_features.get('founder_details', [])
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    models_loaded = {
        "meta_model": model is not None,
        "valuation_model": valuation_model is not None,
        "reasoning_agent": reasoning_agent is not None,
        "decision_agent": decision_agent is not None,
        "business_model_agent": business_model_agent is not None,
        "team_agent": team_agent is not None
    }
    
    return {
        "status": "healthy",
        "models_loaded": models_loaded
    }


@app.get("/competitors/{company_name}")
def get_competitors(company_name: str, industry: str = None):
    """Get competitors for a company"""
    logger.info(f"Getting competitors for: {company_name}, industry: {industry}")
    if team_agent is None:
        logger.error("Team agent not loaded")
        return {"error": "Team agent not loaded"}
    
    try:
        competitors = team_agent.find_competitors(company_name, industry)
        logger.info(f"Found {len(competitors)} competitors")
        
        # Handle NaN values in competitors data
        for competitor in competitors:
            for key, value in competitor.items():
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        logger.info(f"Found invalid float at competitor['{key}']: {value}")
                        competitor[key] = 0.0  # Replace with valid value
        
        return {"competitors": competitors}
    except Exception as e:
        logger.error(f"Error finding competitors: {e}")
        return {"error": f"Error finding competitors: {e}"}


@app.get("/acquisition-targets/{acquirer_name}")
def get_acquisition_targets(acquirer_name: str):
    """Get acquisition targets for an acquirer"""
    logger.info(f"Getting acquisition targets for: {acquirer_name}")
    if team_agent is None:
        logger.error("Team agent not loaded")
        return {"error": "Team agent not loaded"}
    
    try:
        targets = team_agent.find_acquisition_targets(acquirer_name)
        logger.info(f"Found {len(targets)} acquisition targets")
        
        # Handle NaN values in targets data
        for target in targets:
            for key, value in target.items():
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        logger.info(f"Found invalid float at target['{key}']: {value}")
                        target[key] = 0.0  # Replace with valid value
            # Convert USD amounts to INR
            if target.get('price_amount') and target.get('price_currency_code') == 'USD':
                target['price_amount_inr'] = team_agent.convert_to_rupees(target['price_amount'])
        
        return {"targets": targets}
    except Exception as e:
        logger.error(f"Error finding acquisition targets: {e}")
        return {"error": f"Error finding acquisition targets: {e}"}