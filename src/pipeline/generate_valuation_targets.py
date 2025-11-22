import pandas as pd
import numpy as np


def generate_valuation_targets():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Load the processed features
    df = pd.read_csv('data/processed/features.csv')
    
    # Calculate valuation_12m_forward
    # valuation_12m_forward = valuation_proxy_current * (1 + 0.5 * revenue_growth_mom) + noise
    valuation_proxy = df['valuation_proxy_current']
    revenue_growth = df['revenue_growth_mom']
    
    # Calculate the base formula
    base_valuation = valuation_proxy * (1 + 0.5 * revenue_growth / 100)  # Convert percentage to decimal
    
    # Add noise: random normal with mean 0 and std (valuation_proxy_current * 0.1)
    noise = np.random.normal(0, valuation_proxy * 0.1)
    
    # Calculate final valuation_12m_forward
    df['valuation_12m_forward'] = base_valuation + noise
    
    # Save output
    df.to_csv('data/processed/features_with_targets.csv', index=False)
    
    # Print basic statistics
    print(f"Mean valuation_12m_forward: {df['valuation_12m_forward'].mean():.2f}")
    print(f"Std valuation_12m_forward: {df['valuation_12m_forward'].std():.2f}")
    print(f"Min valuation_12m_forward: {df['valuation_12m_forward'].min():.2f}")
    print(f"Max valuation_12m_forward: {df['valuation_12m_forward'].max():.2f}")


if __name__ == "__main__":
    generate_valuation_targets()