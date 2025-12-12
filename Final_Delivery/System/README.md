# Chocolate Sales Prediction

This project is a machine learning pipeline for predicting chocolate sales using Python and R.

## Prerequisites

- Python 3.8 or higher
- R 4.0 or higher (with Rscript in PATH)
- Git (optional, for cloning)

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
- Create a virtual environment
- Install Python dependencies
- Attempt to install R packages

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
# Check Python
python --version

# Check R
Rscript --version
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

## Troubleshooting

### Common Issues

1. **R not found**: Ensure R is installed and Rscript is in your PATH
2. **Python version**: Requires Python 3.8+
3. **Dependencies**: Run `pip install -r requirements.txt` in activated environment
4. **Virtual environment**: Always activate the environment before running

### On Different Operating Systems

- **Windows**: Use `chocolate_env\\Scripts\\activate`
- **Linux/Mac**: Use `source chocolate_env/bin/activate`
- R paths are automatically detected

## Project Structure

```
├── main.py                 # Main data processing script
├── run_pipeline.py         # Complete pipeline runner
├── setup_environment.py    # Environment setup script
├── requirements.txt        # Python dependencies
├── IN/                     # Input data files
├── OUT/                    # Generated outputs
├── Data Processing Layer/  # Python data processing modules
├── Training Layer/         # R model training scripts
└── Presentation Layer/     # Web API