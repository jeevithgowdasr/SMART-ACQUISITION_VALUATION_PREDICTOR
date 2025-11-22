import requests
import json

# Test API response
payload = {
    "funding_json": {
        "rounds": [{
            "type": "Series A",
            "amount": 1000000
        }]
    },
    "team_json": {
        "founders": [{
            "experience_years": 5,
            "has_exit": False
        }],
        "estimated_team_size": 50
    },
    "acquirer_json": {
        "industry": "Technology",
        "revenue": 100000000
    },
    "target_json": {
        "industry": "Technology",
        "revenue": 5000000
    },
    "financials_json": {
        "revenue_ttm": 2000000,
        "revenue_growth_mom": 0.15,
        "gross_margin": 0.75,
        "ebitda_margin": 0.20
    }
}

try:
    response = requests.post("http://localhost:8000/predict", json=payload)
    print("Status Code:", response.status_code)
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print("Error:", str(e))