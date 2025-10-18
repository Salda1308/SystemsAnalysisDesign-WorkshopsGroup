import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("data_training.csv")

#  Remove ID or target columns 
df = df.drop(columns=[c for c in df.columns if c.lower() in ['id', 'sales']], errors='ignore')

#  Encode categoricals 
categorical_cols = ['Tone_of_Ad', 'Weather', 'Coffee_Consumption']
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype('category').cat.codes

#  Select only numerical variables 
num_df = df.select_dtypes(include=[np.number])
cols = num_df.columns.tolist()

#  Create 6x4 figure 
rows, cols_per_row = 6, 4
fig, axes = plt.subplots(rows, cols_per_row, figsize=(18, 12))
axes = axes.flatten()

#  Generate individual boxplots 
for i, col in enumerate(cols[:rows*cols_per_row]):  # maximum 24 variables
    ax = axes[i]
    ax.boxplot(num_df[col].dropna(), patch_artist=True,
               boxprops=dict(facecolor='lightcoral'),
               medianprops=dict(color='black'))
    ax.set_title(col, fontsize=9)
    ax.tick_params(axis='x', bottom=False, labelbottom=False)
    ax.tick_params(axis='y', labelsize=8)

#  Turn off empty axes if there are extras 
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

plt.suptitle("Boxplots of All Numerical Features (Original Scale)", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("Boxplots.png", dpi=200)
plt.close()

