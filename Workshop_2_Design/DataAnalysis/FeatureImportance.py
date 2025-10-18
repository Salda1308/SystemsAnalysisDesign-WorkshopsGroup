# feature_importance_anova_scaled.py
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np


train = pd.read_csv("data_training.csv")


formula = (
    'sales ~ Web_GRP + TV_GRP + Facebook_GRP + Tone_of_Ad + '
    'No_of_Web_Banners + Weather + Avg_Temperature + No_of_Rabbits + '
    'Network_Five_G + No_of_iPhone_14_Sold + No_of_Big_Cities + '
    'Health_Index + Sustainability_Index + Choc_Capital_Distance + '
    'No_of_Competitors + Import_Regulations + Time_in_Region + '
    'Percent_Internet_Access + Percent_Uni_Degrees + Percent_Unemployed + '
    'Gender + Coffee_Consumption + Avg_No_of_Cust_Complaints + Avg_Customer_Age'
)

modelo = ols(formula, data=train).fit()

# ANOVA 
anova_tabla = sm.stats.anova_lm(modelo, typ=2)
anova_tabla = anova_tabla.sort_values('PR(>F)')


# Top 15 most significant variables
top_anova = anova_tabla.head(15).iloc[::-1].copy()
top_anova['F_log'] = np.log10(top_anova['F'] + 1)  # Logarithmic scaling

# Graph
plt.figure(figsize=(9, 6))
bars = plt.barh(top_anova.index, top_anova['F_log'], color="#4C72B0")
plt.xlabel('log₁₀(F-statistic + 1)')
plt.title('Top Variables by ANOVA F-statistic (Log-Scaled)')
plt.tight_layout()

# Labels with the original F value
for bar, f_val in zip(bars, top_anova['F']):
    plt.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/4,
             f"{f_val:.1f}", fontsize=8, color='black')

plt.savefig("FeatureImportance.png", dpi=300)
plt.close()
