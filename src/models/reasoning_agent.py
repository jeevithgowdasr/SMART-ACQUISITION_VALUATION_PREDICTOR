import json
import pandas as pd
import os


def llm_call(system_prompt, user_prompt):
    """
    Mock implementation of LLM call function.
    In a real implementation, this would call an actual LLM API.
    """
    # This is a mock response that follows the expected schema
    import random
    
    # Simple logic to determine decision based on prompts
    mna_likelihood = 0.5
    overall_synergy_score = 0.5
    
    # Try to extract values from the user prompt
    try:
        lines = user_prompt.split("\n")
        for line in lines:
            if "mna_likelihood:" in line:
                mna_likelihood = float(line.split(":")[1].strip())
            elif "overall_synergy_score:" in line:
                overall_synergy_score = float(line.split(":")[1].strip())
    except:
        pass
    
    # Determine decision based on the values
    if mna_likelihood >= 0.7 and overall_synergy_score >= 0.6:
        decision = "ACQUIRE"
    elif 0.4 <= mna_likelihood < 0.7 or (mna_likelihood >= 0.7 and overall_synergy_score < 0.6):
        decision = "INVESTIGATE"
    else:
        decision = "PASS"
    
    confidence = min(1.0, max(0.0, (mna_likelihood + overall_synergy_score) / 2))
    
    return json.dumps({
        "decision": decision,
        "confidence": confidence,
        "rationale": [
            "M&A likelihood is {:.1f}%".format(mna_likelihood * 100),
            "Synergy score is {:.1f}".format(overall_synergy_score),
            "Valuation appears reasonable",
            "Team strength is adequate",
            "Market conditions are favorable"
        ],
        "key_drivers": [
            {"name": "mna_likelihood", "value": mna_likelihood, "impact": "positive" if mna_likelihood > 0.5 else "negative"},
            {"name": "synergy_score", "value": overall_synergy_score, "impact": "positive" if overall_synergy_score > 0.5 else "negative"}
        ],
        "suggested_actions": [
            "Conduct detailed due diligence",
            "Negotiate terms with founder",
            "Review financial projections"
        ]
    })


# Load the VC evaluation dataset for enhanced reasoning
def load_vc_evaluation_data():
    """Load the VC evaluation dataset for enhanced reasoning capabilities"""
    try:
        # Check if the dataset files exist in the project root
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'enhanced_training_data.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            return df
        else:
            # Return empty dataframe with expected columns
            return pd.DataFrame(columns=['prompt', 'completion', 'evaluation_aspect'])
    except Exception as e:
        print(f"Warning: Could not load VC evaluation data: {e}")
        return pd.DataFrame(columns=['prompt', 'completion', 'evaluation_aspect'])


# Load the dataset at module level
VC_EVALUATION_DATA = load_vc_evaluation_data()


SYSTEM_PROMPT = """
You are SmartAcquirer's objective M&A analyst assistant.
Your job is to read structured, factual inputs (funding, team, synergy, valuation, and model scores) and produce:
- a short acquisition recommendation,
- a concise justification,
- and a strict JSON explanation following the required schema.

Rules:
- Use ONLY the numbers given; never invent or hallucinate facts.
- Keep output concise and factual; max 5 rationale items.
- Output MUST be valid JSON matching the schema exactly.
- No text outside JSON.
- Confidence must be between 0.0 and 1.0.
- If an input field is missing, explicitly mention that in rationale.

Enhanced with VC Evaluation Dataset:
- Incorporate insights from real VC evaluation practices
- Consider multiple evaluation aspects: business model, market opportunity, team, competition, financials, risk, traction, technology, funding
- Provide more nuanced recommendations based on industry best practices
"""

USER_PROMPT_TEMPLATE = """
INPUT FACTS:
Funding:
  num_rounds: {{num_rounds}}
  total_raised_usd: {{total_raised_usd}}
  avg_round_size: {{avg_round_size}}
  last_round_type: "{{last_round_type}}"

Team:
  team_strength_score: {{team_strength_score}}
  founder_count: {{founder_count}}
  avg_experience: {{avg_experience}}
  exits_count: {{exits_count}}

Synergy:
  market_similarity: {{market_similarity}}
  tech_similarity: {{tech_similarity}}
  revenue_synergy_score: {{revenue_synergy_score}}
  cost_synergy_score: {{cost_synergy_score}}
  overall_synergy_score: {{overall_synergy_score}}

Valuation:
  revenue_ttm: {{revenue_ttm}}
  revenue_growth_mom: {{revenue_growth_mom}}
  revenue_multiple_proxy: {{revenue_multiple_proxy}}
  valuation_proxy_current: {{valuation_proxy_current}}
  valuation_forecast_usd: {{valuation_forecast_usd}}

Model Scores:
  mna_likelihood: {{mna_likelihood}}

INSTRUCTIONS:
Using only the facts above, output a JSON object with this exact schema:

{{
  "decision": "ACQUIRE" | "PASS" | "INVESTIGATE",
  "confidence": float,
  "rationale": ["short point 1", ...],
  "key_drivers": [
     {{"name":"feature_name","value":number,"impact":"positive"|"negative"|"neutral"}}
  ],
  "suggested_actions": ["action 1", "action 2"]
}}

Decision rules:
- ACQUIRE if mna_likelihood >= 0.7 AND overall_synergy_score >= 0.6.
- INVESTIGATE if 0.4 <= mna_likelihood < 0.7 OR conflicting signals.
- PASS otherwise.

Confidence = average(mna_likelihood, overall_synergy_score), clipped 0–1.

Return ONLY valid JSON. No commentary outside JSON.

Enhanced Evaluation Context:
Based on VC evaluation practices, consider these aspects:
1. Business Model: Scalability and sustainability
2. Market Opportunity: Size and growth potential
3. Team: Experience and track record
4. Competition: Advantages and barriers to entry
5. Financials: Projections and metrics
6. Risk: Challenges and mitigation strategies
7. Traction: Customer feedback and growth
8. Technology: Innovation and IP
9. Funding: Use of funds and runway
"""

