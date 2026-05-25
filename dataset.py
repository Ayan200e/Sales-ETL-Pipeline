import kagglehub as kh
import os 
import pandas as pd 
import main as lg

path = kh.dataset_download("thedevastator/unlock-profits-with-e-commerce-sales-data")
lg.log(f"Dataset downloaded to: {path}" , "info")

files = os.listdir(path)
lg.log(f"Files in the dataset: {[files]}" , "info")

csv_files = [file for file in files if file.endswith('.csv')]

if csv_files:
    try:
        df = pd.read_csv(os.path.join(path, csv_files[3]) , low_memory=False)
        lg.log(f"First few rows of the dataset:\n{df.head()}" , "info")
        lg.log(f"Information about the dataset:\n{df.info()}" , "info")
        lg.log(f"Description of the dataset:\n{df.describe()}" , "info")
        df.to_csv("international_sales_data.csv" , index=False)
        lg.log("Dataset saved as international_sales_data.csv" , "info")
    except Exception as e:
        lg.log(f"Error reading the CSV file: {e}" , "error")
else:
    lg.log("No CSV files found in the dataset." , "warning")
    print("Available files:", csv_files)