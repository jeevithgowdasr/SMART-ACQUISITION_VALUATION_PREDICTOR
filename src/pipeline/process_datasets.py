import pandas as pd
import numpy as np
import json
import os
from tqdm import tqdm
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.funding_agent import FundingAgent
from models.team_agent import TeamAgent
from models.synergy_agent import SynergyAgent
from models.valuation_agent import ValuationAgent

def process_crunchbase_data():
    """
    Process Crunchbase datasets to create training data for our models
    """
    print("Processing Crunchbase datasets...")
    
    # Load the datasets
    try:
        objects_df = pd.read_csv('datasets/objects.csv', low_memory=False)
        funding_rounds_df = pd.read_csv('datasets/funding_rounds.csv', low_memory=False)
        investments_df = pd.read_csv('datasets/investments.csv', low_memory=False)
        print("Datasets loaded successfully")
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return
    
    # Filter for companies only
    companies_df = objects_df[objects_df['entity_type'] == 'Company'].copy()
    print(f"Found {len(companies_df)} companies")
    
    # Process a sample of companies for demonstration (to avoid memory issues)
    sample_companies = companies_df.head(1000)
    
    # Create funding data for each company
    funding_data = {}
    for _, round_row in funding_rounds_df.iterrows():
        object_id = round_row['object_id']
        if object_id in sample_companies['id'].values:
            if object_id not in funding_data:
                funding_data[object_id] = []
            
            funding_data[object_id].append({
                'type': round_row['funding_round_type'],
                'amount': round_row['raised_amount_usd'],
                'date': round_row['funded_at']
            })
    
    # Create synthetic team data based on company information
    team_data = {}
    for _, company_row in sample_companies.iterrows():
        company_id = company_row['id']
        # Create synthetic team data based on company age and funding
        founded_year = None
        if pd.notna(company_row['founded_at']):
            try:
                founded_year = pd.to_datetime(company_row['founded_at']).year
            except:
                pass
        
        # Estimate team size based on funding and age
        total_funding = 0
        if company_id in funding_data:
            total_funding = sum([f.get('amount', 0) or 0 for f in funding_data[company_id]])
        
        # Estimate team size (very rough approximation)
        estimated_team_size = max(1, int(total_funding / 1000000))  # 1 employee per $1M funding
        
        # Create synthetic founders (1-3 founders)
        import random
        num_founders = random.randint(1, 3)
        founders = []
        for i in range(num_founders):
            # Founder experience based on company age
            experience_years = 0
            if founded_year:
                experience_years = max(1, 2023 - founded_year - i*2)
            
            founders.append({
                'experience_years': experience_years,
                'has_exit': random.random() > 0.8  # 20% chance of having an exit
            })
        
        team_data[company_id] = {
            'founders': founders,
            'estimated_team_size': estimated_team_size
        }
    
    # Create synthetic financial data
    financial_data = {}
    for company_id in sample_companies['id'].values:
        # Create synthetic financials based on funding
        total_funding = 0
        if company_id in funding_data:
            total_funding = sum([f.get('amount', 0) or 0 for f in funding_data[company_id]])
        
        # Estimate revenue (very rough - 10% of total funding as annual revenue)
        annual_revenue = total_funding * 0.1
        
        # Estimate growth rate (higher for younger companies)
        growth_rate = np.random.uniform(5.0, 25.0)  # 5-25% monthly growth
        
        # Estimate margins
        gross_margin = np.random.uniform(0.6, 0.9)
        ebitda_margin = np.random.uniform(0.1, 0.3)
        
        financial_data[company_id] = {
            'annual_revenue_usd': annual_revenue,
            'revenue_growth_mom': growth_rate,
            'gross_margin': gross_margin,
            'ebitda_margin': ebitda_margin
        }
    
    # Create synthetic acquirer-target pairs
    # For demonstration, we'll create pairs from the same dataset
    processed_data = []
    company_ids = list(sample_companies['id'].values)
    
    # Create 2000 synthetic acquisition scenarios
    for i in range(min(2000, len(company_ids))):
        acquirer_id = company_ids[i % len(company_ids)]
        target_id = company_ids[(i + 1) % len(company_ids)]
        
        # Skip if we don't have data for either company
        if acquirer_id not in funding_data or target_id not in funding_data:
            continue
            
        # Create startup data
        startup_data = {
            'startup_id': i,
            'funding_json': json.dumps({
                'rounds': funding_data.get(target_id, [])
            }),
            'team_json': json.dumps(team_data.get(target_id, {'founders': []})),
            'acquirer_json': json.dumps({
                'industry': sample_companies[sample_companies['id'] == acquirer_id]['category_code'].iloc[0] if not sample_companies[sample_companies['id'] == acquirer_id]['category_code'].empty else 'unknown',
                'market': sample_companies[sample_companies['id'] == acquirer_id]['category_code'].iloc[0] if not sample_companies[sample_companies['id'] == acquirer_id]['category_code'].empty else 'unknown',
                'tech_stack': [],  # We don't have tech stack data
                'team_size': team_data.get(acquirer_id, {}).get('estimated_team_size', 10)
            }),
            'target_json': json.dumps({
                'industry': sample_companies[sample_companies['id'] == target_id]['category_code'].iloc[0] if not sample_companies[sample_companies['id'] == target_id]['category_code'].empty else 'unknown',
                'market': sample_companies[sample_companies['id'] == target_id]['category_code'].iloc[0] if not sample_companies[sample_companies['id'] == target_id]['category_code'].empty else 'unknown',
                'tech_stack': [],  # We don't have tech stack data
                'team_size': team_data.get(target_id, {}).get('estimated_team_size', 10)
            }),
            'financials_json': json.dumps(financial_data.get(target_id, {}))
        }
        
        processed_data.append(startup_data)
    
    # Save processed data
    if processed_data:
        df = pd.DataFrame(processed_data)
        df.to_csv('data/raw/crunchbase_startups.csv', index=False)
        print(f"Processed {len(processed_data)} startup scenarios and saved to data/raw/crunchbase_startups.csv")
    else:
        print("No data processed")

