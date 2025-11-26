import sys
import os
import importlib.util
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# --- 1. PATH CONFIGURATION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# We calculate the root assuming structure: Root -> Workshop_4 -> Simulation2 -> script
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

print(f"--- DIAGNOSIS ---")
print(f"Project root: {project_root}")

# --- 2. CLASS IMPORTATION ---
def import_class_from_file(module_name, class_name, search_root):
    # Search for the .py file recursively
    file_path = None
    for root, dirs, files in os.walk(search_root):
        if f"{module_name}.py" in files:
            file_path = os.path.join(root, f"{module_name}.py")
            break

    if not file_path:
        print(f" CRITICAL ERROR: Cannot find {module_name}.py in any subfolder.")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)

try:
    DataIngestionModule = import_class_from_file("DataIngestionModule", "DataIngestionModule", project_root)
    PreprocessingTransformationModule = import_class_from_file("PreprocessingTransformationModule", "PreprocessingTransformationModule", project_root)
    print("✓ Modules found and imported correctly.")
except Exception as e:
    print(f" Error importing classes: {e}")
    sys.exit(1)

# --- 3. DATA SEARCH ---
def find_data_file(filename, search_root):
    print(f"Searching for '{filename}' throughout the project...")
    for root, dirs, files in os.walk(search_root):
        if filename in files:
            found_path = os.path.join(root, filename)
            print(f"✓ File found at: {found_path}")
            return found_path
    return None

csv_path = find_data_file("data_training.csv", project_root)

# --- 4. CHAOS SIMULATION ---
def run_chaos_simulation():
    print("\n>>> Starting Chaos Simulation (Scenario 1)")

    if not csv_path:
        print(" FATAL ERROR: 'data_training.csv' not found in any folder.")
        print("   Please make sure the file exists within the TODOANAL folder.")
        return

    # Load Data
    try:
        ingestor = DataIngestionModule(csv_path)
        df = ingestor.load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    if df is None: return

    # Clean Data
    try:
        preprocessor = PreprocessingTransformationModule(df)
        df_clean = preprocessor.transform_categorical_to_numerical()
    except Exception as e:
        print(f"Error preprocessing: {e}")
        return
    
    # Validate columns
    if 'Web_GRP' not in df_clean.columns or 'sales' not in df_clean.columns:
        print(f" Missing necessary columns. Available: {df_clean.columns.tolist()}")
        return

    # Experiment
    results = []
    noise_levels = [0.0, 0.1, 0.2, 0.3, 0.5]
    base_correlation = df_clean['Web_GRP'].corr(df_clean['sales'])

    print(f"   > Base correlation (Web_GRP vs Sales): {base_correlation:.4f}")

    for noise in noise_levels:
        temp_df = df_clean.copy()
        sigma = temp_df['Web_GRP'].std() * noise
        noise_vector = np.random.normal(0, sigma, len(temp_df))
        temp_df['Web_GRP'] += noise_vector

        new_corr = temp_df['Web_GRP'].corr(temp_df['sales'])
        deviation = abs(base_correlation - new_corr)
        results.append(deviation)
        print(f"   > Noise: {int(noise*100)}% -> Deviation: {deviation:.4f}")

    # Graph
    try:
        plt.figure(figsize=(10,6))
        plt.plot(noise_levels, results, marker='o', color='red', linestyle='--')
        plt.title("Chaos Sensitivity: Impact of Noise on Web_GRP")
        plt.xlabel("Noise Level")
        plt.ylabel("Deviation in Correlation")
        plt.grid(True)

        output_path = os.path.join(current_dir, "chaos_plot.png")
        plt.savefig(output_path)
        print(f"\n SUCCESS: Graph saved at: {output_path}")
    except Exception as e:
        print(f"Error saving graph: {e}")

if __name__ == "__main__":
    run_chaos_simulation()
    