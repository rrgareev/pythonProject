import numpy as np
import pandas as pd
import numpy as np
import psycopg2

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)

def get_data_value(df, param_row_list, param_col_list):
    param_list=[]
    for param_col in param_col_list:
        param_temp = []
        for param_row in param_row_list:
            param_temp.append(df.iloc[param_row][param_col])
        param_list.append(param_temp)

    return param_list


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
    funding_date_row = 41
    fix_date_row_list = np.arange(fix_date_row, funding_date_row, 1)
    fix_date_col_start = 2
    fix_date_col_list = np.arange(fix_date_col_start, df_num_cols+fix_date_col_start, notes_columns).tolist()
    # note currency location
    currency_row = 1
    currency_row_list = np.arange(currency_row, currency_row + 1, 1)
    currency_col_start = 3
    currency_col_list = np.arange(currency_col_start, df_num_cols +  currency_col_start, notes_columns).tolist()

    # Get values for all available notes
    isin_values = get_data_value(df, isin_row_list, isin_col_list)
    notional_values = get_data_value(df, notional_row_list, notional_col_list)
    coupon_values = get_data_value(df, coupon_row_list, notional_col_list)
    fix_date_values = get_data_value(df, fix_date_row_list, fix_date_col_list)
    currency_values = get_data_value(df, currency_row_list, currency_col_list)

    return isin_values, notional_values, coupon_values, fix_date_values, currency_values
