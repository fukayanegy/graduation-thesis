import pandas as pd
import numpy as np
from src.apply_func import format_values_RandD
from src.apply_func import format_values
from src.format_data import format_data
from src.download_excel import download_excel
from src import calc_sales_summary
from src import convert_vals
from src import calc_roe
from src import calc_RandD
import os

def apply_func_add(row, database1_list, database2_list):
    if row['is_finish']:
        return row
    if f'{row['docID']}.pickle' in database1_list:
        data = pd.read_pickle(f'database/{row['docID']}.pickle')
    elif f'{row['docID']}.pickle' in database2_list:
        data = pd.read_pickle(f'database2/{row['docID']}.pickle')
    else:
        return row
    data = format_data(data)
    row = calc_roe.calc_prev_roe(row, data)
    return row

if __name__ == '__main__':
    data = pd.read_pickle('data3/docid_perfect_list.pickle')
    data = data.reset_index()
    data.to_excel('/mnt/c/WSLTMPDIR/add_data.xlsx')
