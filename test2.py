col_names = ['IssueDate', 'Side', 'Notional', 'Currency', 'ISIN']
str_temp = ''
for i in range(len(col_names)):
    str_temp = str_temp + '"{}",'.format(col_names[i])