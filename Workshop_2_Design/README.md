# Sweet Regression Competition — Workshop 2


This repository contains the design and system specification for the **Sweet Regression Competition** developed for *Chocolates 4U*.  
The goal is to build a predictive framework capable of estimating chocolate sales in new regions based on marketing exposure, socio-economic indicators, and environmental factors.

This document extends the analytical findings from **Workshop #1**, transforming them into a structured system architecture, requirement set, and implementation plan.

- **Workshop 2 report:**  [See PDF](https://github.com/Salda1308/SystemsAnalysisDesign-WorkshopsGroup/blob/main/Workshop_2_Design/Workshop2.pdf)
---

## Authors
- **Samuel Aljure Bernal** — 20202020111  
- **Carlos Alberto Barriga Gámez** — 20222020179  
- **David Santiago Aldana González** — 20222020158  
- **Juan Diego Álvarez Cristancho** — 20221020076  

## Background

### Workshop #1 Summary
The first workshop established the analytical foundations and identified key constraints affecting model performance:
- The model must be implemented in **R**.
- Limited submission attempts (maximum 10).
- Moderate dataset size (27 variables × 750 records).
- Relative grading (peer-based performance).

The findings highlighted the need for **reproducibility**, **efficiency**, and **robustness** against experimental limitations.

---

## System Requirements

### Functional Requirements
- **FR1:** Data ingestion and validation of structured `.csv` datasets.  
- **FR2:** Preprocessing (normalization, encoding, outlier detection, correlation analysis).  
- **FR3:** Multiple regression modeling (linear, regularized, and ensemble-based).  
- **FR4:** Cross-validation and early stopping to control overfitting.  
- **FR5:** Experiment tracking and reproducibility with logged seeds and metrics.  
- **FR6:** Standardized prediction export (`.csv` format).

### Non-Functional Requirements
- **Performance:** <5 minutes per model training on standard hardware.  
- **Reliability:** >99% successful executions.  
- **Interpretability:** Include feature importance and residual visualizations.  
- **Scalability:** Handle 2× larger datasets without redesign.  
- **Usability:** Modular, documented, and easy to execute.  
- **Security:** All processing is local.

---

## System Architecture

### Modules
1. **Data Ingestion Module** — Loads and validates training/testing data.  
2. **Preprocessing Module** — Handles encoding, normalization, and outlier detection.  
3. **Feature Analysis Module** — Performs correlation and ANOVA to identify key predictors.  
4. **Modeling Engine** — Trains multiple regression models using MAE as the main metric.  
5. **Validation & Control Unit** — Integrates cross-validation and early stopping.  
6. **Output & Reporting Module** — Exports predictions and generates performance reports.

### Core Principles
- **Modularity** — Independent, reusable components.  
- **Traceability** — Full logging from input to output.  
- **Feedback Control** — Continuous validation loop to minimize error.  
- **Scalability & Observability** — Transparent, extensible design.

---

## Handling Sensitivity and Chaos

To mitigate instability and chaotic behavior in data and models, the system integrates:
- Fixed random seeds for reproducibility.  
- Regularization and correlation-based feature reduction.  
- Consistent preprocessing pipelines.  
- Early stopping when validation MAE stagnates.  
- Outlier detection and residual monitoring.  
- Automated error logging and rollback capabilities.

---

## Technical Stack

### Programming Languages
- **Python** (Analytical & Exploratory Environment)  
  Used for data exploration, visualization, and feature analysis.  
  **Libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `scikit-learn`, `xgboost`

- **R** (Modeling & Validation Environment)  
  Used for regression modeling, cross-validation, and final submission.  
  **Libraries:** `tidyverse`, `caret`, `glmnet`, `xgboost`, `ggplot2`

---

## Implementation Plan

1. **Data Ingestion** — Read and validate `.csv` datasets, producing a `data_report.txt`.  
2. **Preprocessing** — Perform normalization, encoding, and outlier filtering (Python).  
3. **Feature Analysis** — Conduct correlation and ANOVA with visual outputs.  
4. **Modeling Engine** — Train multiple regression models (R) and record MAE.  
5. **Validation Module** — Detect overfitting and adjust parameters.  
6. **Output & Reporting** — Generate `.csv` predictions and visual reports.  



# Chocolate Sales Data Analysis

### Requirements
- Python 3.x
- Libraries: pandas, matplotlib, statsmodels, scikit-learn, numpy

### Install Dependencies
```bash
pip install pandas matplotlib statsmodels scikit-learn numpy
```

## Usage

Run the analysis scripts in the following order to reproduce the results:

1. `CompleteAnalysis.py` - Performs initial data exploration, distribution analysis, encoding, correlations, and ANOVA.
2. `Boxplots.py` - Generates boxplots for all numerical features.
3. `CorrelationHeatmap.py` - Creates a correlation heatmap.
4. `FeatureImportance.py` - Computes feature importance using ANOVA.
5. `ScatterCorrelations.py` - Produces scatter plots with correlations against sales.

Execute each script individually or run them sequentially. Visualizations will be saved as PNG files in the project directory.

## Data Analysis

In this project, a comprehensive analysis of sales data from a chocolate company was conducted using the `data_training.csv` dataset. The analysis focused on exploring variable distributions, identifying correlations, assessing feature importance, and visualizing patterns through statistical charts. Below, the process and techniques applied are detailed.

### 1. Initial Data Exploration

- **Loading and Basic Description**: Data was loaded using pandas. An informative summary (`train.info()`), descriptive statistics (`train.describe()`), and a check for missing values (`train.isnull().sum()`) were generated.
- **Variable Definition**: All dataset columns were documented, including marketing variables (such as GRPs for web, TV, and Facebook), regional characteristics (weather, temperature, etc.), demographic variables (internet access, education, etc.), and the target `sales` (sales).

### 2. Distribution Analysis

- **Sales Histogram**: A histogram was created to visualize the sales distribution, using Velleman's rule to determine the number of intervals (approximately 27 intervals for 750 observations).
- **Frequency by Ranges**: A table was generated with sales ranges and their corresponding frequencies.

### 3. Categorical Variable Encoding

- Categorical variables (`Tone_of_Ad`, `Weather`, `Coffee_Consumption`) were mapped to numerical values to enable quantitative analysis:
  - `Tone_of_Ad`: funny=2, emotional=1, serious=0
  - `Weather`: sunny=2, cloudy=1, rainy=0
  - `Coffee_Consumption`: high=2, medium=1, low=0

### 4. Correlation Analysis

- **Linear Correlation**: Pearson correlation was calculated between all numerical variables and sales, sorted by importance.
- **Correlation Heatmap**: A heatmap was generated to visualize correlations between all numerical variables, facilitating the identification of strong or weak relationships.
- **Scatter Plots**: Scatter plots were created for each numerical variable against sales, including linear regression lines and correlation coefficients to assess linear relationships.

### 5. Variance Analysis (ANOVA)

- An ANOVA model was performed to evaluate the statistical significance of each predictor variable on sales.
- Variables were sorted by p-value (`PR(>F)`) to identify the most influential ones.
- **Feature Importance**: A horizontal bar chart was generated showing the top 15 variables by F-statistic (log-scaled), highlighting the most relevant features for predicting sales.

### 6. Additional Visualizations

- **Boxplots**: Boxplots were created for all numerical variables in a 6x4 grid, allowing identification of outliers, medians, and interquartile ranges.


- All visualizations were saved as high-resolution PNG images 

This analysis provides a solid foundation for understanding the factors influencing sales, identifying key variables such as marketing campaigns, regional characteristics, and demographics.

## Files

- `data_training.csv`: The training dataset containing sales and feature data.
- `CompleteAnalysis.py`: Main analysis script for exploration, correlations, and ANOVA.
- `Boxplots.py`: Script to generate boxplots of numerical features.
- `CorrelationHeatmap.py`: Script for creating the correlation heatmap.
- `FeatureImportance.py`: Script for ANOVA-based feature importance.
- `ScatterCorrelations.py`: Script for scatter plots with correlations.
- `*.png`: Generated visualization images.
