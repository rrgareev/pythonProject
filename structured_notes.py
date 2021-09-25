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
    isin_values, issue_date_values, notional_values, currency_values, fix_date_values, \
    coupon_trigger_values, coupon_values, fix_date_note_id = parce_excel(notes_excel_file_name)

    #connect to database
    conn = connect_to_database()

    #insert into note_params
    table_name = 'note_params'
    columns = ['ISIN', 'Notional', 'IssueDate', 'Currency']
    values = [isin_values, notional_values, issue_date_values, currency_values]
    insert_data(conn, table_name, columns, values, num_of_notes=5)

    #insert into observation dates
    table_name = 'coupon_observation_dates'
    columns = ['CouponObservationDate', 'Coupon_TriggerLevel', 'Note_id']
    values = [fix_date_values, coupon_trigger_values, fix_date_note_id]
    insert_data(conn, table_name, columns, values, num_of_notes=5)

    # close connection
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection for notes database is closed")

if __name__ == '__main__':
    main()