def build_enhanced_features():
    """
    Build enhanced features using the Crunchbase data
    """
    print("Building enhanced features from Crunchbase data...")
    
    # Load the processed crunchbase data
    try:
        df = pd.read_csv('data/raw/crunchbase_startups.csv')
        print(f"Loaded {len(df)} startup records")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Initialize agents
    funding_agent = FundingAgent()
    team_agent = TeamAgent()
    synergy_agent = SynergyAgent()
    val_agent = ValuationAgent()
    
    # Process each row to generate features
    feature_rows = []
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing startups"):
        try:
            startup_id = row['startup_id']
            
            # Parse JSON data
            funding_json = json.loads(row['funding_json']) if isinstance(row['funding_json'], str) else row['funding_json']
            team_json = json.loads(row['team_json']) if isinstance(row['team_json'], str) else row['team_json']
            acquirer_json = json.loads(row['acquirer_json']) if isinstance(row['acquirer_json'], str) else row['acquirer_json']
            target_json = json.loads(row['target_json']) if isinstance(row['target_json'], str) else row['target_json']
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
        except Exception as e:
            print(f"Error processing startup {row.get('startup_id', 'unknown')}: {e}")
            continue
    
    # Convert to DataFrame and save
    if feature_rows:
        features_df = pd.DataFrame(feature_rows)
        features_df.to_csv('data/processed/crunchbase_features.csv', index=False)
        print(f"Feature file created with {len(feature_rows)} records!")
        return features_df
    else:
        print("No features generated")
        return None

def enhance_training_data_with_targets(features_df):
    """
    Enhance the training data with synthetic target variables for valuation modeling
    """
    if features_df is None or features_df.empty:
        print("No features data to enhance")
        return
    
    print("Enhancing training data with target variables...")
    
    # Create synthetic target variables
    # For demonstration, we'll create realistic targets based on features
    
    # Create a valuation forecast based on current valuation and growth factors
    features_df['valuation_12m_forward'] = features_df['valuation_proxy_current'] * (
        1 + (features_df['revenue_growth_mom'] / 100) * 12 * 0.8  # 80% of growth rate
    )
    
    # Add some noise to make it more realistic
    noise = np.random.normal(1, 0.2, len(features_df))  # 20% standard deviation
    features_df['valuation_12m_forward'] = features_df['valuation_12m_forward'] * noise
    
    # Ensure positive values
    features_df['valuation_12m_forward'] = np.maximum(features_df['valuation_12m_forward'], 0)
    
    # Save enhanced data
    features_df.to_csv('data/processed/crunchbase_features_with_targets.csv', index=False)
    print("Enhanced training data saved!")

if __name__ == "__main__":
    # Process the Crunchbase datasets
    process_crunchbase_data()
    
    # Build features
    features_df = build_enhanced_features()
    
    # Enhance with targets
    enhance_training_data_with_targets(features_df)
    
    print("Dataset processing complete!")