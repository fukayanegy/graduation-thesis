import pandas as pd
import numpy as np
from src import calc_sales_summary
from src import get_docid
from src import get_csvdata
from src import datetime_calc
from src import calc_equity_to_asset_ratio
from src import calc_roa
from src import calc_roe
from src import get_randd
from src import calc_equity_to_asset_ratio
from src.format_data import format_data
from src import directors_rate
from src import employees
import os

def apply_func(row, database1_list, database2_list):
    if f'{row['docID']}.pickle' in database1_list:
        row['is_csv'] = True
        data = pd.read_pickle(f'database/{row['docID']}.pickle')
    elif f'{row['docID']}.pickle' in database2_list:
        row['is_csv'] = True
        data = pd.read_pickle(f'database2/{row['docID']}.pickle')
    else:
        row['is_csv'] = False
        return row
    data = format_data(data)
    # print(data[['項目名', '値']])
    row = calc_sales_summary.get_netsales(row, data)
    row = calc_roe.calc_roe(row, data)
    row = get_randd.get_randd(row, data)
    row = calc_roa.calc_net_assets(row, data)
    row = calc_roa.calc_total_assets(row, data)
    row = calc_roa.calc_ordinary_income(row, data)
    row = directors_rate.get_directors_info(row, data)
    row = calc_equity_to_asset_ratio.calc_equity_to_asset_ratio(row, data)
    row = employees.calc_employees(row, data)
    return row

if __name__ == '__main__':
    data = pd.read_pickle('data3/all_data.pickle')
    print(data.isna().sum())
    exit()
    # '/売上高', '/研究開発費', '/経常利益', '/純資産額' ,'/総資産額', '自己資本比率','/ROE, '従業員数'
    na_data = all_data[all_data['売上高'].isna()]
    na_data = na_data[:20]
    na_data = na_data.apply(apply_func, axis=1)
    print(na_data[['ROE', 'ROE_nc']])
    na_data.to_pickle('data3/na_data.pickle')

    # download_data = pd.read_pickle(f'database2/S100JKNH.pickle')
    # download_data.to_excel('/mnt/c/WSLTMPDIR/S100JKNH.xlsx')
