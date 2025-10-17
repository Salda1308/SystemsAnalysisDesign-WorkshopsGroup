# Sweet Regression Competition — Workshop 2

## Overview
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

