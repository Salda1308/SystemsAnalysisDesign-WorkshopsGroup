"""
Main file of the Chocolates project
This script coordinates the data flow between all POO modules
"""

import sys
import os

# Add current directory to path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'Data Processing Layer'))

from DataIngestionModule import DataIngestionModule
from PreprocessingTransformationModule import PreprocessingTransformationModule
from FeatureAnalysisModule import FeatureAnalysisModule


def main():
    """
    Main function that executes the entire data analysis pipeline
    """
    print("=" * 60)
    print("CHOCOLATES PROJECT - DATA ANALYSIS PIPELINE")
    print("=" * 60)
    
    try:
        # Step 1: Data ingestion
        print("\nSTEP 1: DATA INGESTION")
        print("-" * 30)
        
        data_ingestor = DataIngestionModule('IN/data_training.csv')
        df = data_ingestor.load_data()
        
        if df is None:
            print("X Error: Could not load data")
            return
        
        # Show head and size
        data_ingestor.show_head()
        data_ingestor.show_dataset_size()
        
        # Step 2: Preprocessing and transformation
        print("\nSTEP 2: PREPROCESSING AND TRANSFORMATION")
        print("-" * 45)
        
        preprocessor = PreprocessingTransformationModule(df)
        
        # Complete data analysis (missing values, columns, size, unique values, data types)
        print("\n2.1 Complete data analysis...")
        analysis_results = preprocessor.complete_data_analysis()
        
        # Transform categorical variables
        print("\n2.2 Transforming categorical variables...")
        processed_df = preprocessor.transform_categorical_to_numerical()
        
        if processed_df is not None:
            print("\nOK Transformation completed successfully")
            
            # Save modified CSV in OUT
            print("\n5. Saving modified CSV...")
            processed_df.to_csv('OUT/processed_data.csv', index=False)
            print("Modified CSV saved in OUT/processed_data.csv")
        else:
            print("X Error in preprocessing")
            return
        
        # Step 3: Feature analysis
        print("\nSTEP 3: FEATURE ANALYSIS")
        print("-" * 38)
        
        analyzer = FeatureAnalysisModule(processed_df)
        
        # Complete feature analysis
        print("\n3.1 Complete feature analysis...")
        feature_results = analyzer.complete_feature_analysis()
        
        # Step 4: Export results
        print("\nSTEP 4: EXPORT RESULTS")
        print("-" * 35)
        
        analyzer.export_analysis_results('OUT/feature_analysis_results.json')
        
        print("\nOK PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nFiles generated in OUT/:")
        print("- processed_data.csv (clean data)")
        print("- feature_analysis_results.json (analysis)")
        print("- CorrelationHeatmap.png")
        print("- FeatureImportance.png")
        print("- ScatterCorrelations.png")
        print("- Boxplots.png")
        
        return {
            'data_ingestor': data_ingestor,
            'preprocessor': preprocessor,
            'analyzer': analyzer,
            'raw_data': df,
            'processed_data': processed_df
        }
        
    except ImportError as e:
        print(f"X Import error: {e}")
        print("Check that all modules are in the same folder")
    except Exception as e:
        print(f"X Unexpected error: {e}")
        import traceback
        traceback.print_exc()


def demonstrate_module_usage():
    """
    Function to demonstrate individual use of each module
    """
    print("\n" + "=" * 50)
    print("DEMONSTRATION OF INDIVIDUAL MODULE USAGE")
    print("=" * 50)
    
    # Example of DataIngestionModule usage
    print("\n1) DataIngestionModule - Individual example:")
    try:
        data_ingestor = DataIngestionModule('IN/data_training.csv')
        df = data_ingestor.load_data()
        if df is not None:
            print(f"   OK Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
            data_ingestor.show_head(3)
            data_ingestor.show_dataset_size()
    except Exception as e:
        print(f"   X Error: {e}")
    
    # Example of PreprocessingTransformationModule usage
    print("\n2) PreprocessingTransformationModule - Individual example:")
    try:
        data_ingestor = DataIngestionModule('IN/data_training.csv')
        df = data_ingestor.load_data()
        
        if df is not None:
            preprocessor = PreprocessingTransformationModule(df)
            
            # Usar metodos individuales
            preprocessor.analyze_missing_values()
            preprocessor.analyze_columns()
            
            processed_df = preprocessor.transform_categorical_to_numerical()
            print(f"   OK Transformation completed: {processed_df.shape}")
    except Exception as e:
        print(f"   X Error: {e}")
    
    # Example of FeatureAnalysisModule usage
    print("\n3) FeatureAnalysisModule - Individual example:")
    try:
        data_ingestor = DataIngestionModule('IN/data_training.csv')
        df = data_ingestor.load_data()
        
        if df is not None:
            preprocessor = PreprocessingTransformationModule(df)
            processed_df = preprocessor.transform_categorical_to_numerical()
            
            if processed_df is not None:
                analyzer = FeatureAnalysisModule(processed_df)
                print("   OK Analysis module ready to use")
                print("   - Complete feature analysis available")
    except Exception as e:
        print(f"   X Error: {e}")


if __name__ == "__main__":
    # Ejecutar el pipeline principal
    results = main()
    
    print("\nChocolates project ready to use!")
    print("Pipeline executed successfully")