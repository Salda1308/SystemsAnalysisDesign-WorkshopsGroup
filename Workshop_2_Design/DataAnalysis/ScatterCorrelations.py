import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


df = pd.read_csv("data_training.csv")

#  Map categorical variables 
mapping_tone = {'funny': 2, 'emotional': 1, 'serious': 0}
mapping_weather = {'sunny': 2, 'cloudy': 1, 'rainy': 0}
mapping_coffee = {'high': 2, 'medium': 1, 'low': 0}

if 'Tone_of_Ad' in df.columns:
    df['Tone_of_Ad'] = df['Tone_of_Ad'].map(mapping_tone)
if 'Weather' in df.columns:
    df['Weather'] = df['Weather'].map(mapping_weather)
if 'Coffee_Consumption' in df.columns:
    df['Coffee_Consumption'] = df['Coffee_Consumption'].map(mapping_coffee)

#  Define numerical columns 
target = 'sales'
exclude = {'Id', 'id', target}

num_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c not in exclude]

#  Calculate correlations 
correlations = df[num_cols + [target]].corr()[target].drop(target)
correlations = correlations.sort_values(ascending=False)

#  Configure subplots 
n_cols = 4
n_rows = math.ceil(len(num_cols) / n_cols)
fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))

# Plot each variable vs sales 
for i, col in enumerate(correlations.index):
    ax = axes.flat[i]
    x = df[col]
    y = df[target]
    ax.scatter(x, y, s=15, alpha=0.7)
    coef = np.polyfit(x, y, 1)
    fit = np.poly1d(coef)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, fit(x_line), color='red', linewidth=1)
    ax.set_title(f"{col} (r={correlations[col]:.2f})", fontsize=9)
    ax.set_xlabel(col)
    ax.set_ylabel(target)

# Hide empty subplots if there are more spaces than variables
for j in range(i + 1, n_rows * n_cols):
    fig.delaxes(axes.flat[j])

plt.tight_layout()
plt.savefig("ScatterCorrelations.png", dpi=300)
plt.close()
