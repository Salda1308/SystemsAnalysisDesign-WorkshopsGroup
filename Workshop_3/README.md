# Workshop 3 – Robust Design and Quality Management  
### Chocolates 4U Predictive System

---

## Overview
This repository documents **Workshop #3** of the *Chocolates 4U Predictive System* project, developed as part of the **Sweet Regression Competition** academic initiative.  
The focus of this stage is the **refinement of the system architecture**, the integration of **quality and risk management mechanisms**, and the establishment of a formal **project management framework** aligned with engineering standards.

The system aims to predict chocolate sales using regression analysis while adhering to engineering principles such as modularity, traceability, and reproducibility.

---

## Workshop Objectives
- Refine and update the predictive system’s architecture to ensure robustness, modularity, and fault tolerance.  
- Integrate **ISO 9001** (Quality Management Systems) and **CMMI Level 2–3** (Capability Maturity Model Integration) principles into the design process.  
- Conduct a structured **Quality and Risk Analysis**, identifying potential failure points and mitigation strategies.  
- Define a **Project Management Plan** including team roles, workflow, and milestones.  
- Document **Incremental Improvements** from previous workshops (Systemic Analysis and System Design).

---

## Deliverables
This workshop produced the following deliverables:

| Deliverable | Description |
|--------------|-------------|
| **Refined Architecture Diagram** | Three-layer architecture (Data Processing, Training, Presentation) emphasizing local reproducibility and control. |
| **Quality and Risk Management Plan** | Risk identification, mitigation strategies, and monitoring approach aligned with ISO 9001 and CMMI. |
| **Project Management Plan** | Definition of roles (Analyst, Developer, Tester, Manager), workflow, and milestones. |
| **Incremental Improvements Report** | Summary of how the system evolved from conceptual analysis to robust design. |
| **Technical References Section** | Integration of literature on ISO 9001, CMMI, and Six Sigma methodologies. |

---

## Team Roles

| Team Member | Role | Responsibilities |
|--------------|------|------------------|
| **Samuel Aljure Bernal** | Analyst | Defines requirements, maintains traceability between design artifacts, and ensures conceptual alignment. |
| **Carlos Alberto Barriga Gámez** | Developer | Implements and maintains system modules, ensuring compliance with defined architecture. |
| **David Santiago Aldana González** | Tester | Executes validation and reproducibility tests, verifies model accuracy and preprocessing correctness. |
| **Juan Diego Álvarez Cristancho** | Manager | Coordinates the workflow, oversees progress tracking, and ensures compliance with documentation and quality standards. |

---

## System Architecture (Workshop 3)
The architecture defined in this workshop consists of three main layers:

1. **Data Processing Layer** – Handles ingestion, validation, preprocessing, and feature selection.  
2. **Training Layer** – Manages regression modeling, validation, and performance evaluation.  
3. **Presentation Layer** – Produces interpretable reports and exports prediction results in standardized formats.

All components include **validation checkpoints**, **version control**, and **fault isolation mechanisms**, consistent with ISO 9001 documentation and CMMI process traceability.

---

## Quality and Risk Analysis
Key risks identified include:
- Data corruption or missing values.  
- Environment dependency or package conflicts.  
- Model overfitting and reproducibility loss.  
- Execution interruptions during local runs.

Mitigation strategies:
- Schema validation and data backup policies.  
- Controlled virtual environments (`conda`, `renv`).  
- Cross-validation and version tracking.  
- Logging and checkpoint mechanisms for recovery.

These controls ensure system stability and compliance with ISO 9001 process validation and CMMI configuration management.

---

## Project Management Framework
Workshop #3 formalized the team’s **Kanban-based workflow**, emphasizing continuous improvement and traceability.  
Tasks are categorized as *To Do*, *In Progress*, *Under Review*, and *Completed* using Trello / GitHub Projects.

**Management highlights:**
- Weekly reviews for progress validation and documentation control.  
- Versioning via Git with milestone tagging.  
- LaTeX-based technical reporting for formal documentation consistency.

---

## Incremental Improvements Summary
| Workshop | Focus | Outcome |
|-----------|--------|----------|
| **#1 – Systemic Analysis** | Defined inputs, processes, and system constraints; identified instability and chaos factors. |
| **#2 – System Design** | Built modular architecture and requirement specification. |
| **#3 – Robust Design & Quality Integration** | Added quality assurance, risk management, and project governance following ISO 9001 and CMMI. |

---

