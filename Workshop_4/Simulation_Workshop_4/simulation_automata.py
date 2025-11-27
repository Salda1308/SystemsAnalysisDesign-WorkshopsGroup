import sys
import os
import importlib.util
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..')) 

print(f"--- AUTOMATA DIAGNOSIS ---")
print(f"Project root: {project_root}")


def import_class_from_file(module_name, class_name, search_root):
    file_path = None
    for root, dirs, files in os.walk(search_root):
        if f"{module_name}.py" in files:
            file_path = os.path.join(root, f"{module_name}.py")
            break     
    if not file_path:
        print(f"ERROR: Cannot find {module_name}.py")
        sys.exit(1)  
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return getattr(module, class_name)

# Import your module to read real data
try:
    DataIngestionModule = import_class_from_file("DataIngestionModule", "DataIngestionModule", project_root)
except Exception as e:
    print(f"Error importing DataIngestionModule: {e}")
    sys.exit(1)

# We search for the CSV
def find_data_file(filename, search_root):
    for root, dirs, files in os.walk(search_root):
        if filename in files:
            return os.path.join(root, filename)
    return None

csv_path = find_data_file("data_training.csv", project_root)

# --- 3. CELLULAR AUTOMATA CLASS ---
class MarketAutomata:
    def __init__(self, real_data_path, grid_size=50):
        self.size = grid_size
        self.grid = np.zeros((grid_size, grid_size))
        
        # Load real data to initialize the simulation
        if real_data_path:
            ingestor = DataIngestionModule(real_data_path)
            df = ingestor.load_data()
            if df is not None and 'sales' in df.columns:
                # We use real statistics to seed the initial map
                # Initial sales probability based on normalized real mean
                sales_norm = (df['sales'] - df['sales'].min()) / (df['sales'].max() - df['sales'].min())
                avg_sales_prob = sales_norm.mean()

                print(f"   > Initializing network with real sales density: {avg_sales_prob:.2f}")
                # Seed the map randomly using that probability
                self.grid = np.random.choice([0.0, 0.5], size=(grid_size, grid_size), p=[1-avg_sales_prob, avg_sales_prob])
            else:
                self.grid = np.random.rand(grid_size, grid_size)
        else:
            self.grid = np.random.rand(grid_size, grid_size)

    def update(self):
        """Evolution Rule: Sales Diffusion (Word of Mouth)"""
        new_grid = self.grid.copy()

        for i in range(self.size):
            for j in range(self.size):
                # Get neighbors (3x3)
                i_min, i_max = max(0, i-1), min(self.size, i+2)
                j_min, j_max = max(0, j-1), min(self.size, j+2)
                neighbors = self.grid[i_min:i_max, j_min:j_max]

                avg_local = np.mean(neighbors)

                # RULE 1: Contagion (Viral Marketing)
                # If my neighbors buy a lot (avg > 0.3), I increase my purchases
                if avg_local > 0.3:
                    new_grid[i, j] += 0.05 * avg_local

                # RULE 2: Cooling (Market Saturation)
                # Sales naturally decrease over time if there is no stimulus
                new_grid[i, j] -= 0.01

                # RULE 3: Random Event (Sudden Advertising Campaign)
                # 0.1% probability that a cell shoots its sales to the maximum
                if np.random.random() < 0.001:
                    new_grid[i, j] = 1.0

        # Keep values between 0 and 1
        self.grid = np.clip(new_grid, 0, 1)
        return self.grid

# --- 4. EXECUTION ---
def run_automata_simulation():
    print("\n>>> Starting Event Simulation (Scenario 2 - Automata)")

    if not csv_path:
        print(" Warning: Could not find data_training.csv. Using random values.")

    # Initialize simulation
    automata = MarketAutomata(csv_path)

    # Execute 50 time steps
    steps = 50
    history = []
    print(f"   > Simulating {steps} time steps of market evolution...")

    for _ in range(steps):
        history.append(automata.update())

    # Generate Final Visualization (Heat Map)
    plt.figure(figsize=(10, 8))
    plt.imshow(history[-1], cmap='inferno', vmin=0, vmax=1)
    plt.colorbar(label='Sales Intensity (Normalized)')
    plt.title(f"Spatial Distribution of Sales (Step {steps})\nCellular Automata Dynamics")

    output_path = os.path.join(current_dir, "automata_heatmap.png")
    plt.savefig(output_path)
    print(f"\n SUCCESS: Heat map saved at: {output_path}")
    print("   (Include this image in your PDF report as evidence of Scenario 2)")

if __name__ == "__main__":
    run_automata_simulation()