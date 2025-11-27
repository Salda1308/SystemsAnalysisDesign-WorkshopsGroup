import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')


class FeatureAnalysisModule:
    
    
    def __init__(self, dataframe):
        
        self.df = dataframe.copy() if dataframe is not None else None
        self.analysis_results = {}
    



    def analyze_sales_distribution(self):

        if self.df is None or 'sales' not in self.df.columns:
            error_msg = "Error: No data or 'sales' column does not exist"
            print(error_msg)
            return {"error": error_msg}


        n_bins = math.ceil(len(self.df) ** (1/2))

        print(f"=== SALES DISTRIBUTION ANALYSIS ===")
        print(f"Calculated number of bins: {n_bins}")
        print(f"Sales range: {self.df['sales'].min():.2f} - {self.df['sales'].max():.2f}")


        counts, bins, patches = plt.hist(self.df['sales'], bins=n_bins, alpha=0.7, color='skyblue', edgecolor='black')

        plt.title("Sales Distribution", fontsize=14, fontweight='bold')
        plt.xlabel("Sales", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(True, alpha=0.3)


        mean_sales = self.df['sales'].mean()
        plt.axvline(mean_sales, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_sales:.2f}')
        plt.legend()

        plt.tight_layout()
        plt.show()


        hist_df = pd.DataFrame({
            "Range": [f"{bins[i]:.0f} - {bins[i+1]:.0f}" for i in range(len(bins) - 1)],
            "Frequency": counts.astype(int),
            "Percentage": (counts / len(self.df) * 100).round(2)
        })

        print("\nDistribution by ranges:")
        print(hist_df.to_string(index=False))
        
        
        sales_stats = {
            "mean": mean_sales,
            "median": self.df['sales'].median(),
            "std": self.df['sales'].std(),
            "min": self.df['sales'].min(),
            "max": self.df['sales'].max(),
            "skewness": self.df['sales'].skew(),
            "histogram_data": hist_df.to_dict('records')
        }
        
        self.analysis_results['sales_distribution'] = sales_stats
        
        return sales_stats
    





    def correlation_analysis_with_heatmap(self):

        if self.df is None:
            error_msg = "Error: No data available"
            print(error_msg)
            return {"error": error_msg}

        print(f"\n=== CORRELATION ANALYSIS ===")
        
        
        df_work = self.df.copy()
        df_work = df_work.drop(columns=[c for c in df_work.columns if c.lower() in ['id', 'Id']], errors='ignore')
        
        
        corr = df_work.select_dtypes(include=[np.number]).corr()
        
        
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
        plt.savefig("OUT/CorrelationHeatmap.png", dpi=200, bbox_inches='tight')
        plt.show()
        plt.close()


        corr_pairs = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                corr_value = corr.iloc[i, j]
                corr_pairs.append({
                    'Variable1': corr.columns[i],
                    'Variable2': corr.columns[j],
                    'Correlation': corr_value
                })


        corr_pairs.sort(key=lambda x: abs(x['Correlation']), reverse=True)

        print(f"\nTop 10 strongest correlations:")
        for i, pair in enumerate(corr_pairs[:10]):
            print(f"{i+1}. {pair['Variable1']} - {pair['Variable2']}: {pair['Correlation']:.3f}")
        
        self.analysis_results['correlation'] = {
            "matrix": corr.to_dict(),
            "top_correlations": corr_pairs[:10]
        }
        
        return corr
    





    def anova_feature_importance(self):

        if self.df is None:
            error_msg = "Error: No data available"
            print(error_msg)
            return {"error": error_msg}

        try:
            import statsmodels.api as sm
            from statsmodels.formula.api import ols
        except ImportError:
            print("Error: statsmodels not available. Install with: pip install statsmodels")
            return {"error": "statsmodels not available"}

        print(f"\n=== ANOVA ANALYSIS - FEATURE IMPORTANCE ===")
        
        
        df_work = self.df.copy()
        
        
        exclude_cols = {'sales', 'id', 'Id', 'ID'}
        numeric_cols = [c for c in df_work.select_dtypes(include=[np.number]).columns if c not in exclude_cols]
        
        formula = f"sales ~ {' + '.join(numeric_cols)}"
        
        # Fit model
        modelo = ols(formula, data=df_work).fit()

        # ANOVA
        anova_tabla = sm.stats.anova_lm(modelo, typ=2)
        anova_tabla = anova_tabla.sort_values('PR(>F)')

        # Top 15 most significant variables
        top_anova = anova_tabla.head(15).iloc[::-1].copy()
        top_anova['F_log'] = np.log10(top_anova['F'] + 1)  # Logarithmic scaling
        
        # Gráfico
        plt.figure(figsize=(9, 6))
        bars = plt.barh(top_anova.index, top_anova['F_log'], color="#4C72B0")
        plt.xlabel('log₁₀(F-statistic + 1)')
        plt.title('Top Variables by ANOVA F-statistic (Log-Scaled)')
        plt.tight_layout()
        
        # Labels con el valor F original
        for bar, f_val in zip(bars, top_anova['F']):
            plt.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/4,
                     f"{f_val:.1f}", fontsize=8, color='black')
        
        plt.savefig("OUT/FeatureImportance.png", dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()

        print(f"\nTop 15 most important variables:")
        print(top_anova[['F', 'PR(>F)']].round(4))
        
        self.analysis_results['anova'] = {
            "full_table": anova_tabla.to_dict(),
            "top_15": top_anova.to_dict()
        }
        
        return anova_tabla
    





    def scatter_correlations(self):

        if self.df is None:
            error_msg = "Error: No data available"
            print(error_msg)
            return {"error": error_msg}

        print(f"\n=== SCATTER PLOTS WITH TREND LINES ===")
        
        
        target = 'sales'
        df_work = self.df.copy()
        
        
        exclude = {'Id', 'id', 'sales'}
        num_cols = [c for c in df_work.select_dtypes(include=[np.number]).columns if c not in exclude]
        
        
        correlations = df_work[num_cols + [target]].corr()[target].drop(target)
        correlations = correlations.sort_values(ascending=False)
        
        
        n_cols = 4
        n_rows = math.ceil(len(num_cols) / n_cols)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
        
        
        for i, col in enumerate(correlations.index):
            ax = axes.flat[i] if n_rows > 1 else axes
            x = df_work[col]
            y = df_work[target]
            ax.scatter(x, y, s=15, alpha=0.7, color='skyblue')
            
            # Trend line
            coef = np.polyfit(x, y, 1)
            fit = np.poly1d(coef)
            x_line = np.linspace(x.min(), x.max(), 100)
            ax.plot(x_line, fit(x_line), color='red', linewidth=1)
            
            ax.set_title(f"{col} (r={correlations[col]:.2f})", fontsize=9)
            ax.set_xlabel(col)
            ax.set_ylabel(target)
            ax.grid(True, alpha=0.3)
        
        # Hide empty subplots if there are more spaces than variables
        for j in range(i + 1, n_rows * n_cols):
            axes.flat[j].axis('off') if n_rows > 1 else axes.axis('off')
        
        plt.tight_layout()
        plt.savefig("OUT/ScatterCorrelations.png", dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()

        print(f"\nCorrelations with 'sales' (sorted):")
        for i, (var, corr) in enumerate(correlations.items()):
            print(f"{i+1:2d}. {var:25s}: {corr:6.3f}")
        
        self.analysis_results['scatter_correlations'] = correlations.to_dict()
        
        return correlations
    




    def boxplots_analysis(self):

        if self.df is None:
            error_msg = "Error: No data available"
            print(error_msg)
            return {"error": error_msg}

        print(f"\n=== BOXPLOTS ANALYSIS ===")

        # Prepare data
        df_work = self.df.copy()

        # Remove ID or target columns
        df_work = df_work.drop(columns=[c for c in df_work.columns if c.lower() in ['id', 'sales']], errors='ignore')

        # Select only numerical variables
        num_df = df_work.select_dtypes(include=[np.number])
        cols = num_df.columns.tolist()

        # Create 6x4 figure
        rows, cols_per_row = 6, 4
        fig, axes = plt.subplots(rows, cols_per_row, figsize=(18, 12))
        axes = axes.flatten()

        # Generate individual boxplots
        for i, col in enumerate(cols[:rows*cols_per_row]):  # maximum 24 variables
            ax = axes[i]
            bp = ax.boxplot(num_df[col].dropna(), patch_artist=True,
                            boxprops=dict(facecolor='lightcoral'),
                            medianprops=dict(color='black'))
            ax.set_title(col, fontsize=9)
            ax.tick_params(axis='x', bottom=False, labelbottom=False)
            ax.tick_params(axis='y', labelsize=8)
            ax.grid(True, alpha=0.3)

        # Deactivate empty axes if there are extras
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')
        
        plt.suptitle("Boxplots of All Numerical Features (Original Scale)", fontsize=14)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig("OUT/Boxplots.png", dpi=200, bbox_inches='tight')
        plt.show()
        plt.close()

        # Descriptive statistics
        desc_stats = num_df.describe()
        print(f"\nDescriptive statistics of numerical variables:")
        print(desc_stats.round(2))
        
        self.analysis_results['boxplots'] = {
            "descriptive_stats": desc_stats.to_dict(),
            "variables_analyzed": cols
        }
        
        return desc_stats
    


    def complete_feature_analysis(self):

        if self.df is None:
            print("Error: No data available")
            return None

        print("=" * 70)
        print("COMPLETE FEATURE ANALYSIS - FEATURE ANALYSIS MODULE")
        print("=" * 70)

        try:
            # Sales distribution analysis
            print("\n1. SALES DISTRIBUTION ANALYSIS")
            sales_results = self.analyze_sales_distribution()

            # Correlation analysis
            print("\n2. CORRELATION ANALYSIS")
            correlation_results = self.correlation_analysis_with_heatmap()

            # ANOVA analysis
            print("\n3. ANOVA ANALYSIS")
            anova_results = self.anova_feature_importance()

            # Scatter plots
            print("\n4. SCATTER PLOTS")
            scatter_results = self.scatter_correlations()

            # Boxplots
            print("\n5. BOXPLOTS ANALYSIS")
            boxplot_results = self.boxplots_analysis()
            
            
            
            return {
                'sales_distribution': sales_results,
                'correlation': correlation_results,
                'anova': anova_results,
                'scatter_correlations': scatter_results,
                'boxplots': boxplot_results
            }
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    




    def get_analysis_summary(self):

        if not self.analysis_results:
            print("No analyses have been performed yet")
            return {"error": "No analyses available"}

        print(f"\n=== SUMMARY OF PERFORMED ANALYSES ===")
        for analysis_type, results in self.analysis_results.items():
            print(f"OK {analysis_type}: Completed")

        print("=" * 40)
        return self.analysis_results
    


    def export_analysis_results(self, filename="feature_analysis_results.json"):

        import json

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, indent=2, default=str)
            print(f"Results exported successfully to {filename}")
        except Exception as e:
            print(f"Error exporting results: {e}")


if __name__ == "__main__":
    
    print("-")