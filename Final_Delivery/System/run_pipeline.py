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
if platform.system() == "Windows":
    R_PATH = r"C:\Program Files\R\R-4.5.2\bin\Rscript.exe"
else:
    R_PATH = "Rscript"

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
        print(f"[ERROR] {description} failed")
        print(result.stderr)
        return False

    print(f"[OK] {description} completed successfully")
    if result.stdout:
        print(result.stdout)
    return True

def main():
    """Execute the complete pipeline"""

    print("\n" + "="*70)
    print("CHOCOLATE SALES PREDICTION - COMPLETE PIPELINE")
    print("3-Layer Architecture: Python -> R -> Python API")
    print("="*70)

    # Step 1: Data Processing (Python)
    print_step(1, "DATA PROCESSING")
    if not run_command('python "Training Layer/main.py"', "Data processing"):
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
            print(f"[OK] {file} exists")
        else:
            print(f"[ERROR] {file} missing")
            all_exist = False

    if not all_exist:
        print("\n[ERROR] Pipeline incomplete - some files are missing")
        sys.exit(1)

    # Step 4: Summary
    print_step(4, "PIPELINE COMPLETE")
    print("[OK] Data processed successfully")
    print("[OK] Model trained and saved (R Stacking Ensemble)")
    print("[OK] Visualizations generated")
    print("[OK] Model comparison results saved")

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
