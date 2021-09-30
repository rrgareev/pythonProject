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
    # number of notes from excel to parce
    num_of_notes = 8

    # getting notes params from excel
    isin_values, issue_date_values, notional_values, note_id, currency_values, coupon_values, coupon_uncon_values, reoffer_values, coupon_obs_date_values, \
    funding_fix_date_values, funding_acc_start_date_values, funding_acc_end_date_values, funding_pay_date_values, coupon_paydate_values, coupon_accrual_start_date_values, \
    coupon_accrual_end_date_values, coupon_trigger_values, autocall_trigger_values, equity_name_values, equity_initial_levels_values, coupon_paydate_id, equity_id, \
    fund_date_note_id = parce_excel(notes_excel_file_name)

    #connect to database
    conn = connect_to_database()

    #insert into note_params
    table_name = 'note_params'
    columns = ['ISIN', 'Notional', 'IssueDate', 'Currency', 'Reoffer']
    values = [isin_values, notional_values, issue_date_values, currency_values, reoffer_values]
    num_of_inserted_rows = insert_data(conn, table_name, columns, values, num_of_notes)
    print(num_of_inserted_rows, "Records inserted successfully into " + table_name)

    #insert into observation dates
    table_name = 'coupon_observation_dates'
    columns = ['CouponObservationDate', 'Coupon_TriggerLevel', 'Note_id', 'Accrual_Start', 'Accrual_End']
    values = [coupon_obs_date_values, coupon_trigger_values, note_id, coupon_accrual_start_date_values, coupon_accrual_end_date_values]
    num_of_inserted_rows = insert_data(conn, table_name, columns, values, num_of_notes)
    print(num_of_inserted_rows, "Records inserted successfully into " + table_name)

    #insert into coupon coupon_dates
    table_name = 'coupon_dates'
    columns = ['CouponObservationDate_id', 'CouponDates', 'Coupon_RatePerAnnum', 'Coupon_GuaranteedPerAnnum']
    for note_num in range(num_of_notes):
        for i in range(len(coupon_paydate_values[note_num])-1):
            if len(coupon_values[note_num]) == 0:
                coupon_values[note_num].append(0)
            if len(coupon_uncon_values[note_num]) == 0:
                coupon_uncon_values[note_num].append(0)
            coupon_values[note_num].append(coupon_values[note_num][0])
            coupon_uncon_values[note_num].append(coupon_uncon_values[note_num][0])

    values = [coupon_paydate_id, coupon_paydate_values, coupon_values, coupon_uncon_values]
    num_of_inserted_rows = insert_data(conn, table_name, columns, values, num_of_notes)
    print(num_of_inserted_rows, "Records inserted successfully into " + table_name)

    #insert into autocall_trigger_levels
    table_name = 'autocall_trigger_levels'
    columns = ['Autocall_TriggerLevel', 'CouponObservationDate_id']
    values = [autocall_trigger_values, coupon_paydate_id]
    num_of_inserted_rows = insert_data(conn, table_name, columns, values, num_of_notes)
    print(num_of_inserted_rows, "Records inserted successfully into " + table_name)

    # insert into equity
    table_name = 'equities'
    columns = ['Note_id', 'EquityName', 'EquityInitialLevels']
    values = [equity_id, equity_name_values, equity_initial_levels_values]
    num_of_inserted_rows = insert_data(conn, table_name, columns, values, num_of_notes)
    print(num_of_inserted_rows, "Records inserted successfully into " + table_name)

    # insert into funding
    table_name = 'funding'
    columns = ['Note_id', 'FundFixDate', 'FundAccrualStart', 'FundAccrualEnd', 'FundPayDate']
    values = [fund_date_note_id, funding_fix_date_values, funding_acc_start_date_values, funding_acc_end_date_values, funding_pay_date_values]
    num_of_inserted_rows = insert_data(conn, table_name, columns, values, num_of_notes)
    print(num_of_inserted_rows, "Records inserted successfully into " + table_name)

    # close connection
    if conn:
        conn.close()
        print("PostgreSQL connection for notes database is closed")

if __name__ == '__main__':
    main()