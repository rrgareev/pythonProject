import pandas as pd
import psycopg2
from parcing_excel import parce_excel
from insert_data_into_database import insert_data

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)

def connect_to_database():
    conn = psycopg2.connect(
        host="localhost",
        database="notes_database_pg",
        user="postgres",
        password="Bootstrap1")

    return conn

def insert_data_to_database(table_cols, values):
    pass

    return 0

def get_data_from_database():
    pass

    return 0

def main():
    notes_excel_file_name = "SN_database_2.xlsx"
    isin_values, notional_values, coupon_values, fix_date_values, currency_values = parce_excel(notes_excel_file_name)
    values = [isin_values, notional_values, fix_date_values, currency_values]

    conn = connect_to_database()

    #get_data_from_database()
    table_name = 'note_params'
    columns = ['ISIN', 'Notional', 'IssueDate', 'Currency']
    insert_data(conn, table_name, columns, values)
if __name__ == '__main__':
    main()