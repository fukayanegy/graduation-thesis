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
    all_data = pd.read_pickle('data3/all_data2.pickle')
    finish_data = pd.read_pickle('data3/finish_data3.pickle')
    finish_data2 = pd.read_pickle('data3/finish_data_tmp.pickle')
    data = all_data[['secCode', 'year', 'docID', 'name', '研究開発費、研究開発活動', '研究開発費、販売費及び一般管理費', '研究開発活動 [テキストブロック]', '一般管理費及び当期製造費用に含まれる研究開発費 [テキストブロック]',]]
    data = pd.concat([data, finish_data2[['RandD_all', 'RandD_general']]], axis=1)
    column_names = ['研究開発費、研究開発活動', '研究開発費、販売費及び一般管理費', 'RandD_all', 'RandD_general']
    for column_name in column_names:
        data = convert_vals.convert_vals(data, column_name, 'int')
    data = data.replace({np.nan: None})
    data['RandD_all_text'] = None
    data = data[(data['RandD_all'].isna()) & (data['RandD_general'].isna())]
    data = data[data['year'] == 2020]
    data = format_values_RandD(data)
    data.to_pickle('data3/RandD.pickle')
    # print(data[['RandD_all', 'RandD_all_text', 'name']])
    # finish_data2['RandD'] = finish_data2['RandD_all']
    # finish_data2.loc[finish_data2['RandD'].isna(), 'RandD'] = finish_data2.loc[finish_data2['RandD'].isna(), 'RandD_all']
    # nan_data = (finish_data2[['year', 'name', 'RandD', 'RandD_all', 'RandD_general',  'RandD_general_text']])
    # print(nan_data.isna().sum())

    # finish_data.to_excel('/mnt/c/WSLTMPDIR/data.xlsx', index=False)
    # exit()

    # column_names = ['研究開発費、研究開発活動', '研究開発費、販売費及び一般管理費']
    # for column_name in column_names:
    #     data = convert_vals.convert_vals(data, column_name, 'int')
    # data = data.replace({np.nan: None})
    # result = format_values_RandD(data)

    # i = int(input())
    # j = tmp.index[i]
    # print(tmp.loc[j, '一般管理費及び当期製造費用に含まれる研究開発費 [テキストブロック]'])

    # list1 = os.listdir('database')
    # list2 = os.listdir('database2')
    # result = result.apply(apply_func_add, axis=1, database1_list=list1, database2_list=list2)

    # data = data[['secCode', 'year', 'docID', 'name', 'market_type', 'is_consolidated', '33indus', '17indus', 'scale_code']]
    # list1 = os.listdir('database')
    # list2 = os.listdir('database2')
    # data = data.apply(apply_func, axis=1, database1_list=list1, database2_list=list2)
    # data.to_pickle('data3/all_data3.pickle')
