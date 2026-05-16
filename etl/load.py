import sqlite3
import os
from logger import logger

def load_transactions(transformed_data):

    db_path="data/gold/bank_transactions_gold.db"
    csv_path="data/gold/bank_transactions_gold.csv"


    try:
        # Check data (Empty)
        if transformed_data.empty:
            return ValueError("No data found in Transform Data")

        conn = sqlite3.connect(db_path)

        # Save suspicious transactions to DB
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        transformed_data.to_sql(db_path, conn, if_exists="replace", index=False)
        transformed_data.to_csv(csv_path, index=False)
        logger.info(f"Load completed. Saved {len(transformed_data)} rows to {db_path}")
        conn.close()

    except Exception as e:
        logger.error(f"Load failed: {e}")
        raise


def load_employees(sql_data):

    db_path="data/gold/employee.db"
    
    try:
        # Check data (Empty)
        # if load_employees.empty:
        #     return ValueError("No data found in Transform Data")

        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)

        # Save suspicious transactions to DB
        sql_data.to_sql("alerts", conn, if_exists="replace", index=False)
        # logger.info(f"Load completed. Saved {len(load_employees)} rows to {db_path}")
        conn.close()

    except Exception as e:
        logger.error(f"Load failed: {e}")
        raise