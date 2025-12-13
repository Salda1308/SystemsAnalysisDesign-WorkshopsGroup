# Chocolate Sales Prediction

This project is a machine learning pipeline for predicting chocolate sales using Python and R.

## Prerequisites

- Python 3.8 or higher
- R 4.0 or higher (with Rscript in PATH)
- Git (optional, for cloning)
- Windows PowerShell or Terminal access

**Important**: Ensure R is properly installed and accessible via command line. The setup will verify R installation automatically.

## Installation

### 1. Clone or download the repository

```bash
git clone <repository-url>
cd chocolate-sales-prediction
```

### 2. Set up Python environment

#### Option A: Using the setup script (recommended)

```bash
python setup_environment.py
```

This will:
- Create a virtual environment (venv/)
- Install Python dependencies from requirements.txt
- Verify R installation and version
- Automatically install required R packages
- Run verification tests for both Python and R environments

#### Option B: Manual setup

```bash
# Create virtual environment
python -m venv chocolate_env

# Activate environment
# Windows:
chocolate_env\\Scripts\\activate
# Linux/Mac:
source chocolate_env/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Install R and packages

Download and install R from: https://cran.r-project.org/

Make sure Rscript is in your PATH.

Install required R packages:

```bash
# In R console or using Rscript:
Rscript -e "install.packages(c('caret', 'randomForest', 'xgboost', 'jsonlite', 'data.table'), repos='https://cloud.r-project.org/')"
```

### 4. Verify installation

```bash
# Automated verification script
python verify_r_installation.py

# Manual checks
python --version
Rscript --version

# Test R packages
Rscript -e "library(caret); library(randomForest); library(xgboost)"
```

## Quick Start

### Run Complete Pipeline

```bash
# Activate environment first
# Windows:
chocolate_env\\Scripts\\activate
# Linux/Mac:
source chocolate_env/bin/activate

python run_pipeline.py
```

### Start Web Interface

```bash
python "Presentation Layer/api.py"
```

Then open: **http://localhost:8000**

## Model Training Improvements

The system now includes enhanced model training with the following features:

### Four Robust Models
1. **XGBoost**: Direct implementation using native xgboost library for better stability
2. **Random Forest**: Ensemble method with 1000 trees
3. **Linear Regression**: Baseline model for comparison
4. **Stacking Ensemble**: Meta-model combining all base models for optimal performance

### Key Enhancements
- **Robust Data Preprocessing**: Handles categorical variables, missing values, and feature engineering
- **Consistent Encoding**: Shared categorical levels between training and test sets
- **Error Handling**: Graceful fallbacks if individual models fail
- **Cross-Validation**: 5-fold CV for Random Forest and Linear Regression, 3-fold for XGBoost
- **Performance Tracking**: MAE (Mean Absolute Error) comparison across all models

### Model Selection
The system automatically selects the best performing model based on validation MAE and saves it for predictions.

## Troubleshooting

### Common Issues

1. **R not found**: Ensure R is installed and Rscript is in your PATH
   - Run `verify_r_installation.py` to diagnose R setup issues
   - On Windows, add R installation directory to PATH

2. **Python version**: Requires Python 3.8+

3. **Dependencies**: Run `pip install -r requirements.txt` in activated environment

4. **Virtual environment**: Always activate the environment before running
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

5. **XGBoost issues**: If XGBoost fails to train:
   - Verify R package installation: `Rscript -e "library(xgboost)"`
   - The system will fallback to other models automatically

6. **Model training failures**: Check for:
   - Sufficient data in training set
   - Properly formatted CSV files
   - No missing target variable (sales column)

### On Different Operating Systems

- **Windows**: Use `chocolate_env\\Scripts\\activate`
- **Linux/Mac**: Use `source chocolate_env/bin/activate`
- R paths are automatically detected

## Project Structure

```
├── main.py                     # Main data processing script
├── run_pipeline.py             # Complete pipeline runner
├── setup_environment.py        # Environment setup script
├── verify_r_installation.py    # R verification script
├── requirements.txt            # Python dependencies
├── venv/                       # Virtual environment (created by setup)
├── IN/                         # Input data files
│   ├── data_training.csv
│   └── data_test.csv
├── OUT/                        # Generated outputs
│   ├── processed_data.csv
│   ├── test_predictions.csv
│   ├── model_comparison_results_R.json
│   └── models/                 # Trained model files
├── Data Processing Layer/      # Python data processing modules
├── Training Layer/             # Enhanced R model training
│   └── compare_models.R        # Four-model comparison script
└── Presentation Layer/         # Web API and interface
    ├── api.py
    ├── index.html
    └── predict.R