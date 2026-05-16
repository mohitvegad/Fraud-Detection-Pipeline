import pandas as pd
from database.db_connection import get_connection
from logger import logger

def extract_transactions():

    file_path="data/raw/bank_transactions.csv"

    try:
        # Read CSV
        data = pd.read_csv(file_path)

        # Check data (Empty)
        if data.empty:
            raise ValueError("No data found in CSV")
        
        # Logging
        logger.info("Extraction completed successfully")

        return data

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise

### DABASE EXTRACTION
def extract_database_employee():
    try:
        conn = get_connection()  # get connection from your connection file

        query = "SELECT * FROM employee"
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            raise ValueError("No data found in CSV")
        else:
            logger.info("Data extraction successful")
            print("Preview of extracted data:")
            print(df.head())

        return df

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise