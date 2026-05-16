import pandas as pd
import os
from logger import logger

def transform_transactions(raw_data):

    save_path = "data/silver/bank_transactions_silver.csv"

    try:
        if raw_data.empty:
            raise ValueError("No data provided to transform!")

        # ---------------------------
        # 1. Remove duplicate transactions
        # ---------------------------
        df = raw_data.drop_duplicates(subset=['TransactionID'])

        # ---------------------------
        # 2. Fill missing values
        # ---------------------------

        numeric_columns = ['TransactionAmount', 'CustomerAge', 'AccountBalance', 'TransactionDuration', 'LoginAttempts']
        df[numeric_columns] = df[numeric_columns].fillna(0)

        categoty_columns = ['TransactionType', 'TransactionDate', 'Location', 'MerchantID', 'Channel', 'CustomerOccupation', ]
        df[categoty_columns] = df[categoty_columns].fillna('Unknown')

        # ---------------------------
        # 3. Convert data types
        # ---------------------------

        numeric_cols = ['AccountBalance', 'TransactionAmount']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        df[numeric_cols] = df[numeric_cols].fillna(0)

        date_cols = ['TransactionDate', 'PreviousTransactionDate']
        df[date_cols] = df[date_cols].apply(pd.to_datetime, errors='coerce')

        # ---------------------------
        # 3. Feature 
        # ---------------------------

        # High Amount Transactions
        df['high_amount_flag'] = df['TransactionAmount'] > 1000

        # Odd Time Transactions
        df['hour'] = df['TransactionDate'].dt.hour
        df['odd_hour_flag'] = (df['hour'] < 6) | (df['hour'] > 22)

        # Unusual Location (City Change)
        user_city = df.groupby('AccountID')['Location'].agg(lambda x: x.mode()[0]).reset_index()
        user_city.rename(columns={'Location': 'usual_city'}, inplace=True)

        df = df.merge(user_city, on='AccountID', how='left')
        df['location_flag'] = df['Location'] != df['usual_city']

        # New Device / IP
        user_device = df.groupby('AccountID')['DeviceID'].agg(lambda x: x.mode()[0]).reset_index()
        user_device.rename(columns={'DeviceID': 'usual_device'}, inplace=True)

        df = df.merge(user_device, on='AccountID', how='left')

        df['new_device_flag'] = df['DeviceID'] != df['usual_device']

        # High Frequenct Transaction
        tx_count = df.groupby('AccountID')['TransactionID'].count().reset_index()
        tx_count.rename(columns={'TransactionID': 'tx_count'}, inplace=True)

        df = df.merge(tx_count, on='AccountID', how='left')
        df['high_freq_flag'] = df['tx_count'] > 3

        #Final Score
        df['fraud_score'] = (
            df['high_amount_flag'].astype(int) +
            df['odd_hour_flag'].astype(int) +
            df['location_flag'].astype(int) +
            df['new_device_flag'].astype(int) +
            df['high_freq_flag'].astype(int) 
            )
        
        #Final Suspicious Flag
        df['is_suspicious'] = df['fraud_score'] >= 2

        df['Location']
        # 5. Save to silver layer
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
        logger.info(f"Transformation completed successfully. Saved to {save_path}")
        return df

    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        raise





























def transform_database_employee(sql_data):
    save_path = "data/silver/employee.csv"

    try:
        # if sql_data.empty:
        #     raise ValueError("No data provided to transform!")

        df = sql_data.drop_duplicates()
        df['salary'] = pd.to_numeric(df['salary'], errors='coerce').fillna(0)

        df_agg = df.groupby('name', as_index=False)['salary'].sum()
        df_agg.rename(columns={'salary': 'TotalSalary'}, inplace=True)

        df_agg['Department'] = 'Finance'
        df_agg['Bonus'] = df_agg['TotalSalary'] * 0.20
        df_agg['TotalSalaryWithBonus'] = df_agg['TotalSalary'] + df_agg['Bonus']

        df_sorted = df_agg.sort_values(by='TotalSalary', ascending=True)
        print(df_sorted)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df_sorted.to_csv(save_path, index=False)
        logger.info(f"Transformation completed successfully. Saved to {save_path}")

        return df_sorted

    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        raise