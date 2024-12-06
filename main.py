import pandas as pd
import numpy as np
from src import calc_sales_summary
from src import get_docid
from src import get_csvdata
from src import calc_RandD
from src import calc_equity_to_asset_ratio
from src import calc_roa
from src import calc_roe
from src import get_randd
from src import calc_equity_to_asset_ratio
from src.format_data import format_data
from src import directors_rate
from src import employees
from src.download_excel import download_excel
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
        # print(row['役員のうち男性の人数'], row['役員のうち女性の人数'], row['役員のうち女性の割合'])
    else:
        return row

if __name__ == '__main__':
    data = pd.read_pickle('data3/all_data3.pickle')
    print(data[['役員のうち男性の人数', '役員のうち女性の人数']].isna().sum())
    print(data[(data['name'] == '乃村工藝社')][['役員のうち男性の人数']])

    list1 = os.listdir('database')
    list2 = os.listdir('database2')
    data = data.apply(apply_func_add, axis=1, database1_list=list1, database2_list=list2)

    print(data[['役員のうち男性の人数', '役員のうち女性の人数']].isna().sum())
    print(data[16090:16100][['year', '役員のうち男性の人数']])
