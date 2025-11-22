import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os


def mean_absolute_percentage_error(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def train_valuation_model():
    # Check if features file exists
    if not os.path.exists("data/processed/features_with_targets.csv"):
        print("Features file not found. Please run the feature building pipeline first.")
        return
    
    # Load the features data
    df = pd.read_csv("data/processed/features_with_targets.csv")
    
    # Prepare features and target
    # Drop non-numeric columns and the target column
    columns_to_drop = ["startup_id", "valuation_12m_forward"]
    if "last_round_type" in df.columns:
        columns_to_drop.append("last_round_type")
    
    X = df.drop(columns=columns_to_drop)
    y = df["valuation_12m_forward"]
    
    # Convert all X columns to numeric if needed
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Try to import and use XGBRegressor, fallback to RandomForestRegressor if unavailable
    try:
        from xgboost import XGBRegressor
        model = XGBRegressor(random_state=42)
        print("Using XGBRegressor")
    except ImportError:
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        print("Using RandomForestRegressor (xgboost not available)")
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    preds = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, preds)
    mape = mean_absolute_percentage_error(y_test, preds)
    
    print(f"MAE: {mae:.2f}")
    print(f"MAPE: {mape:.2f}%")
    
    # Save the model
    joblib.dump(model, "models/valuation_model.joblib")
    print("Model saved!")


if __name__ == "__main__":
    train_valuation_model()