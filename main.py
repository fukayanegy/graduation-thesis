import pandas as pd
import numpy as np
from src import calc_sales_summary
from src import get_docid
from src import get_csvdata
from src import datetime_calc
from src import calc_sales_summary
from src import calc_roa
from src import calc_roe
from src import get_randd
from src import calc_equity_to_asset_ratio
from src.format_data import format_data
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
    return row

if __name__ == '__main__':
    data = pd.read_pickle('data3/docid_perfect_list.pickle')
    old_data = pd.read_pickle('data/final_data.pickle')
    data = data.reset_index()
    old_data = old_data.reset_index()

    data['secCode'] = data['secCode'].astype('str')
    old_data['secCode'] = old_data['secCode'].astype('str')
    data['year'] = data['year'].astype('int')
    old_data['year'] = old_data['year'].astype('int')
    all_data = pd.merge(data, old_data, on=['secCode', 'year'], how='left')
    all_data = all_data.rename(columns={'docID_x': 'docID'})

    test = all_data[all_data['year'] == 2020]
    test = test[['secCode', 'year', 'docID', 'name']]
    one = os.listdir('database')
    two = os.listdir('database2')
    test = test[:1]
    test = test.apply(apply_func, axis=1, database1_list=one, database2_list=two)
    print(test.iloc[0, :])

    exit()
    # '/売上高', '/研究開発費', '/経常利益', '/純資産額' ,'/総資産額', '自己資本比率','/ROE, '従業員数'
    na_data = all_data[all_data['売上高'].isna()]
    na_data = na_data[:20]
    na_data = na_data.apply(apply_func, axis=1)
    print(na_data[['ROE', 'ROE_nc']])
    na_data.to_pickle('data3/na_data.pickle')

    # download_data = pd.read_pickle(f'database2/S100JKNH.pickle')
    # download_data.to_excel('/mnt/c/WSLTMPDIR/S100JKNH.xlsx')
