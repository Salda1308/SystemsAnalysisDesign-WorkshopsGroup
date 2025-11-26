import pandas as pd


class DataIngestionModule:
    """
    Module for data ingestion of the Chocolates project
    """
    
    def __init__(self, file_path):
        
        self.file_path = file_path
        self.df = None
    


    def load_data(self):
        
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"Data loaded successfully from {self.file_path}")
            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    


    def show_head(self, n=5):

        if self.df is not None:
            print(f"\n=== FIRST {n} ROWS ===")
            print(self.df.head(n))
        else:
            print("Error: No data loaded")
    


    def show_dataset_size(self):

        if self.df is not None:
            print(f"\n=== DATASET SIZE ===")
            print(f"Dimensions: {self.df.shape}")
            print(f"Rows: {self.df.shape[0]}")
            print(f"Columns: {self.df.shape[1]}")
        else:
            print("Error: No data loaded")
    


    def get_dataframe(self):
        
        return self.df



if __name__ == "__main__":
    
    data_ingestor = DataIngestionModule('data_training.csv')
    df = data_ingestor.load_data()
    
    
    data_ingestor.show_head()
    data_ingestor.show_dataset_size()
