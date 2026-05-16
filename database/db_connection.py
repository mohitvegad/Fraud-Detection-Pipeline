import mysql.connector
from logger import logger

def get_connection():
    try:
        conn = mysql.connector.connect(
         host="127.0.0.1",
         user="root",
         password="@Apple8422",
        database="xyz_company"
        )
        logger.info("MySQL connection established")
        return conn
    except Exception as e:
         print("❌ Connection failed:", e)
         raise 


