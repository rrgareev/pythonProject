import pandas as pd
import psycopg2

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)

conn = psycopg2.connect(
    host="localhost",
    database="notes_database_pg",
    user="postgres",
    password="Bootstrap1")
#select
#query_select = "select * from note_params fetch first 100 rows only"
#query_select_columns = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'note_params'"
#query_select_tables = "SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema='public';"

#insert
query_insert = """insert into note_params ("{}","{}","{}","{}","{}") values (%s,%s,%s,%s,%s)""".format('IssueDate', 'Side', 'Notional', 'Currency', 'ISIN')
record_to_insert = ('23.09.2021', 'Sell', 100000, 'USD', 'XS132434')
#query_insert = "insert into note_params values (1, '2021-05-05', 'SELL', '1350000.89', 'EUR', '30/360', 'XS2340073787');"

#update
query_update ="""update note_params set "{}"=123 where "{}"=2""".format('Notional', 'id')

cursor = conn.cursor()

cursor.execute(query_update)
conn.commit()
count = cursor.rowcount
#cursor.execute(query_select)
#data = cursor.fetchall()
conn.close()
print(data)