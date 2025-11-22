import joblib
import pandas as pd
import numpy as np

# Load the model
print("Loading model...")
model = joblib.load("models/meta_model_crunchbase.joblib")
print("Model loaded successfully!")

# Create test data that matches the training data format
test_data = {
    'num_rounds': 2,
    'total_raised_usd': 2000000.0,
    'avg_round_size': 1000000.0,
    'team_strength_score': 7.0,
    'founder_count': 2,
    'avg_experience': 8.0,
    'exits_count': 1,
    'market_similarity': 1.0,
    'tech_similarity': 1.0,
    'revenue_synergy_score': 1.0,
    'cost_synergy_score': 0.8,
    'overall_synergy_score': 0.9
}

# Convert to DataFrame
meta_feature_columns = [
    'num_rounds', 'total_raised_usd', 'avg_round_size',
    'team_strength_score', 'founder_count', 'avg_experience', 'exits_count',
    'market_similarity', 'tech_similarity', 'revenue_synergy_score',
    'cost_synergy_score', 'overall_synergy_score'
]

# Create feature values list
feature_values = [test_data.get(col, 0) for col in meta_feature_columns]
df_mna = pd.DataFrame([feature_values], columns=meta_feature_columns)

print("Test data:")
for i, col in enumerate(meta_feature_columns):
    print(f"  {col}: {feature_values[i]}")

# Make prediction
print("\nMaking prediction...")
try:
    mna_likelihood = model.predict_proba(df_mna)[0][1]  # Probability of positive class
    print(f"M&A likelihood: {mna_likelihood}")
    
    # Also get the prediction class
    prediction = model.predict(df_mna)[0]
    print(f"Prediction class: {prediction}")
    
    # Show feature importance if available
    if hasattr(model, 'feature_importances_'):
        print("\nFeature importances:")
        feature_importance = pd.DataFrame({
            'feature': meta_feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        print(feature_importance.head(10))
        
except Exception as e:
    print(f"Error in prediction: {e}")
    import traceback
    traceback.print_exc()