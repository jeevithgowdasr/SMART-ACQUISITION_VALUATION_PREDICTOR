# Smart Acquirer - AI Startup Valuation & Acquisition Predictor

Smart Acquirer is an AI-powered platform that predicts startup valuations and acquisition likelihood using machine learning models trained on real-world datasets.

## Project Structure

```
smart-acquirer/
├── datasets/                 # Crunchbase datasets
├── data/
│   ├── raw/                  # Raw startup data
│   └── processed/            # Processed features
├── models/                   # Trained ML models
├── src/
│   ├── api/                  # FastAPI backend
│   ├── models/               # AI agents and training scripts
│   ├── pipeline/             # Data processing pipeline
│   └── components/           # React frontend components
├── train_models.py           # Main training script
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- pip package manager

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
npm install
```

### Training Models with Crunchbase Data

The project includes a complete pipeline to process Crunchbase datasets and train new models:

1. **Process datasets**:
```bash
python src/pipeline/process_datasets.py
```

2. **Train models**:
```bash
python src/models/train_with_crunchbase.py
```

3. **Or run the complete pipeline**:
```bash
python train_models.py
```

### Starting the API Server

```bash
uvicorn src.api.app:app --reload
```

The API will automatically use the new Crunchbase-trained models if available.

### Starting the Frontend

```bash
npm run dev
```

## API Endpoints

- `POST /predict` - Get acquisition likelihood and valuation forecast
- `GET /health` - Check if models are loaded correctly
- `GET /competitors/{company_name}` - Find competitors for a company
- `GET /acquisition-targets/{acquirer_name}` - Find acquisition targets for an acquirer

## Model Architecture

The system uses multiple AI agents to analyze different aspects of startups:

1. **Funding Agent** - Analyzes funding history and patterns
2. **Team Agent** - Evaluates team strength and founder experience
3. **Synergy Agent** - Calculates acquisition synergies
4. **Valuation Agent** - Estimates current and future valuations
5. **Risk Agent** - Assesses business and market risks
6. **Benchmark Agent** - Compares startups against industry benchmarks
7. **Business Model Agent** - Evaluates business model strength
8. **Reasoning Agent** - Provides explanations for predictions
9. **Decision Score Agent** - Computes overall acquisition decision scores

## Data Processing Pipeline

1. **Batch Processing** (Offline)
   ```
   Raw Crunchbase Data → AI Agents → Feature Files → ML Training → Trained Models
   ```

2. **Real-time Processing** (Online)
   ```
   JSON Request → AI Agents → Feature Extraction → ML Inference → Predictions
   ```

## ML Models

Two primary models have been trained:

1. **Meta Model** (Classification)
   - Predicts acquisition likelihood (0-1 probability)
   - Uses Random Forest classifier
   - Trained on funding, team, and synergy features

2. **Valuation Model** (Regression)
   - Forecasts 12-month forward valuations
   - Uses XGBoost regressor (falls back to Random Forest)
   - Trained on comprehensive financial and operational features

## Testing the System

To test the dataset feeding process:

1. Ensure the API server is running:
   ```
   uvicorn src.api.app:app --reload
   ```

2. Send a sample request to the prediction endpoint:
   ```json
   {
     "funding_json": {
       "rounds": [
         {"type": "Seed", "amount": "500000"},
         {"type": "Series A", "amount": "2000000"}
       ]
     },
     "team_json": {
       "founders": [
         {"experience_years": 5, "has_exit": true},
         {"experience_years": 3, "has_exit": false}
       ]
     },
     "acquirer_json": {
       "industry": "tech",
       "market": "saas",
       "tech_stack": ["python", "react"],
       "team_size": 500
     },
     "target_json": {
       "industry": "tech",
       "market": "saas",
       "tech_stack": ["python", "angular"],
       "team_size": 50
     },
     "financials_json": {
       "monthly_revenue_usd": 100000,
       "revenue_growth_mom": 15.0,
       "gross_margin": 0.8
     }
   }
   ```

## Current Status

✅ Crunchbase datasets have been successfully processed
✅ ML models trained with Crunchbase data are active
✅ API is running and accepting requests
✅ Models are serving predictions in real-time
✅ Frontend application is fully functional with modern UI
✅ All route components (Dashboard, History, Settings) are implemented
✅ Complete form validation and error handling
✅ Responsive design with Tailwind CSS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.