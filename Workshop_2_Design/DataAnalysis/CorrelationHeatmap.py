import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import f_regression
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv("data_training.csv")

# Remove ID columns if they exist
df = df.drop(columns=[c for c in df.columns if c.lower() == "id"], errors="ignore")

# Encode categorical variables as numerical
categorical_cols = ['Tone_of_Ad', 'Weather', 'Coffee_Consumption']
for col in categorical_cols:
    if col in df.columns:
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))

#  Pearson Correlation 
corr = df.corr(numeric_only=True)


#  Correlation Heatmap 
fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(corr, cmap='coolwarm', interpolation='nearest', aspect='auto')

# Axes
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.index)))
ax.set_xticklabels(corr.columns, rotation=90, fontsize=9)
ax.set_yticklabels(corr.index, fontsize=9)

# Show numerical values
for i in range(len(corr.columns)):
    for j in range(len(corr.index)):
        text = ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                       ha="center", va="center", color="black", fontsize=8)

plt.title("Correlation Heatmap (Numerical Features)", fontsize=14)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig("CorrelationHeatmap.png", dpi=200)
plt.close()
