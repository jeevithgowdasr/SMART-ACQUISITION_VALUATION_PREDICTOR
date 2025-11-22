"""
Script to integrate the VC startup evaluation dataset with the Smart Acquirer project.

This script demonstrates how to:
1. Use the dataset to fine-tune the ReasoningAgent's LLM
2. Create training data for additional ML models
3. Enhance the existing agents with more sophisticated evaluation criteria
"""

from datasets import load_dataset
import json
import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_explore_dataset():
    """Load and explore the VC startup evaluation dataset"""
    print("Loading VC startup evaluation dataset...")
    ds = load_dataset("gauravshrm211/VC-startup-evaluation-for-investment")
    print(f"Dataset loaded with {len(ds['train'])} examples")
    return ds

def prepare_fine_tuning_data(ds):
    """Prepare data for fine-tuning the ReasoningAgent's LLM"""
    print("\nPreparing data for LLM fine-tuning...")
    
    # Format data for instruction fine-tuning
    fine_tuning_data = []
    for example in ds['train']:
        fine_tuning_data.append({
            "instruction": example['prompt'],
            "input": "",  # In this dataset, the prompt is the instruction itself
            "output": example['completion']
        })
    
    # Save to JSONL format (common for LLM fine-tuning)
    with open("llm_fine_tuning_data.jsonl", "w", encoding="utf-8") as f:
        for item in fine_tuning_data:
            f.write(json.dumps(item) + "\n")
    
    print(f"Saved {len(fine_tuning_data)} examples for LLM fine-tuning to llm_fine_tuning_data.jsonl")
    return fine_tuning_data

def create_enhanced_training_data(ds):
    """Create enhanced training data for ML models"""
    print("\nCreating enhanced training data...")
    
    # Convert to DataFrame for easier manipulation
    data_list = []
    for example in ds['train']:
        data_list.append({
            'prompt': example['prompt'],
            'completion': example['completion'],
            'evaluation_aspect': extract_aspect_from_prompt(example['prompt'])
        })
    
    df = pd.DataFrame(data_list)
    
    # Save as CSV for model training
    df.to_csv("enhanced_training_data.csv", index=False)
    print(f"Saved enhanced training data to enhanced_training_data.csv")
    print("Data includes:")
    print(df['evaluation_aspect'].value_counts())
    
    return df

def extract_aspect_from_prompt(prompt):
    """Extract evaluation aspect from prompt"""
    prompt = prompt.lower()
    if 'business model' in prompt:
        return 'business_model'
    elif 'market opportunity' in prompt or 'market potential' in prompt:
        return 'market_opportunity'
    elif 'founding team' in prompt or 'team' in prompt:
        return 'team'
    elif 'competitive advantage' in prompt:
        return 'competition'
    elif 'financial' in prompt:
        return 'financials'
    elif 'risk' in prompt:
        return 'risk'
    elif 'traction' in prompt or 'customer' in prompt:
        return 'traction'
    elif 'technology' in prompt:
        return 'technology'
    elif 'funds' in prompt or 'investment' in prompt:
        return 'funding'
    else:
        return 'general'

def enhance_reasoning_agent():
    """Show how to enhance the ReasoningAgent with dataset insights"""
    print("\n=== ENHANCEMENT OPPORTUNITIES FOR REASONING AGENT ===")
    print("1. Fine-tune the LLM on this domain-specific data for better investment recommendations")
    print("2. Add aspect-based evaluation scores to the reasoning output")
    print("3. Improve the decision rules based on patterns in the dataset")
    print("4. Add confidence calibration based on the dataset's completion quality")

def generate_new_features(ds):
    """Generate new features for the Smart Acquirer system"""
    print("\n=== NEW FEATURES THAT CAN BE ADDED ===")
    aspects = set()
    for example in ds['train']:
        aspects.add(extract_aspect_from_prompt(example['prompt']))
    
    print("Evaluation aspects that can be added to Smart Acquirer:")
    for aspect in aspects:
        print(f"- {aspect.replace('_', ' ').title()} evaluation agent")
    
    print("\nExample new agents that could be created:")
    print("- BusinessModelAgent")
    print("- MarketOpportunityAgent")
    print("- CompetitiveAdvantageAgent")
    print("- FinancialHealthAgent")
    print("- RiskAssessmentAgent")

def main():
    """Main function to run the integration"""
    print("=== SMART ACQUIRER DATASET INTEGRATION ===")
    
    # Load dataset
    ds = load_and_explore_dataset()
    
    # Prepare data for different uses
    fine_tuning_data = prepare_fine_tuning_data(ds)
    training_data = create_enhanced_training_data(ds)
    
    # Show enhancement opportunities
    enhance_reasoning_agent()
    generate_new_features(ds)
    
    print("\n=== NEXT STEPS ===")
    print("1. Use llm_fine_tuning_data.jsonl to fine-tune your LLM")
    print("2. Use enhanced_training_data.csv to train specialized models")
    print("3. Consider creating new agents based on the evaluation aspects")
    print("4. Integrate aspect-based scoring into the decision framework")

if __name__ == "__main__":
    main()