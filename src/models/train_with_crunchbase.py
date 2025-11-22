import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def mean_absolute_percentage_error(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # Avoid division by zero
    mask = y_true != 0
    if not mask.any():
        return np.inf
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def train_meta_model_with_crunchbase():
    """Train the meta model using Crunchbase data"""
    print("Training meta model with Crunchbase data...")
    
    # Check if features file exists
    if not os.path.exists("data/processed/crunchbase_features.csv"):
        print("Crunchbase features file not found. Please run the dataset processing pipeline first.")
        return
    
    # Load the features data
    df = pd.read_csv("data/processed/crunchbase_features.csv")
    
    if df.empty:
        print("No data found in features file.")
        return
    
    print(f"Loaded {len(df)} records for training")
    
    # Create a more realistic target variable
    # Target: 1 if company has strong funding and team, 0 otherwise
    df['target'] = (
        (df['total_raised_usd'] > df['total_raised_usd'].quantile(0.7)) & 
        (df['team_strength_score'] > df['team_strength_score'].quantile(0.7))
    ).astype(int)
    
    print(f"Target distribution: {df['target'].value_counts().to_dict()}")
    
    # Define the feature columns that should be used for the meta model
    meta_feature_columns = [
        'num_rounds', 'total_raised_usd', 'avg_round_size',
        'team_strength_score', 'founder_count', 'avg_experience', 'exits_count',
        'market_similarity', 'tech_similarity', 'revenue_synergy_score',
        'cost_synergy_score', 'overall_synergy_score'
    ]
    
    # Prepare features and target
    X = df[meta_feature_columns]
    y = df["target"]
    
    # Remove any rows with NaN values
    mask = ~(X.isnull().any(axis=1) | y.isnull())
    X = X[mask]
    y = y[mask]
    
    if len(X) == 0:
        print("No valid data after cleaning.")
        return
    
    print(f"Training on {len(X)} samples with {len(X.columns)} features")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    # Make predictions
    preds = model.predict(X_test)
    
    # Calculate accuracy
    if len(y_test) > 0:
        accuracy = accuracy_score(y_test, preds)
        print(f"Accuracy: {accuracy:.4f}")
    else:
        print("Not enough data for testing.")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    # Save the model
    joblib.dump(model, "models/meta_model_crunchbase.joblib")
    print("Meta model saved as models/meta_model_crunchbase.joblib!")

def train_valuation_model_with_crunchbase():
    """Train the valuation model using Crunchbase data"""
    print("\nTraining valuation model with Crunchbase data...")
    
    # Check if features file exists
    if not os.path.exists("data/processed/crunchbase_features_with_targets.csv"):
        print("Crunchbase features with targets file not found. Please run the dataset processing pipeline first.")
        return
    
    # Load the features data
    df = pd.read_csv("data/processed/crunchbase_features_with_targets.csv")
    
    if df.empty:
        print("No data found in features file.")
        return
    
    print(f"Loaded {len(df)} records for training")
    
    # Define the feature columns that should be used for the valuation model
    valuation_feature_columns = [
        'num_rounds', 'total_raised_usd', 'avg_round_size',
        'team_strength_score', 'founder_count', 'avg_experience', 'exits_count',
        'market_similarity', 'tech_similarity', 'revenue_synergy_score',
        'cost_synergy_score', 'overall_synergy_score',
        'revenue_ttm', 'revenue_growth_mom', 'gross_margin', 'ebitda_margin',
        'revenue_multiple_proxy', 'valuation_proxy_current'
    ]
    
    # Prepare features and target
    X = df[valuation_feature_columns]
    y = df["valuation_12m_forward"]
    
    # Remove any rows with NaN values or infinite values
    mask = ~(X.isnull().any(axis=1) | y.isnull() | np.isinf(y) | np.isinf(X).any(axis=1))
    X = X[mask]
    y = y[mask]
    
    if len(X) == 0:
        print("No valid data after cleaning.")
        return
    
    # Also remove extreme outliers (values beyond 99th percentile)
    y_upper_limit = np.percentile(y, 99)
    mask = y <= y_upper_limit
    X = X[mask]
    y = y[mask]
    
    if len(X) == 0:
        print("No valid data after outlier removal.")
        return
    
    print(f"Training on {len(X)} samples with {len(X.columns)} features")
    print(f"Target variable statistics: min={y.min():.2f}, max={y.max():.2f}, median={np.median(y):.2f}")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Try to import and use XGBRegressor, fallback to RandomForestRegressor if unavailable
    try:
        from xgboost import XGBRegressor
        model = XGBRegressor(random_state=42, n_estimators=100)
        print("Using XGBRegressor")
    except ImportError:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        print("Using RandomForestRegressor (xgboost not available)")
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    preds = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, preds)
    mape = mean_absolute_percentage_error(y_test, preds)
    
    print(f"MAE: ${mae:,.2f}")
    print(f"MAPE: {mape:.2f}%")
    
    # Feature importance
    if hasattr(model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features for Valuation:")
        print(feature_importance.head(10))
    
    # Save the model
    joblib.dump(model, "models/valuation_model_crunchbase.joblib")
    print("Valuation model saved as models/valuation_model_crunchbase.joblib!")

def compare_models():
    """Compare the new models with the existing ones"""
    print("\n" + "="*50)
    print("COMPARING MODELS")
    print("="*50)
    
    # Check if both model versions exist
    if os.path.exists("models/meta_model.joblib") and os.path.exists("models/meta_model_crunchbase.joblib"):
        print("Both meta models exist - comparison possible")
    else:
        print("Cannot compare meta models - one or both missing")
        
    if os.path.exists("models/valuation_model.joblib") and os.path.exists("models/valuation_model_crunchbase.joblib"):
        print("Both valuation models exist - comparison possible")
    else:
        print("Cannot compare valuation models - one or both missing")

if __name__ == "__main__":
    # Train models with Crunchbase data
    train_meta_model_with_crunchbase()
    train_valuation_model_with_crunchbase()
    
    # Compare models
    compare_models()
    
    print("\nTraining complete!")