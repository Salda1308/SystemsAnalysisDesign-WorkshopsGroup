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

    # Experiment: RandomForest sensitivity to noise on ALL numeric features
    noise_levels = [0.0, 0.1, 0.2, 0.3, 0.5]
    print("   > Training RandomForest to predict 'sales' (baseline and noisy variants for all features)")

    # Identify numeric features (exclude target)
    candidate_features = [c for c in df_clean.columns if c != 'sales']
    numeric_features = [c for c in candidate_features if pd.api.types.is_numeric_dtype(df_clean[c])]

    if not numeric_features:
        print(" No numeric features found to perturb. Ensure preprocessing converted categoricals to numeric.")
        return

    # Prepare base X and y
    try:
        X_base = df_clean.drop(columns=['sales'])
        y = df_clean['sales']
    except Exception as e:
        print(f"Error preparing features/target: {e}")
        return

    # Baseline MAE (no added noise)
    try:
        X_train, X_test, y_train, y_test = train_test_split(X_base, y, test_size=0.2, random_state=42)
        base_model = RandomForestRegressor(n_estimators=100, random_state=42)
        base_model.fit(X_train, y_train)
        y_pred = base_model.predict(X_test)
        base_mae = mean_absolute_error(y_test, y_pred)
        print(f"   > Baseline MAE (no noise): {base_mae:.4f}")
    except Exception as e:
        print(f"Error training baseline RandomForest: {e}")
        return

    # Run noise experiments per feature
    results_by_feature = {feat: [] for feat in numeric_features}

    for feat in numeric_features:
        print(f"\n   > Perturbing feature: {feat}")
        for noise in noise_levels:
            temp_df = df_clean.copy()
            sigma = temp_df[feat].std() * noise
            noise_vector = np.random.normal(0, sigma, len(temp_df)) if sigma > 0 else np.zeros(len(temp_df))
            temp_df[feat] = temp_df[feat] + noise_vector

            X_temp = temp_df.drop(columns=['sales'])
            y_temp = temp_df['sales']

            try:
                Xtr, Xte, ytr, yte = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)
                m = RandomForestRegressor(n_estimators=100, random_state=42)
                m.fit(Xtr, ytr)
                yp = m.predict(Xte)
                mae = mean_absolute_error(yte, yp)
                results_by_feature[feat].append(mae)
                deviation = mae - base_mae
                print(f"      Noise {int(noise*100)}% -> MAE: {mae:.4f} (Δ {deviation:.4f})")
            except Exception as e:
                print(f"      Error at noise {noise} for feature {feat}: {e}")
                results_by_feature[feat].append(np.nan)

    # Plot MAE vs Noise for each feature
    try:
        plt.figure(figsize=(12,8))
        for feat, maes in results_by_feature.items():
            plt.plot(noise_levels, maes, marker='o', linestyle='--', label=feat)
        plt.title("Chaos Sensitivity: Noise impact on RF MAE predicting Sales (by feature)")
        plt.xlabel("Noise Level")
        plt.ylabel("MAE")
        plt.grid(True)
        plt.legend(loc='best', fontsize='small')

        output_path = os.path.join(current_dir, "chaos_plot.png")
        plt.savefig(output_path, bbox_inches='tight')
        print(f"\n SUCCESS: Graph saved at: {output_path}")
    except Exception as e:
        print(f"Error saving graph: {e}")

if __name__ == "__main__":
    run_chaos_simulation()
    