class ReasoningAgent:
    def __init__(self):
        """
        Initialize ReasoningAgent with no arguments.
        """
        # Load VC evaluation data for enhanced reasoning
        self.vc_data = VC_EVALUATION_DATA
        pass
    
    def explain(self, features: dict) -> dict:
        """
        Generate an explanation for M&A decision based on input features.
        
        Args:
            features: Dictionary containing all relevant features for decision making
            
        Returns:
            Dictionary with decision, confidence, rationale, key drivers, and suggested actions
        """
        # Format the user prompt with real values from features
        user_prompt = USER_PROMPT_TEMPLATE.format(
            num_rounds=features.get('num_rounds', 0),
            total_raised_usd=features.get('total_raised_usd', 0),
            avg_round_size=features.get('avg_round_size', 0),
            last_round_type=features.get('last_round_type', 'Unknown'),
            team_strength_score=features.get('team_strength_score', 0),
            founder_count=features.get('founder_count', 0),
            avg_experience=features.get('avg_experience', 0),
            exits_count=features.get('exits_count', 0),
            market_similarity=features.get('market_similarity', 0),
            tech_similarity=features.get('tech_similarity', 0),
            revenue_synergy_score=features.get('revenue_synergy_score', 0),
            cost_synergy_score=features.get('cost_synergy_score', 0),
            overall_synergy_score=features.get('overall_synergy_score', 0),
            revenue_ttm=features.get('revenue_ttm', 0),
            revenue_growth_mom=features.get('revenue_growth_mom', 0),
            revenue_multiple_proxy=features.get('revenue_multiple_proxy', 0),
            valuation_proxy_current=features.get('valuation_proxy_current', 0),
            valuation_forecast_usd=features.get('valuation_forecast_usd', 0),
            mna_likelihood=features.get('mna_likelihood', 0)
        )
        
        # Try to call the LLM
        try:
            # Assume llm_call function exists
            llm_response = llm_call(SYSTEM_PROMPT, user_prompt)
            result = json.loads(llm_response)
            
            # Validate required fields
            if self._validate_response(result):
                return result
        except (json.JSONDecodeError, Exception):
            pass
        
        # Retry with instruction to return only valid JSON
        try:
            retry_prompt = user_prompt + "\n\nReturn ONLY valid JSON following the schema."
            llm_response = llm_call(SYSTEM_PROMPT, retry_prompt)
            result = json.loads(llm_response)
            
            # Validate required fields
            if self._validate_response(result):
                return result
        except (json.JSONDecodeError, Exception):
            pass
        
        # If both attempts fail, return error
        return {"error": "llm_failure"}
    
    def _validate_response(self, response: dict) -> bool:
        """
        Validate that the response contains all required fields with correct types.
        
        Args:
            response: The LLM response to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["decision", "confidence", "rationale", "key_drivers", "suggested_actions"]
        
        # Check that all required fields exist
        for field in required_fields:
            if field not in response:
                return False
        
        # Check decision is one of the allowed values
        if response["decision"] not in ["ACQUIRE", "PASS", "INVESTIGATE"]:
            return False
        
        # Check confidence is a float between 0 and 1
        if not isinstance(response["confidence"], (int, float)) or not (0 <= response["confidence"] <= 1):
            return False
        
        # Check rationale is a list with max 5 items
        if not isinstance(response["rationale"], list) or len(response["rationale"]) > 5:
            return False
        
        # Check key_drivers is a list
        if not isinstance(response["key_drivers"], list):
            return False
        
        # Check suggested_actions is a list with 1-3 items
        if not isinstance(response["suggested_actions"], list) or not (1 <= len(response["suggested_actions"]) <= 3):
            return False
        
        return True
    
    @staticmethod
    def load() -> 'ReasoningAgent':
        """
        Static method to create and return a ReasoningAgent instance.
        
        Returns:
            ReasoningAgent: A new ReasoningAgent instance
        """
        return ReasoningAgent()