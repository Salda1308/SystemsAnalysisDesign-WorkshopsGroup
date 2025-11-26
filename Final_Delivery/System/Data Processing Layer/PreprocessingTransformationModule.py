import pandas as pd


class PreprocessingTransformationModule:
    
    
    def __init__(self, dataframe):
        
        self.df = dataframe.copy() if dataframe is not None else None
        self.original_df = dataframe.copy() if dataframe is not None else None
    
    def analyze_missing_values(self):

        if self.df is None:
            print("Error: No data available")
            return None

        print("\n=== MISSING VALUES ANALYSIS ===")
        missing_values = self.df.isnull().sum()
        return missing_values
    


    def analyze_columns(self):

        if self.df is None:
            print("Error: No data available")
            return None

        print("\n=== COLUMNS ANALYSIS ===")
        analyze1 = self.df.info()
        analyze2 = self.df.describe()

        return {
            'info': analyze1,
            'describe': analyze2
        }
    

    
    
    def complete_data_analysis(self):

        if self.df is None:
            print("Error: No data available")
            return None

        print("=" * 60)
        print("ANALYSIS - PREPROCESSING MODULE")
        print("=" * 60)
        
        results = {}

        results['columns_analysis'] = self.analyze_columns()
        results['missing_values_analysis'] = self.analyze_missing_values()
        
        
        return results
    


    def transform_categorical_to_numerical(self):

        if self.df is None:
            print("Error: No data available")
            return None


        mappings = {
            'Tone_of_Ad': {'funny': 2, 'emotional': 1, 'serious': 0},
            'Weather': {'sunny': 2, 'cloudy': 1, 'rainy': 0},
            'Coffee_Consumption': {'high': 2, 'medium': 1, 'low': 0}
        }

        print("\n=== CATEGORICAL TO NUMERICAL TRANSFORMATION ===")
        
        transformations_applied = []
        
        for column, mapping in mappings.items():
            if column in self.df.columns:
                if self.df[column].dtype == 'object':
                    # Verificar que todos los valores tienen un mapping
                    missing_mappings = set(self.df[column].unique()) - set(mapping.keys())
                    if missing_mappings:
                        print(f"Warning: Values without mapping in {column}: {missing_mappings}")
                        # Use -1 for unmapped values
                        mapping_with_default = mapping.copy()
                        for val in missing_mappings:
                            mapping_with_default[val] = -1
                        self.df[column] = self.df[column].map(mapping_with_default)
                    else:
                        self.df[column] = self.df[column].map(mapping)

                    transformations_applied.append(f"{column}: {mapping}")
        
        print("Applied transformations:")
        for transformation in transformations_applied:
            print(f"  {transformation}")

        if not transformations_applied:
            print("No categorical transformations applied")
        
        return self.df
    


    def get_processed_dataframe(self):
       
        return self.df
    
    
    def reset_data(self):

        self.df = self.original_df.copy()
        print("DataFrame restored to its original state")
        return self.df



if __name__ == "__main__":
    print("-")
