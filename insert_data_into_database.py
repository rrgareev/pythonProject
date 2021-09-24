import pandas as pd
import psycopg2

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)



def insert_data(conn, table_name, columns, values):
    column_str = str()
    values_str = ''
    column_len = len(columns)
    for i in range(column_len):
        if i < column_len-1:
            column_str = column_str + '"{}",'.format(columns[i])
            values_str = values_str + '%s' + ','
        else:
            column_str = column_str + '"{}"'.format(columns[i])
            values_str = values_str + '%s'
    #insert into note_params

    #query_insert = """insert into note_params ("{}","{}","{}","{}","{}") values (%s,%s,%s,%s,%s)""".format('IssueDate', 'Side', 'Notional', 'Currency', 'ISIN')

    query_insert = "insert into " + table_name + " (" + column_str + ") values " + "(" + values_str + ");"

    cursor = conn.cursor()
    for i in range(len(values[0])):
        records_to_insert = ()
        for col_value in values:
            records_to_insert = records_to_insert + (col_value[i][0],)
    #record_to_insert = ('23.09.2021', 'Sell', 'USD', 100000, 'XS132434')


        cursor.execute(query_insert, records_to_insert)
        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into notes table")

    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

    return 0