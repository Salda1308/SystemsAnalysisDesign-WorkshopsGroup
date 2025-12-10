# Chocolate Sales Prediction - Model Training Summary

## Overview
This document summarizes the machine learning model training and comparison for chocolate sales prediction using R-based ensemble methods.

## Dataset
- **Training Data**: `IN/data_training.csv` (750 rows, 27 columns)
- **Test Data**: `IN/data_test.csv` (250 rows, 26 columns)
- **Processed Data**: `OUT/processed_data.csv`

## Models Trained and Compared

### 1. **Linear Regression** (Baseline)
- **MAE**: 11,994.91
- **Type**: Simple linear model
- **Purpose**: Baseline for comparison
- **Rank**: 3rd

### 2. **Random Forest**
- **MAE**: 21,283.07
- **Configuration**: 200 trees, 3-fold CV
- **Type**: Tree-based ensemble
- **Rank**: 4th

### 3. **XGBoost**
- **MAE**: 6,185.26
- **Configuration**: 100 rounds, depth=3, eta=0.1
- **Type**: Gradient boosting
- **Rank**: 2nd

### 4. **Stacking Ensemble** ⭐ **WINNER**
- **MAE**: 4,608.67
- **Configuration**:
  - Base models: Linear Regression, Random Forest, XGBoost
  - Meta-learner: Linear regression on base predictions
- **Type**: Ensemble of ensembles
- **Rank**: 1st

## Model Ranking

| Rank | Model | MAE |
|------|-------|-----|
| 🥇 | **Stacking Ensemble** | **4,608.67** |
| 🥈 | XGBoost | 6,185.26 |
| 🥉 | Linear Regression | 11,994.91 |
| 4th | Random Forest | 21,283.07 |

## Performance Improvement

The **Stacking Ensemble** achieves:
- **25.5%** improvement over XGBoost (best single model)
- **61.6%** improvement over Linear Regression
- **78.3%** improvement over Random Forest

## Training Details

### Data Split
- **Training Set**: 600 samples (80%)
- **Validation Set**: 150 samples (20%)
- **Test Set**: 250 samples (external)

### Cross-Validation
- **Method**: 3-fold cross-validation
- **Purpose**: Robust model evaluation and hyperparameter tuning

### Feature Engineering
- Removed target variable (`sales`) and ID columns
- Applied categorical encoding (Tone_of_Ad, Weather, Gender, Coffee_Consumption)
- Handled missing values with median imputation
- Log transformation of target variable for better distribution

## Predictions

### Output Files
- `OUT/models/best_model_R.rds` - Trained Stacking Ensemble model
- `OUT/test_predictions.csv` - Predictions on test set
- `OUT/model_comparison_results_R.json` - Comparison metrics

### Sample Predictions
The model predicts chocolate sales in the original scale (exponentiated from log scale).

Example predictions from test data:
- ID 1: 334,888.50
- ID 4: 166,902.66
- ID 6: 466,751.52

## API Integration

### Endpoints
- `GET /` - Web dashboard
- `POST /predict` - Get predictions as JSON
- `POST /predict/csv` - Get predictions as CSV download
- `GET /health` - API health status

### Model Type
The API automatically detects and uses:
- **Type**: Stacking Ensemble (3-model stack)
- **Base Models**: Linear + Random Forest + XGBoost
- **Meta-learner**: Linear regression

## How to Train/Predict

### Training
```bash
# Activate venv
.\.venv\Scripts\Activate.ps1

# Run training script
Rscript "Training Layer/compare_models.R"
```

### Making Predictions
```bash
# Via API
python "Presentation Layer/api.py"
# Then upload CSV to http://localhost:8000

# Via R directly
Rscript "Presentation Layer/predict.R" <csv_file>
```

## Key Advantages of Stacking Ensemble

1. **Combines Strengths**: Leverages complementary predictive capabilities of different model types
2. **Reduces Variance**: Meta-learner learns optimal combination of base models
3. **Robust**: Less sensitive to outliers than single models
4. **Interpretable**: Meta-model weights show contribution of each base model

## Technical Stack

- **Language**: R 4.5.2
- **ML Framework**: caret, xgboost, randomForest
- **Data Processing**: data.table
- **API**: FastAPI (Python)
- **Output Format**: JSON, CSV

## Files Modified/Created

- `Training Layer/compare_models.R` - Added Stacking Ensemble comparison
- `Presentation Layer/predict.R` - Updated for Stacking support
- `Presentation Layer/api.py` - Updated model description
- `OUT/model_comparison_results_R.json` - Comparison results
- `OUT/models/best_model_R.rds` - Trained model with metadata

---

**Status**: ✅ Production Ready
**Last Updated**: 2025-12-09
**Model**: Stacking Ensemble (R-based)
