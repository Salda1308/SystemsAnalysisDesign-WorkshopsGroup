#!/usr/bin/env python3
"""
Setup script for Chocolate Sales Prediction project
Creates virtual environment and installs dependencies
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(cmd, description):
    """Run command and return success"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Setup the project environment"""

    print("="*60)
    print("CHOCOLATE SALES PREDICTION - ENVIRONMENT SETUP")
    print("="*60)

    base_dir = Path(__file__).parent

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)

    print(f"✅ Python {sys.version.split()[0]} detected")

    # Create virtual environment with Python 3.11
    env_name = "venv"

    # Try to create environment with Python 3.11
    if platform.system() == "Windows":
        create_cmd = f"py -3.11 -m venv {env_name}"
    else:
        create_cmd = f"python3.11 -m venv {env_name}"

    if not run_command(create_cmd, "Creating virtual environment with Python 3.11"):
        print("⚠️ Python 3.11 not found, trying default Python...")
        if not run_command(f"python -m venv {env_name}", "Creating virtual environment"):
            sys.exit(1)

    # Install Python packages using the virtual environment's pip directly
    if platform.system() == "Windows":
        pip_path = os.path.join(env_name, "Scripts", "pip.exe")
        python_path = os.path.join(env_name, "Scripts", "python.exe")
    else:
        pip_path = os.path.join(env_name, "bin", "pip")
        python_path = os.path.join(env_name, "bin", "python")

    # Upgrade pip first
    run_command(f'"{python_path}" -m pip install --upgrade pip', "Upgrading pip")

    # Install requirements
    if not run_command(f'"{pip_path}" install -r requirements.txt', "Installing Python dependencies"):
        sys.exit(1)

    # Check for R
    r_available = False
    try:
        result = subprocess.run(["Rscript", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            r_available = True
            print("✅ R detected")
        else:
            print("⚠️ R not found - you'll need to install R manually")
    except FileNotFoundError:
        print("⚠️ R not found - you'll need to install R manually")

    # Install R packages if R is available
    if r_available:
        r_script = """
        packages <- c("caret", "randomForest", "xgboost", "jsonlite", "data.table")
        install.packages(packages, repos="https://cloud.r-project.org/")
        """
        with open("temp_r_install.R", "w") as f:
            f.write(r_script)

        if run_command("Rscript temp_r_install.R", "Installing R packages"):
            os.remove("temp_r_install.R")
        else:
            print("⚠️ R package installation failed - you may need to install manually")

    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print("To activate the environment:")
    if platform.system() == "Windows":
        print(f"  .\\{env_name}\\Scripts\\Activate.ps1  (PowerShell)")
        print(f"  {env_name}\\Scripts\\activate.bat  (CMD)")
    else:
        print(f"  source {env_name}/bin/activate")

    print("\nTo run the pipeline:")
    print(f"  {python_path} run_pipeline.py")

    print("\nTo start the web interface:")
    print(f'  {python_path} "Presentation Layer/api.py"')

    print("\nThen open: http://localhost:8000")
    print("="*60)

if __name__ == "__main__":
    main()