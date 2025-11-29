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



## Workshop 3
- **Description:**

Workshop 3 focused on strengthening the predictive system’s architecture and integrating **quality assurance**, **risk management**, and **project governance** aligned with international engineering standards.

This phase redefined the architecture into three main layers — **Data Processing**, **Training**, and **Presentation** — designed for **local execution**, **fault tolerance**, and **traceability**.

Additionally, a formal **Quality and Risk Management Plan** was introduced, identifying potential risks (data corruption, dependency conflicts, overfitting, reproducibility loss) and proposing mitigation strategies under the frameworks of **ISO 9001:2015** (Quality Management Systems) and **CMMI** (Capability Maturity Model Integration).

A **Project Management Plan** was also established, defining clear team roles and an iterative **Kanban-based workflow** emphasizing documentation integrity and process control.

**Team Roles:**
| Name | Role | Responsibility |
|------|------|----------------|
| **Samuel Aljure Bernal** | Analyst | Defines requirements and maintains system traceability. |
| **Carlos Alberto Barriga Gámez** | Developer | Implements and maintains modular code structure. |
| **David Santiago Aldana González** | Tester | Executes validation and reproducibility testing. |
| **Juan Diego Álvarez Cristancho** | Manager | Coordinates project milestones and documentation. |

This workshop consolidated the system into a reproducible and auditable framework, establishing a strong foundation for the upcoming **implementation and validation phase**.

- **Workshop 3 report:** [See PDF](https://github.com/Salda1308/SystemsAnalysisDesign-WorkshopsGroup/blob/main/Workshop_3/Workshop3.pdf)

## Workshop 4
- **Description:**

 Workshop 4 was developed as the fourth phase of the sales forecasting project for Chocolates 4U, with the goal of complementing deterministic models with simulation approaches capable of evaluating system sensitivity and emerging market patterns. Based on the modular architecture defined in previous workshops, the ingestion, preprocessing, and analysis modules were integrated to prepare a numerical dataset suitable for both machine learning techniques and event-driven simulations.

The work combined a sensitivity and chaos approach using Random Forest with Gaussian noise injection to identify critical variables affecting model stability, and a spatial dynamics approach using cellular automata to represent market evolution and the formation of sales clusters. Both methods were implemented in Python following principles of modularity, traceability, and consistency with the project baseline.

This README refers to the full report [Workshop 4](https://github.com/Salda1308/SystemsAnalysisDesign-WorkshopsGroup/blob/main/Workshop_4/Workshop_4.pdf)
 and the  [Simulation_Workshop_4](https://github.com/Salda1308/SystemsAnalysisDesign-WorkshopsGroup/tree/main/Workshop_4/Simulation_Workshop_4) folder, where the source code and scripts used in the simulations are located.
