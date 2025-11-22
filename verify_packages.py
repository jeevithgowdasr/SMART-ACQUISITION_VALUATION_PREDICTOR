import sys
print("Python version:", sys.version)

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print("✗ Failed to import pandas:", e)

try:
    import numpy as np
    print("✓ numpy imported successfully")
except ImportError as e:
    print("✗ Failed to import numpy:", e)

try:
    import sklearn
    print("✓ scikit-learn imported successfully")
except ImportError as e:
    print("✗ Failed to import scikit-learn:", e)

try:
    import xgboost
    print("✓ xgboost imported successfully")
except ImportError as e:
    print("✗ Failed to import xgboost:", e)

try:
    import lightgbm
    print("✓ lightgbm imported successfully")
except ImportError as e:
    print("✗ Failed to import lightgbm:", e)

try:
    import fastapi
    print("✓ fastapi imported successfully")
except ImportError as e:
    print("✗ Failed to import fastapi:", e)

try:
    import uvicorn
    print("✓ uvicorn imported successfully")
except ImportError as e:
    print("✗ Failed to import uvicorn:", e)

try:
    import joblib
    print("✓ joblib imported successfully")
except ImportError as e:
    print("✗ Failed to import joblib:", e)