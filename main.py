from etl.extract import extract_transactions
from etl.extract import extract_database_employee

from etl.transform import transform_transactions
from etl.transform import transform_database_employee

from etl.load import load_transactions
from etl.load import load_employees


def run_etl():
    # Extract
    raw_data = extract_transactions()
    # sql_data = extract_database_employee()

    # Transform
    transformed_data = transform_transactions(raw_data)
    # transformed_data = transform_database_employee(sql_data)

    # Load
    load_transactions(transformed_data)
    # load_employees(transformed_data)


if __name__ == "__main__":
    run_etl()