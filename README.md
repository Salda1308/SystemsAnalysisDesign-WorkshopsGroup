#  Systems analysis design workshops 
# Analysis Workshops

This repository contains the workshops developed during the course.

## Workshop 1
- **Description:**


  
The main objective of this workshop is to analyze the "Sweet Regression" competition from a systemic perspective.

The analysis was carried out by applying a systemic approach to the competition, taking into account the concepts covered in the systems analysis and design course.
To this end, the general description, data, and regulations of the "Sweet Regression: Prediction of Chocolate Sale" competition were reviewed.

First, the system components were identified: inputs, processes, outputs, and constraints.

Each component was then examined in terms of its sensitivity to change.

Then, the potential effects of chaos and randomness were analyzed, considering both the stochastic nature of machine learning algorithms and the competitive dynamics imposed by the rules of participation.
Finally, the analysis concluded with the identification of strengths and weaknesses, highlighting the elements that make the competition suitable for a systemic study.

- **Workshop 1 report:** [See PDF](Workshop%201/Workshop%201%20Sweet%20Regression%20Competition.pdf)

## Workshop 2

- **Description:**

Workshop 2: Sweet Regression Competition Analysis was developed as the second phase of the sales prediction project for Chocolates 4U, with the objective of designing a predictive system capable of estimating sales in new regions based on marketing data, socioeconomic, and environmental factors. Based on the analysis from Workshop 1, technical constraints, functional and non-functional requirements, and a modular architecture composed of six modules (ingestion, preprocessing, analysis, modeling, validation, and export) were defined, following systems engineering principles such as modularity, traceability, and feedback control.
Sensitivity and chaos control mechanisms were also included, such as the use of fixed seeds, regularization, preprocessing standardization, and outlier detection.

The implementation was defined as combining Python for data exploration and preprocessing and R for modeling and validation using linear and regularized regression techniques, employing error metrics (MAE) and overfitting control mechanisms.

- **Workshop 2 report:**  [See PDF](https://github.com/Salda1308/SystemsAnalysisDesign-WorkshopsGroup/blob/main/Workshop_2_Design/Workshop2.pdf)
