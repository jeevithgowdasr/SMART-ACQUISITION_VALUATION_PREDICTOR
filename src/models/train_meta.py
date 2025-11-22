import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os


def train_meta_model():
    # Check if features file exists
    if not os.path.exists("data/processed/features.csv"):
        print("Features file not found. Please run the feature building pipeline first.")
        return
    
    # Load the features data
    df = pd.read_csv("data/processed/features.csv")
    
    # For demonstration purposes, let's create a synthetic target variable
    # In a real scenario, this would be provided in your dataset
    # Let's assume target is 1 if the startup is "successful" (high team strength and funding), 0 otherwise
    df['target'] = ((df['team_strength_score'] > df['team_strength_score'].median()) & 
                    (df['total_raised_usd'] > df['total_raised_usd'].median())).astype(int)
    
    # Prepare features and target
    # Drop only the startup_id column, keep all other numeric columns including synergy features
    X = df.drop(columns=["startup_id", "target"])
    y = df["target"]
    
    # Handle any remaining categorical variables if needed
    # In this case, last_round_type might need to be dropped or encoded
    if 'last_round_type' in X.columns:
        X = X.drop(columns=["last_round_type"])
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    preds = model.predict(X_test)
    
    # Calculate accuracy
    if len(y_test) > 0:
        accuracy = accuracy_score(y_test, preds)
        print(f"Accuracy: {accuracy:.2f}")
    else:
        print("Not enough data for testing.")
    
    # Save the model
    joblib.dump(model, "models/meta_model.joblib")
    print("Model saved!")


if __name__ == "__main__":
    train_meta_model()