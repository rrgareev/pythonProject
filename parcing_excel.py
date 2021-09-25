import datetime

import numpy as np
import pandas as pd
import numpy as np
import psycopg2

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)

def get_data_value(df, param_row_list, param_col_list):
    param_list = []
    note_id_list = []
    id_count = 1
    for param_col in param_col_list:
        param_temp = []
        note_id_temp = []
        for param_row in param_row_list:
            if not pd.isna(df.iloc[param_row][param_col]):
                param_temp.append(df.iloc[param_row][param_col])
                note_id_temp.append(id_count)
        param_list.append(param_temp)
        note_id_list.append(note_id_temp)
        id_count += 1

    return param_list, note_id_list


def parce_excel(file):
    df = pd.read_excel(file, index_col=None, header=None)

    df_num_row = df.shape[0]
    df_num_cols = df.shape[1]
    notes_columns = 8
    # isin location
    isin_row = 0
    isin_col_start = 2
    isin_row_list = np.arange(isin_row, isin_row+1, 1)
    isin_col_list = np.arange(isin_col_start, df_num_cols+isin_col_start, notes_columns).tolist()
    # notional location
    notional_row = 1
    notional_row_list = np.arange(notional_row, notional_row+1, 1)
    notional_col_start = 2
    notional_col_list = np.arange(notional_col_start, df_num_cols+notional_col_start, notes_columns).tolist()
    # coupon location
    coupon_row = 1
    coupon_row_list = np.arange(coupon_row, coupon_row+1, 1)
    coupon_col_start = 5
    coupon_col_list = np.arange(coupon_col_start, df_num_cols+coupon_col_start, notes_columns).tolist()
    # fix_date location
    fix_date_row = 4
    fix_date_row_end = 41
    fix_date_row_list = np.arange(fix_date_row, fix_date_row_end, 1)
    fix_date_col_start = 2
    fix_date_col_list = np.arange(fix_date_col_start, df_num_cols+fix_date_col_start, notes_columns).tolist()
    # coupon_trigger location
    coupon_trigger_row = 80
    coupon_trigger_row_end = 117
    coupon_trigger_row_list = np.arange(coupon_trigger_row, coupon_trigger_row_end, 1)
    coupon_trigger_col_start = 4
    coupon_trigger_col_list = np.arange(coupon_trigger_col_start, df_num_cols+coupon_trigger_col_start, notes_columns).tolist()
    # note currency location
    currency_row = 1
    currency_row_list = np.arange(currency_row, currency_row + 1, 1)
    currency_col_start = 3
    currency_col_list = np.arange(currency_col_start, df_num_cols +  currency_col_start, notes_columns).tolist()

    # Get values for all available notes
    note_id_values, note_id = get_data_value(df, isin_row_list, isin_col_list)
    #getting issue date and isin
    isin_values = []
    issue_date_values = []
    for value in note_id_values:
        issue_date_str = '20' + value[0].split('_')[0][0:2] + '-' + value[0].split('_')[0][2:4] + '-' + value[0].split('_')[0][4:6]
        issue_date = datetime.datetime.strptime(issue_date_str, "%Y-%m-%d").date()
        issue_date_values.append([issue_date])
        isin_values.append([value[0].split('_')[1]])

    notional_values, note_id = get_data_value(df, notional_row_list, notional_col_list)
    coupon_values, note_id = get_data_value(df, coupon_row_list, notional_col_list)
    fix_date_values, fix_date_note_id = get_data_value(df, fix_date_row_list, fix_date_col_list)
    coupon_trigger_values, note_id = get_data_value(df, coupon_trigger_row_list, coupon_trigger_col_list)
    currency_values, note_id = get_data_value(df, currency_row_list, currency_col_list)

    return isin_values, issue_date_values, notional_values, currency_values, fix_date_values, coupon_trigger_values, coupon_values, fix_date_note_id
