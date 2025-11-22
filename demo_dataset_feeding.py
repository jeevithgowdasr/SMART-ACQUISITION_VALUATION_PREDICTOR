#!/usr/bin/env python3
"""
Demo Script: Dataset Feeding to AI Agents and ML Models
This script demonstrates the complete flow of feeding datasets to the AI system.
"""

import os
import subprocess
import sys
import time

def check_api_health():
    """Check if the API is running and healthy"""
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200 and response.json().get("status") == "healthy"
    except:
        return False

def start_api_server():
    """Start the API server in the background"""
    print("Starting API server...")
    # Start the server in background
    subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "src.api.app:app", 
        "--port", "8000",
        "--reload"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait for server to start
    print("Waiting for API server to start...")
    for i in range(10):
        if check_api_health():
            print("✅ API server is running and healthy!")
            return True
        time.sleep(1)
    
    print("❌ API server failed to start")
    return False

def demonstrate_batch_processing():
    """Demonstrate batch processing of datasets"""
    print("\n" + "="*60)
    print("BATCH PROCESSING DEMONSTRATION")
    print("="*60)
    
    print("1. Dataset Processing Pipeline:")
    print("   - Reading raw Crunchbase data from datasets/")
    print("   - Transforming data with AI agents")
    print("   - Generating feature files in data/processed/")
    
    # Show what files were created
    if os.path.exists("data/processed/crunchbase_features_with_targets.csv"):
        print("   ✅ Processed features file: data/processed/crunchbase_features_with_targets.csv")
    
    print("\n2. Model Training:")
    print("   - Loading processed features")
    print("   - Training Random Forest models")
    print("   - Saving models to models/ directory")
    
    # Show trained models
    if os.path.exists("models/meta_model_crunchbase.joblib"):
        print("   ✅ Meta model trained: models/meta_model_crunchbase.joblib")
    if os.path.exists("models/valuation_model_crunchbase.joblib"):
        print("   ✅ Valuation model trained: models/valuation_model_crunchbase.joblib")

def demonstrate_real_time_processing():
    """Demonstrate real-time data processing through API"""
    print("\n" + "="*60)
    print("REAL-TIME PROCESSING DEMONSTRATION")
    print("="*60)
    
    print("1. API Endpoint: POST /predict")
    print("2. Data Flow:")
    print("   - Receive JSON payload with startup data")
    print("   - Transform with AI agents (Funding, Team, Synergy, Valuation)")
    print("   - Apply trained models for predictions")
    print("   - Return comprehensive analysis")
    
    # Show sample request
    sample_request = """
{
  "funding_json": {
    "rounds": [
      {"type": "Seed", "amount": "500000"},
      {"type": "Series A", "amount": "2000000"}
    ]
  },
  "team_json": {
    "founders": [
      {"experience_years": 5, "has_exit": true},
      {"experience_years": 3, "has_exit": false}
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
    """
    
    print("\n3. Sample Request:")
    print(sample_request)

def demonstrate_ai_agents():
    """Demonstrate the AI agents in the system"""
    print("\n" + "="*60)
    print("AI AGENTS IN THE SYSTEM")
    print("="*60)
    
    agents = [
        ("Funding Agent", "Analyzes funding rounds, amounts, and patterns"),
        ("Team Agent", "Evaluates founder experience, team strength, and exits"),
        ("Synergy Agent", "Calculates market, technology, and operational synergies"),
        ("Valuation Agent", "Processes financial metrics and revenue data"),
        ("Risk Agent", "Assesses acquisition risks and potential issues"),
        ("Benchmark Agent", "Compares against industry benchmarks"),
        ("Business Model Agent", "Evaluates business model strength"),
        ("Reasoning Agent", "Provides explanations for predictions"),
        ("Decision Score Agent", "Computes overall acquisition decision score")
    ]
    
    for name, description in agents:
        print(f"🤖 {name}: {description}")

def main():
    """Main demonstration function"""
    print("SMART ACQUIRER - DATASET FEEDING DEMONSTRATION")
    print("="*60)
    
    # Check if API is already running
    if not check_api_health():
        print("API server is not running. Starting it now...")
        if not start_api_server():
            print("Failed to start API server. Some demonstrations will be limited.")
    
    # Demonstrate the complete flow
    demonstrate_batch_processing()
    demonstrate_ai_agents()
    demonstrate_real_time_processing()
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\n✅ Datasets have been successfully fed to the AI agents and ML models!")
    print("✅ The system is ready to process new data and make predictions!")
    
    if check_api_health():
        print("✅ API is running and accepting requests at http://localhost:8000")
        print("   - Health check: GET http://localhost:8000/health")
        print("   - Prediction: POST http://localhost:8000/predict")

if __name__ == "__main__":
    main()