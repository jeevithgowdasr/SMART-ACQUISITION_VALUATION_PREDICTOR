import requests
import json
import time

# Test data representing a startup scenario
test_data = {
    "funding_json": {
        "rounds": [
            {"type": "Seed", "amount": "500000"},
            {"type": "Series A", "amount": "2000000"},
            {"type": "Series B", "amount": "10000000"}
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
        "tech_stack": ["python", "react", "aws"],
        "team_size": 500
    },
    "target_json": {
        "industry": "tech",
        "market": "saas",
        "tech_stack": ["python", "angular", "gcp"],
        "team_size": 50
    },
    "financials_json": {
        "monthly_revenue_usd": 100000,
        "revenue_growth_mom": 15.0,
        "gross_margin": 0.8,
        "ebitda_margin": 0.2
    }
}

def test_api_health():
    """Test if the API is healthy and models are loaded"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            print("API Health Check:")
            print(json.dumps(health_data, indent=2))
            return health_data.get("status") == "healthy"
        else:
            print(f"Health check failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return False

def test_prediction():
    """Test sending data to the AI models for prediction"""
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            "http://localhost:8000/predict",
            headers=headers,
            json=test_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\nPrediction Results:")
            print(json.dumps(result, indent=2))
            return result
        else:
            print(f"Prediction failed with status code: {response.status_code}")
            print("Response:", response.text)
            return None
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

def main():
    print("Testing dataset feeding to AI agents and ML models...")
    print("=" * 50)
    
    # Wait a moment for the API to fully start
    time.sleep(2)
    
    # Test health first
    if not test_api_health():
        print("API is not healthy. Please check the server.")
        return
    
    print("\n" + "=" * 50)
    
    # Test prediction
    result = test_prediction()
    
    if result:
        print("\n" + "=" * 50)
        print("SUCCESS: Data has been successfully fed to the AI agents and ML models!")
        print("The models have processed the dataset and returned predictions.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("FAILED: Could not get predictions from the models.")
        print("=" * 50)

if __name__ == "__main__":
    main()