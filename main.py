import pandas as pd
import numpy as np
from src.apply_func import apply_func
from src.format_data import format_data
from src import directors_rate
from src.download_excel import download_excel
import os

def apply_func_add(row, database1_list, database2_list):
    if row['役員のうち女性の人数'] == None:
        if f'{row['docID']}.pickle' in database1_list:
            data = pd.read_pickle(f'database/{row['docID']}.pickle')
        elif f'{row['docID']}.pickle' in database2_list:
            data = pd.read_pickle(f'database2/{row['docID']}.pickle')
        else:
            return row
        data = format_data(data)
        row = directors_rate.get_directors_info(row, data)
        return row
    else:
        return row

if __name__ == '__main__':
    data = pd.read_pickle('data3/all_data3.pickle')

    list1 = os.listdir('database')
    list2 = os.listdir('database2')
    data = data.apply(apply_func, axis=1, database1_list=list1, database2_list=list2)
