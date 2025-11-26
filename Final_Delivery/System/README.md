# Chocolate Sales Prediction - R-Powered ML Pipeline

## 🎯 Project Overview

3-layer machine learning pipeline for chocolate sales prediction:
- **Layer 1 (Python)**: Data processing and statistical analysis
- **Layer 2 (R)**: Model training and selection
- **Layer 3 (Python API + Web)**: Predictions and visualization

## 🚀 Quick Start

### Run Complete Pipeline

```bash
python run_pipeline.py
```

This will:
1. Process raw data (`main.py`)
2. Train and compare models in R
3. Generate visualizations
4. Save the best model

### Start Web Interface

```bash
python "Presentation Layer/api.py"
```

Then open: **http://localhost:8000**

## 📁 Project Structure

```
WORKSHOP4/
├── IN/                          # Input data
├── OUT/                         # Outputs
│   ├── processed_data.csv      # Processed dataset
│   ├── *.png                   # Visualizations
│   ├── model_comparison_results_R.json
│   └── models/
│       └── best_model_R.rds    # Trained R model
├── Data Processing Layer/
│   ├── main.py                 # Data processing
│   └── DataIngestionModule.py
├── Training Layer/
│   └── compare_models.R        # R model training
├── Presentation Layer/
│   ├── api.py                  # FastAPI server
│   ├── predict.R               # R prediction script
│   └── index.html              # Web dashboard
├── run_pipeline.py             # Master script
└── docker-compose.yml          # Docker deployment
```

## 🔬 What Each Layer Does

### Layer 1: Data Processing (Python)
- Loads raw data from `IN/`
- Statistical analysis and feature engineering
- Generates visualizations (heatmaps, boxplots, etc.)
- Outputs: `OUT/processed_data.csv` + PNG files

### Layer 2: Training (R)
- Compares 4 models: Linear, Random Forest, GBM, XGBoost
- Cross-validation with 5 folds
- Selects best model based on MAE
- Saves model to `OUT/models/best_model_R.rds`

### Layer 3: Presentation (Python + R)
- FastAPI serves web interface
- Calls R for predictions via `predict.R`
- Web dashboard shows visualizations and results
- Upload CSV to get predictions

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up --build

# Access
http://localhost:8000
```

## 📊 Model Results

The R training script compares:
1. Linear Regression (baseline)
2. Random Forest
3. Gradient Boosting (GBM)
4. XGBoost ⭐ (typically wins)

Results saved to: `OUT/model_comparison_results_R.json`

## 🔧 Manual Steps

If you want to run each step individually:

```bash
# Step 1: Process data
python main.py

# Step 2: Train models in R
Rscript "Training Layer/compare_models.R"

# Step 3: Start API
python "Presentation Layer/api.py"
```

## 📝 API Endpoints

- `GET /` - Web dashboard
- `GET /health` - API health check
- `POST /predict` - Get predictions (JSON)
- `POST /predict/csv` - Download predictions as CSV

## 🛠️ Technologies

- **Python**: pandas, numpy, scikit-learn, matplotlib, seaborn, FastAPI
- **R**: caret, xgboost, randomForest, gbm, jsonlite
- **Web**: HTML, CSS, JavaScript
- **Deployment**: Docker

## 📌 Notes

- All comments in English (student-friendly style)
- R is the primary training engine
- Python handles data prep and API
- Model comparison ensures best algorithm selection

---

**Status**: ✅ Production-ready R-powered ML pipeline