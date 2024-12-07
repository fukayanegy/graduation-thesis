import pandas as pd
import numpy as np
from src.apply_func import apply_func
from src.apply_func import format_values
from src.format_data import format_data
from src.download_excel import download_excel
from src import calc_sales_summary
from src import convert_vals
from src import calc_roe
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
    # download_excel('S100OGB7')
    # download_excel('S1005BQI')
    # download_excel('S100IHOK')
    # download_excel('S100LDRB')
    # download_excel('S100O413')
    # exit()
    data = pd.read_pickle('data3/all_data2.pickle')
    finish_data = pd.read_pickle('data3/finish_data.pickle')

    column_names = ['ROE', 'ROE_nc', 'prev_ROE', 'prev_ROE_nc']
    for column_name in column_names:
        data = convert_vals.convert_vals(data, column_name, 'float')
    data = data.replace({np.nan: None})
    result = format_values(data)
    list1 = os.listdir('database')
    list2 = os.listdir('database2')
    # result = result.apply(apply_func_add, axis=1, database1_list=list1, database2_list=list2)
    print(result[result['ROE'].isna()])

    # data = data[['secCode', 'year', 'docID', 'name', 'market_type', 'is_consolidated', '33indus', '17indus', 'scale_code']]
    # list1 = os.listdir('database')
    # list2 = os.listdir('database2')
    # data = data.apply(apply_func, axis=1, database1_list=list1, database2_list=list2)
    # data.to_pickle('data3/all_data3.pickle')


'''
Index(['secCode', 'year', 'docID', 'name', 'market_type', 'is_consolidated',
       '33indus', '17indus', 'scale_code', 'is_csv', '売上高', '売上高_nc',
       '売上高、経営指標等', '売上高、経営指標等_nc', '売上収益、経営指標等', '売上収益、経営指標等_nc',
       '売上収益（IFRS）、経営指標等', '売上収益（IFRS）、経営指標等_nc', '経常収益、経営指標等',
       '経常収益、経営指標等_nc', '営業収入、経営指標等', '営業収入、経営指標等_nc', '経常収益、保険業',
       '経常収益、保険業_nc', '売上高（US GAAP）、経営指標等', '売上高（US GAAP）、経営指標等_nc',
       '売上高_other', '売上高_other_nc', '売上高_other_ifrs', '売上高_other_ifrs_nc',
       'ROE', 'ROE_nc', 
       '研究開発費、研究開発活動', '研究開発費、販売費及び一般管理費',
       '研究開発活動 [テキストブロック]', '一般管理費及び当期製造費用に含まれる研究開発費 [テキストブロック]', '純資産額',
       '純資産額_nc', '純資産額_br', '純資産額_br_nc', '総資産額', '総資産額_nc', '総資産額_br',
       '総資産額_br_nc', '経常利益', '経常利益_nc', '経常利益_br', '経常利益_br_nc', '役員のうち男性の人数',
       '役員のうち女性の人数', '役員のうち女性の割合', '自己資本比率', '自己資本比率_nc', '自己資本比率_br',
       '自己資本比率_br_nc', '従業員数', '平均年齢', '平均勤続年数', '平均年間給与', '従業員数_nc',
       '平均年齢_nc', '平均勤続年数_nc', '平均年間給与_nc'],
'''
