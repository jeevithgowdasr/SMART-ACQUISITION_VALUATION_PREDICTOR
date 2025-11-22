import requests
import json

# Test data
data = {
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
        "team_size": 500
    },
    "target_json": {
        "industry": "tech",
        "market": "saas",
        "tech_stack": ["python", "angular"],
        "team_size": 50
    },
    "financials_json": {
        "monthly_revenue_usd": 100000,
        "revenue_growth_mom": 15.0,
        "gross_margin": 0.8
    }
}

# Make prediction request
response = requests.post('http://localhost:8000/predict', json=data)
result = response.json()

print("=== FUNDING AGENT RESULTS ===")
funding = result.get('funding_json', {})
print(f"Total Raised: ${funding.get('total_raised_usd', 0):,.2f}")
print(f"Number of Rounds: {funding.get('num_rounds', 0)}")
print(f"Average Round Size: ${funding.get('avg_round_size', 0):,.2f}")
print(f"Last Round Type: {funding.get('last_round_type', 'N/A')}")
print()

print("=== VALUATION AGENT RESULTS ===")
financials = result.get('financials_json', {})
print(f"Revenue TTM: ${financials.get('revenue_ttm', 0):,.2f}")
print(f"Gross Margin: {financials.get('gross_margin', 0):.1%}")
print(f"EBITDA Margin: {financials.get('ebitda_margin', 0):.1%}")
print(f"Revenue Growth: {financials.get('revenue_growth_mom', 0):.1f}%")
print()

print("=== DECISION AGENT RESULTS ===")
decision = result.get('decision_score', {})
print(f"Acquisition Score: {decision.get('acquisition_score', 0):.3f}")
print(f"Valuation Component: {decision.get('valuation_component', 0):.3f}")
print(f"M&A Likelihood: {decision.get('mna_likelihood', 0):.3f}")
print(f"Synergy Component: {decision.get('synergy_component', 0):.3f}")
print(f"Team Component: {decision.get('team_component', 0):.3f}")
print()

print("=== VALUATION FORECAST ===")
print(f"Forecast USD: ${result.get('valuation_forecast_usd', 0):,.2f}")
print(f"Forecast INR: ₹{result.get('valuation_forecast_inr', 0):,.2f}")