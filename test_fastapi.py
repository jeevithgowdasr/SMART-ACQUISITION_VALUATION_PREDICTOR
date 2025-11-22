from fastapi import FastAPI
from src.models.team_agent import TeamAgent
import traceback
import json
import math

app = FastAPI()
team_agent = TeamAgent()

@app.get("/test")
def test():
    return {"message": "Test endpoint working"}

@app.get("/competitors/{company_name}")
def get_competitors(company_name: str):
    try:
        print(f"Received request for competitors of: {company_name}")
        competitors = team_agent.find_competitors(company_name)
        print(f"Found {len(competitors)} competitors")
        
        # Deep check for NaN values
        for i, competitor in enumerate(competitors):
            for key, value in competitor.items():
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        print(f"Found invalid float at competitors[{i}]['{key}']: {value}")
                        competitor[key] = 0.0  # Replace with valid value
        
        # Test JSON serialization before returning
        try:
            json.dumps(competitors)
            print("JSON serialization successful")
        except Exception as e:
            print(f"JSON serialization failed: {e}")
            # Return a simplified response for debugging
            return {"competitors": [], "error": "JSON serialization failed"}
        
        return {"competitors": competitors}
    except Exception as e:
        print(f"Error in get_competitors: {e}")
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)