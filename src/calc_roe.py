import pandas as pd
from src import calc_utils

def calc_roe(row, data):
    roe_str = 'jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults'
    row['ROE'] = calc_utils.calc_row_data(data, roe_str, False, True)
    row['ROE_nc'] = calc_utils.calc_row_data(data, roe_str, False, False)
    return row
