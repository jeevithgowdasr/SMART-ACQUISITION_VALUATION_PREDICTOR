import requests
import json

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

# Test the API
try:
    response = requests.post(
        "http://localhost:8000/predict",
        json=test_data
    )
    
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")