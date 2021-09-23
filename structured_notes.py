import pandas as pd
import psycopg2
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)

query_select = "select * from note_params fetch first 100 rows only"
query_insert = "insert into note_params values ('3', '2021-05-05', 'SELL', '1350000.89', 'EUR', '30/360', 'XS2340073787');"
cursor = conn.cursor()
cursor.execute(query_insert)
conn.commit()
#cursor.execute(query_select)
#data = cursor.fetchall()

#print(data)

def parse_notes_original_params(file_name):
    df = pd.read_excel(file_name)

    return df

def connect_to_database():
    conn = psycopg2.connect(
        host="localhost",
        database="notes_database_pg",
        user="postgres",
        password="Bootstrap1")

    return conn

def insert_data_to_database(table_cols, values):

    return 0

def get_data_from_database():

    return 0

def main():
    notes_excel_file_name = "SN_database_2.xlsx"
    conn = connect_to_database()
    get_data_from_database()
    insert_data_to_database()
    parse_notes_original_params(notes_excel_file_name)


if __name__ == '__main__':
    main()