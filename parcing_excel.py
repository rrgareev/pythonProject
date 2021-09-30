import datetime

import numpy as np
import pandas as pd
import numpy as np
import psycopg2

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 2000)

def get_data_value(df, param_row_list, param_col_list, is_id):
    param_list = []
    id_list = []
    id_count = 1
    for param_col in param_col_list:
        param_temp = []
        id_temp = []
        for param_row in param_row_list:
            if not pd.isna(df.iloc[param_row][param_col]):
                param_temp.append(df.iloc[param_row][param_col])
                if is_id:
                    id_temp.append(id_count)

        param_list.append(param_temp)
        if is_id:
            id_list.append(id_temp)
            id_count += 1

    if is_id:
        return param_list, id_list
    else:
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
    # note currency location
    currency_row = 1
    currency_row_list = np.arange(currency_row, currency_row + 1, 1)
    currency_col_start = 3
    currency_col_list = np.arange(currency_col_start, df_num_cols + currency_col_start, notes_columns).tolist()
    # coupon conditional location
    coupon_row = 1
    coupon_row_list = np.arange(coupon_row, coupon_row+1, 1)
    coupon_col_start = 5
    coupon_col_list = np.arange(coupon_col_start, df_num_cols+coupon_col_start, notes_columns).tolist()
    # coupon unconditional location
    coupon_uncond_row = 2
    coupon_uncond_row_list = np.arange(coupon_uncond_row, coupon_uncond_row + 1, 1)
    coupon_uncond_col_start = 5
    coupon_uncond_col_list = np.arange(coupon_uncond_col_start, df_num_cols + coupon_uncond_col_start, notes_columns).tolist()
    # reoffer location
    reoffer_row = 2
    reoffer_row_list = np.arange(reoffer_row, reoffer_row + 1, 1)
    reoffer_col_start = 2
    reoffer_col_list = np.arange(reoffer_col_start, df_num_cols + reoffer_col_start, notes_columns).tolist()
    # fix_date location (coupon observation dates)
    coupon_obs_date_row = 4
    coupon_obs_date_row_end = 41
    coupon_obs_date_row_list = np.arange(coupon_obs_date_row, coupon_obs_date_row_end, 1)
    coupon_obs_date_col_start = 2
    coupon_obs_date_col_list = np.arange(coupon_obs_date_col_start, df_num_cols+coupon_obs_date_col_start, notes_columns).tolist()
    # accrual start/accrual end / paydate
    accrual_start_date_row = 4
    accrual_start_date_row_end = 41
    accrual_start_date_row_list = np.arange(accrual_start_date_row, accrual_start_date_row_end, 1)
    accrual_end_date_row_list = accrual_start_date_row_list
    coupon_paydate_row_list = accrual_start_date_row_list
    accrual_start_date_col_start = 3
    accrual_end_date_col_start = 4
    paydate_col_start = 5
    accrual_start_date_col_list = np.arange(accrual_start_date_col_start, df_num_cols + accrual_start_date_col_start, notes_columns).tolist()
    accrual_end_date_col_list = np.arange(accrual_end_date_col_start, df_num_cols + accrual_end_date_col_start, notes_columns).tolist()
    coupon_paydate_col_list = np.arange(paydate_col_start, df_num_cols + paydate_col_start, notes_columns).tolist()
    # funding
    funding_start_date_row = 42
    funding_start_date_row_list = np.arange(funding_start_date_row, funding_start_date_row + 1, 1)
    funding_start_date_col_start = 2
    funding_start_date_col_list = np.arange(funding_start_date_col_start, df_num_cols + funding_start_date_col_start, notes_columns).tolist()
    # coupon_trigger location
    coupon_trigger_row = 80
    coupon_trigger_row_end = 117
    coupon_trigger_row_list = np.arange(coupon_trigger_row, coupon_trigger_row_end, 1)
    coupon_trigger_col_start = 4
    coupon_trigger_col_list = np.arange(coupon_trigger_col_start, df_num_cols+coupon_trigger_col_start, notes_columns).tolist()
    # autocall_trigger location
    autocall_trigger_row = 80
    autocall_trigger_row_end = 117
    autocall_trigger_row_list = np.arange(autocall_trigger_row, autocall_trigger_row_end, 1)
    autocall_trigger_col_start = 2
    autocall_trigger_col_list = np.arange(autocall_trigger_col_start, df_num_cols + autocall_trigger_col_start, notes_columns).tolist()
    # equities name and initial levels
    equity_name_row = 118
    equity_name_row_end = 123
    equity_name_row_list = np.arange(equity_name_row, equity_name_row_end, 1)
    equity_initial_levels_row_list = equity_name_row_list
    equity_name_col_start = 2
    equity_initial_levels_col_start = 3
    equity_name_col_list = np.arange(equity_name_col_start, df_num_cols + equity_name_col_start, notes_columns).tolist()
    equity_initial_levels_col_list = np.arange(equity_initial_levels_col_start, df_num_cols + equity_initial_levels_col_start, notes_columns).tolist()

    # Get values for all available notes
    note_id_values = get_data_value(df, isin_row_list, isin_col_list, is_id=False)
    #getting issue date and isin
    isin_values = []
    issue_date_values = []
    for value in note_id_values:
        issue_date_str = '20' + value[0].split('_')[0][0:2] + '-' + value[0].split('_')[0][2:4] + '-' + value[0].split('_')[0][4:6]
        issue_date = datetime.datetime.strptime(issue_date_str, "%Y-%m-%d").date()
        issue_date_values.append([issue_date])
        isin_values.append([value[0].split('_')[1]])

    notional_values = get_data_value(df, notional_row_list, notional_col_list, is_id=False)
    currency_values = get_data_value(df, currency_row_list, currency_col_list, is_id=False)
    coupon_values = get_data_value(df, coupon_row_list, coupon_col_list, is_id=False)
    coupon_uncon_values = get_data_value(df, coupon_uncond_row_list, coupon_uncond_col_list, is_id=False)
    reoffer_values = get_data_value(df, reoffer_row_list, reoffer_col_list, is_id=False)
    coupon_obs_date_values, note_id = get_data_value(df, coupon_obs_date_row_list, coupon_obs_date_col_list, is_id=True)
    accrual_start_date_values = get_data_value(df, accrual_start_date_row_list, accrual_start_date_col_list, is_id=False)
    accrual_end_date_values = get_data_value(df, accrual_end_date_row_list, accrual_end_date_col_list, is_id=False)
    coupon_paydate_values = get_data_value(df, coupon_paydate_row_list, coupon_paydate_col_list, is_id=False)
    coupon_paydate_id = []
    counter = 1
    for elem in note_id:
        temp_list = []
        for i in range(len(elem)):
            temp_list.append(counter)
            counter += 1
        coupon_paydate_id.append(temp_list)
    funding_start_date_values = get_data_value(df, funding_start_date_row_list, funding_start_date_col_list, is_id=False)
    coupon_trigger_values = get_data_value(df, coupon_trigger_row_list, coupon_trigger_col_list, is_id=False)
    autocall_trigger_values = get_data_value(df, autocall_trigger_row_list, autocall_trigger_col_list, is_id=False)
    equity_name_values = get_data_value(df, equity_name_row_list, equity_name_col_list, is_id=False)
    equity_initial_levels_values = get_data_value(df, equity_initial_levels_row_list, equity_initial_levels_col_list, is_id=False)

    return isin_values, issue_date_values, notional_values, note_id, currency_values, coupon_values, coupon_uncon_values, reoffer_values, coupon_obs_date_values, \
           accrual_start_date_values, accrual_end_date_values, coupon_paydate_values, funding_start_date_values, coupon_trigger_values, autocall_trigger_values, \
           equity_name_values, equity_initial_levels_values, coupon_paydate_id
