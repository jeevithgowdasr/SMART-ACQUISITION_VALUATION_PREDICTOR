#!/usr/bin/env python3
"""
Main training script for Smart Acquirer AI models
This script processes the Crunchbase datasets and trains new models
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {description}:")
        print(f"Command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("Smart Acquirer - Model Training Pipeline")
    print("========================================")
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"Working directory: {project_dir}")
    
    # Step 1: Process the datasets
    print("\nStep 1: Processing Crunchbase datasets...")
    success = run_command(
        "python src/pipeline/process_datasets.py",
        "Dataset Processing"
    )
    
    if not success:
        print("Dataset processing failed. Exiting.")
        return 1
    
    # Step 2: Train models with Crunchbase data
    print("\nStep 2: Training models with Crunchbase data...")
    success = run_command(
        "python src/models/train_with_crunchbase.py",
        "Model Training"
    )
    
    if not success:
        print("Model training failed. Exiting.")
        return 1
    
    # Step 3: Test the API
    print("\nStep 3: Testing API health...")
    success = run_command(
        "curl -X GET http://localhost:8000/health",
        "API Health Check"
    )
    
    if not success:
        print("API health check failed.")
        return 1
    
    print("\n" + "="*50)
    print("TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("\nNext steps:")
    print("1. Start the API server: uvicorn src.api.app:app --reload")
    print("2. The API will automatically use the new Crunchbase-trained models")
    print("3. Test the API endpoints with your data")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())