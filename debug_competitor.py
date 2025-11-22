import pandas as pd
import os

# Load the datasets like the TeamAgent does
print("Loading datasets...")
companies_df = pd.read_csv("datasets/objects.csv", nrows=5000)
print(f"Loaded {len(companies_df)} companies")

# Test the competitor lookup logic directly
company_name = "Facebook"
print(f"Searching for competitors of: {company_name}")

try:
    # This is the exact logic from the TeamAgent
    competitors = companies_df[
        companies_df['name'].str.contains(company_name, case=False, na=False) == False
    ].head(10)
    
    print(f"Found {len(competitors)} competitors")
    if len(competitors) > 0:
        print("First competitor:")
        print(competitors.iloc[0][['name', 'permalink', 'domain', 'funding_total_usd']])
        
        # Try to convert to the return format
        result = {
            'name': competitors.iloc[0]['name'],
            'permalink': competitors.iloc[0]['permalink'],
            'domain': competitors.iloc[0].get('domain', ''),
            'funding_total_usd': competitors.iloc[0].get('funding_total_usd', 0),
            'category_code': competitors.iloc[0].get('category_code', '')
        }
        print("Result format:", result)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()