import traceback
import pandas as pd
import sqlite3 as sql
from sklearn.impute import SimpleImputer
import main as lg


def extract_data():
    try:
        df = pd.read_csv("international_sales_data.csv")
        lg.log("Data extracted successfully.", "info")
        
        c_df = df.copy()
        lg.log("Created a copy of the dataframe.", "info")
        
        lg.log(f"Extracted {len(c_df):,} rows and {len(df.columns)} columns.", "info")
        return c_df
    
    except Exception as e:
        lg.log(f"Error extracting data: {e}", "error")
        return None


class FillingMissingValues:
    
    def numerical_imputation(self, c_df):
        numerical_cols = ["PCS", "RATE", "GROSS AMT"]
        for col in numerical_cols:
            c_df[col] = pd.to_numeric(c_df[col], errors='coerce')
        if c_df[numerical_cols].isnull().values.any():
            imputer = SimpleImputer(strategy='median')
            c_df[numerical_cols] = imputer.fit_transform(c_df[numerical_cols])
            lg.log(f"Numerical columns imputed: {numerical_cols}", "info")
        return c_df

    def categorical_imputation(self, c_df):
        categorical_cols = ["Months", "CUSTOMER", "Style", "SKU", "Size"]
        if c_df[categorical_cols].isnull().values.any():
            imputer = SimpleImputer(strategy='most_frequent')
            c_df[categorical_cols] = imputer.fit_transform(c_df[categorical_cols])
            lg.log(f"Categorical columns imputed: {categorical_cols}", "info")
        return c_df

    def date_imputation(self, c_df):
        if 'DATE' in c_df.columns:
            c_df['DATE'] = pd.to_datetime(c_df['DATE'], format='%d-%m-%Y', errors='coerce')
            c_df = c_df.sort_values('DATE').reset_index(drop=True)
            timestamps = pd.to_numeric(c_df['DATE'], errors='coerce')
        
            interpolated_timestamps = timestamps.interpolate(method='linear', limit_direction='both')
        
            c_df['DATE'] = pd.to_datetime(interpolated_timestamps)
            lg.log("Date column imputed successfully via linear time interpolation.", "info")
            return c_df


miss = FillingMissingValues()
def transform_data(c_df):
    lg.log("Starting data transformation.", "info")
    try:
        initial_rows = len(c_df)
        c_df = c_df.drop_duplicates()
        lg.log(f"Removed {initial_rows - len(c_df)} duplicate rows.", "info")
        
        c_df = miss.numerical_imputation(c_df)
        c_df = miss.categorical_imputation(c_df)
        c_df = miss.date_imputation(c_df)
        
        c_df = c_df.rename(columns={"GROSS AMT": "GROSS_AMT"})
        
        lg.log(f"Data transformation complete. {len(c_df):,} records ready.", "info")
        return c_df

    except Exception as e:
        lg.log(f"Error during data transformation: {e}", "error")
        return None


def load_data(c_df, sales_db="sales_data.db"):
    lg.log(f"Connecting to database: {sales_db}", "info")
    try:
        conn = sql.connect(sales_db)
        with open ('schema.sql', 'r') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        lg.log("Db schema initialized to schema.sql", "info")

        column_mapping = {
            "index": "id",
            "DATE": "sales_date",
            "Months": "months",
            "CUSTOMER": "customer_name",
            "Style": "style_type",
            "SKU": "sku_code",
            "Size": "product_size",
            "PCS": "pcs_quantity",
            "RATE": "unit_rate",
            "GROSS_AMT": "gross_amt"
        }

        c_df_mapped = c_df.rename(columns=column_mapping)
        c_df_mapped.to_sql("sales", conn, if_exists='append', index=False)
        lg.log(f"Successfully loaded {len(c_df):,} records into clean schema.", "info")
        
        conn.commit()

    except Exception as e:
        lg.log(f"Error loading data: {e}", "error")
        print(traceback.format_exc())
    finally:
        conn.close()

if __name__ == "__main__":
    raw_df = extract_data()
    if raw_df is not None:
        clean_df = transform_data(raw_df)
        if clean_df is not None:
            load_data(clean_df)