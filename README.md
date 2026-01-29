# Smart Acquirer - AI Startup Valuation & Acquisition Predictor

Smart Acquirer is an AI-powered platform that predicts startup valuations and acquisition likelihood using machine learning models trained on real-world datasets.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/jeevithgowdasr/SMART-ACQUISITION_VALUATION_PREDICTOR)

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

### Starting the Application (Production Mode)

The backend is configured to serve the frontend automatically.
1. Build the frontend:
```bash
npm run build
```
2. Start the unified server:
```bash
python -m uvicorn src.api.app:app
```

## Deployment

### 1. Backend (Render)
Click the **Deploy to Render** button above or connect your repo to Render and it will use the `render.yaml` configuration.

### 2. Frontend (Vercel - Optional)
If you want to host the frontend on Vercel:
1. Connect your repo to Vercel.
2. Set the environment variable `VITE_API_URL` to your Render backend URL.

## API Endpoints

- `POST /predict` - Get acquisition likelihood and valuation forecast
- `GET /health` - Check if models are loaded correctly
- `GET /competitors/{company_name}` - Find competitors for a company
- `GET /acquisition-targets/{acquirer_name}` - Find acquisition targets for an acquirer

## License

This project is licensed under the MIT License.

