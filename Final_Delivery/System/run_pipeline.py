# Master Pipeline Script
# Executes the complete ML pipeline from data processing to model deployment
# This is a student project for chocolate sales prediction

import subprocess
import sys
import platform
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).parent

# Set R path based on OS
# Try to find Rscript in PATH first, fallback to common locations
r_available = False
try:
    result = subprocess.run(["Rscript", "--version"], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        r_available = True
        R_PATH = "Rscript"
except (FileNotFoundError, subprocess.TimeoutExpired):
    pass

if not r_available:
    # Try fallback paths
    if platform.system() == "Windows":
        fallback_paths = [
            r"C:\Program Files\R\R-4.5.2\bin\Rscript.exe",
            r"C:\Program Files\R\R-4.4.1\bin\Rscript.exe",
            r"C:\Program Files\R\R-4.3.3\bin\Rscript.exe",
            "Rscript.exe"
        ]
    else:
        fallback_paths = ["Rscript"]

    for path in fallback_paths:
        try:
            result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                R_PATH = path
                r_available = True
                break
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue

if not r_available:
    print("❌ R not found. Please install R from https://cran.r-project.org/")
    sys.exit(1)

def print_step(step_num, description):
    """Print a formatted step header"""
    print("\n" + "="*70)
    print(f"STEP {step_num}: {description}")
    print("="*70 + "\n")

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"Running: {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Error: {description} failed")
        print(result.stderr)
        return False

    print(f"✓ {description} completed successfully")
    if result.stdout:
        print(result.stdout)
    return True

def main():
    """Execute the complete pipeline"""

    print("\n" + "="*70)
    print("CHOCOLATE SALES PREDICTION - COMPLETE PIPELINE")
    print("3-Layer Architecture: Python → R → Python API")
    print("="*70)

    # Detect Python executable - prefer venv if available
    python_exe = sys.executable

    # Step 1: Data Processing (Python)
    print_step(1, "DATA PROCESSING")
    if not run_command(f'"{python_exe}" main.py', "Data processing"):
        sys.exit(1)

    # Step 2: Model Training and Selection (R)
    print_step(2, "MODEL TRAINING AND SELECTION (R)")
    if not run_command(f'"{R_PATH}" "Training Layer/compare_models.R"', "R model training"):
        sys.exit(1)

    # Step 3: Verify outputs
    print_step(3, "VERIFICATION")

    required_files = [
        "OUT/processed_data.csv",
        "OUT/CorrelationHeatmap.png",
        "OUT/FeatureImportance.png",
        "OUT/models/best_model_R.rds",
        "OUT/model_comparison_results_R.json"
    ]

    all_exist = True
    for file in required_files:
        file_path = BASE_DIR / file
        if file_path.exists():
            print(f"✓ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False

    if not all_exist:
        print("\n❌ Pipeline incomplete - some files are missing")
        sys.exit(1)

    # Step 4: Summary
    print_step(4, "PIPELINE COMPLETE")
    print("✓ Data processed successfully")
    print("✓ Model trained and saved (R XGBoost)")
    print("✓ Visualizations generated")
    print("✓ Model comparison results saved")

    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Start the API:")
    print('   python "Presentation Layer/api.py"')
    print("\n2. Open your browser:")
    print("   http://localhost:8000")
    print("\n3. Upload a CSV file to get predictions!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
