import json
from typing import List, Dict, Any, Union


class FeatureImportanceAgent:
    def __init__(self):
        """
        Initialize FeatureImportanceAgent with no arguments.
        """
        pass
    
    def compute_importance(self, model, feature_names: List[str], 
                          sample: Union[List[float], Dict[str, float]]) -> Dict[str, Any]:
        """
        Compute feature importance for a given model and sample.
        
        Args:
            model: Trained model (RandomForestClassifier or XGBoostRegressor)
            feature_names: List of feature names
            sample: List of feature values or dict mapping feature names to values
            
        Returns:
            Dictionary with feature importances sorted by importance descending
        """
        # Convert sample dict to list if needed
        if isinstance(sample, dict):
            sample_list = [sample.get(name, 0.0) for name in feature_names]
        else:
            sample_list = sample
            
        # Try to get feature importances directly from model
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            # Normalize to sum to 1.0
            total_importance = sum(importances)
            if total_importance > 0:
                normalized_importances = [imp / total_importance for imp in importances]
            else:
                # If all importances are zero, return uniform importance
                normalized_importances = [1.0 / len(importances) for _ in importances]
        else:
            # Fall back to manual permutation importance
            normalized_importances = self._compute_permutation_importance(
                model, feature_names, sample_list
            )
        
        # Create feature importance list
        feature_importance = []
        for i, name in enumerate(feature_names):
            feature_importance.append({
                "feature": name,
                "importance": float(normalized_importances[i]) if i < len(normalized_importances) else 0.0
            })
        
        # Sort by importance descending
        feature_importance.sort(key=lambda x: x["importance"], reverse=True)
        
        return {
            "feature_importance": feature_importance
        }
    
    def _compute_permutation_importance(self, model, feature_names: List[str], 
                                      sample: List[float]) -> List[float]:
        """
        Compute permutation importance for models without feature_importances_ attribute.
        
        Args:
            model: Trained model
            feature_names: List of feature names
            sample: List of feature values
            
        Returns:
            List of normalized importances
        """
        importances = []
        
        # Get original prediction
        try:
            if hasattr(model, "predict_proba"):
                original_pred = model.predict_proba([sample])[0][1]  # Probability of positive class
            else:
                original_pred = model.predict([sample])[0]
        except Exception:
            # If prediction fails, return uniform importance
            return [1.0 / len(feature_names) for _ in feature_names]
        
        # Compute importance for each feature
        for i in range(len(feature_names)):
            if i >= len(sample):
                importances.append(0.0)
                continue
                
            # Create perturbed sample
            perturbed_sample = sample.copy()
            original_value = perturbed_sample[i]
            
            # Perturb by +10% (avoiding division by zero)
            if original_value != 0:
                perturbed_sample[i] = original_value * 1.1
            else:
                perturbed_sample[i] = 1.0  # Small positive value if original was zero
            
            # Get perturbed prediction
            try:
                if hasattr(model, "predict_proba"):
                    perturbed_pred = model.predict_proba([perturbed_sample])[0][1]
                else:
                    perturbed_pred = model.predict([perturbed_sample])[0]
                
                # Compute importance as absolute difference
                importance = abs(perturbed_pred - original_pred)
                importances.append(importance)
            except Exception:
                importances.append(0.0)
        
        # Normalize to sum to 1.0
        total_importance = sum(importances)
        if total_importance > 0:
            normalized_importances = [imp / total_importance for imp in importances]
        else:
            # If all importances are zero, return uniform importance
            normalized_importances = [1.0 / len(importances) for _ in importances]
        
        return normalized_importances
    
    @staticmethod
    def load() -> 'FeatureImportanceAgent':
        """
        Static method to create and return a FeatureImportanceAgent instance.
        
        Returns:
            FeatureImportanceAgent: A new FeatureImportanceAgent instance
        """
        return FeatureImportanceAgent()