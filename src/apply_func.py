import pandas as pd
from src import calc_sales_summary
from src import calc_equity_to_asset_ratio
from src import calc_roa
from src import calc_roe
from src import calc_RandD
from src import get_randd
from src import calc_equity_to_asset_ratio
from src.format_data import format_data
from src import directors_rate
from src import employees

def apply_func(row, database1_list, database2_list):
    index = int(row.name)
    if index % 500 == 0:
        print(index, row['year'], row['name'])
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
    row = calc_sales_summary.get_netsales(row, data)
    row = calc_sales_summary.get_netsales_other(row, data)
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
    if f'{row['docID']}.pickle' in database1_list:
        data = pd.read_pickle(f'database/{row['docID']}.pickle')
    elif f'{row['docID']}.pickle' in database2_list:
        data = pd.read_pickle(f'database2/{row['docID']}.pickle')
    else:
        return row
    data = format_data(data)
    return row

def calc_RandDall(row, ):
    if (row['RandD_all'] != None):
        row['RandD_all_text'] = row['RandD_all']
        return row
    if (row['研究開発活動 [テキストブロック]'] == None):
        row['RandD_all_text'] = None
        return row
    tmp = calc_RandD.search_yen(row['研究開発活動 [テキストブロック]'])
    if tmp == None:
        row['RandD_all_text'] = 0
    else:
        row['RandD_all_text'] = tmp
    return row

def calc_RandD_general(row):
    general_textblock = '一般管理費及び当期製造費用に含まれる研究開発費 [テキストブロック]'
    if row['RandD_general'] != None:
        row['RandD_general_text'] = row['RandD_general']
        return row
    if (row[general_textblock] == None):
        row['RandD_general_text'] = None
        return row
    s = (calc_RandD.search_yen2(row[general_textblock]))
    return row

def format_values(data):
    # 従業員数
    result = pd.DataFrame({})
    result['secCode'] = data['secCode']
    result['year'] = data['year']
    result['docID'] = data['docID']
    result.loc[:, '従業員数'] = data.loc[:, '従業員数']
    result.loc[(result['従業員数'].isna()), '従業員数'] = data.loc[(result['従業員数'].isna()), '従業員数_nc']
    result['name'] = data['name']
    return result

def format_values_RandD(data):
    general_textblock = '一般管理費及び当期製造費用に含まれる研究開発費 [テキストブロック]'
    result = pd.DataFrame({})
    result['secCode'] = data['secCode']
    result['year'] = data['year']
    result['docID'] = data['docID']
    result.loc[:, 'RandD_all'] = data.loc[:, '研究開発費、研究開発活動']

    data = pd.concat([data, result[['RandD_all']]], axis=1)

    # result = data.apply(calc_RandDall, axis=1)
    result.loc[:, 'RandD_general'] = data.loc[:, '研究開発費、販売費及び一般管理費']

    data = pd.concat([data, result[['RandD_general']]], axis=1)

    result = data.apply(calc_RandD_general, axis=1)
    return result

def format_values_directors(data):
    result = pd.DataFrame({})
    result['secCode'] = data['secCode']
    result['year'] = data['year']
    result['docID'] = data['docID']

    result.loc[:, 'male_num'] = data.loc[:, '役員のうち男性の人数']
    result.loc[:, 'female_num'] = data.loc[:, '役員のうち女性の人数']

    result['name'] = data['name']
    return result


def format_values_tmp(data):
    result = pd.DataFrame({})
    result['secCode'] = data['secCode']
    result['year'] = data['year']
    result['docID'] = data['docID']

    result.loc[(data['is_consolidated']), '自己資本比率'] = data.loc[(data['is_consolidated']), '自己資本比率_br']
    result.loc[(data['is_consolidated']) & (result['自己資本比率'].isna()), '自己資本比率'] = data.loc[(data['is_consolidated']), '自己資本比率']
    result.loc[(data['is_consolidated']) & (result['自己資本比率'].isna()), '自己資本比率'] = data.loc[(data['is_consolidated']), '自己資本比率_br_nc']

    result.loc[(~data['is_consolidated']), '自己資本比率'] = data.loc[(~data['is_consolidated']), '自己資本比率_br_nc']
    result.loc[(~data['is_consolidated']) & (result['自己資本比率'].isna()), '自己資本比率'] = data.loc[(~data['is_consolidated']), '自己資本比率_nc']

    result['name'] = data['name']
    return result


def format_ROE(data):
    result = pd.DataFrame({})
    result['secCode'] = data['secCode']
    result['year'] = data['year']
    result['docID'] = data['docID']

    result.loc[(data['is_consolidated']), 'ROE'] = data.loc[(data['is_consolidated']), 'ROE']
    result.loc[(data['is_consolidated']) & (result['ROE'].isna()), 'ROE'] = data.loc[(data['is_consolidated']), 'ROE_nc']
    result.loc[(data['is_consolidated']) & (result['ROE'].isna()), 'ROE'] = data.loc[(data['is_consolidated']), 'prev_ROE']
    result.loc[(data['is_consolidated']) & (result['ROE'].isna()), 'ROE'] = data.loc[(data['is_consolidated']), 'prev_ROE_nc']

    result.loc[(~data['is_consolidated']), 'ROE'] = data.loc[(~data['is_consolidated']), 'ROE_nc']
    result.loc[(~data['is_consolidated']) & (result['ROE'].isna()), 'ROE'] = data.loc[(~data['is_consolidated']), 'ROE']
    result.loc[(~data['is_consolidated']) & (result['ROE'].isna()), 'ROE'] = data.loc[(~data['is_consolidated']), 'prev_ROE']
    result.loc[(~data['is_consolidated']) & (result['ROE'].isna()), 'ROE'] = data.loc[(~data['is_consolidated']), 'prev_ROE_nc']
    result['name'] = data['name']

    return result


def format_values_salse(data):
    result = pd.DataFrame({})
    result['secCode'] = data['secCode']
    result['year'] = data['year']
    result['docID'] = data['docID']

    ### 連結企業があるため'NonConsolidatedMember'ではない方で算出する
    result.loc[(data['is_consolidated']), '売上高'] = data.loc[(data['is_consolidated']), '売上高、経営指標等']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上収益（IFRS）、経営指標等']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上収益、経営指標等']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '経常収益、経営指標等']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '営業収入、経営指標等']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '経常収益、保険業']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上高（US GAAP）、経営指標等']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上高_other']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上高_other_ifrs']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上高_other2']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上高_other3']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上収益、経営指標等2']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '営業総収入、経営指標等']

    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上高、経営指標等_nc']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上収益（IFRS）、経営指標等_nc']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '売上収益、経営指標等_nc']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '経常収益、経営指標等_nc']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '営業収入、経営指標等_nc']
    result.loc[(data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(data['is_consolidated']), '経常収益、保険業_nc']

    ### 連結企業がないため'NonConsolidatedMember'で算出する
    result.loc[(~data['is_consolidated']), '売上高'] = data.loc[(~data['is_consolidated']), '売上高、経営指標等_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上収益（IFRS）、経営指標等_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上収益、経営指標等_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '経常収益、経営指標等_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '営業収入、経営指標等_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '経常収益、保険業_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上高（US GAAP）、経営指標等_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上高_other_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上高_other_ifrs_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上高_other2_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上高_other3_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上収益、経営指標等2_nc']
    result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '営業総収入、経営指標等_nc']

    # result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上高、経営指標等']
    # result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上収益（IFRS）、経営指標等']
    # result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '売上収益、経営指標等']
    # result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '経常収益、経営指標等']
    # result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '営業収入、経営指標等']
    # result.loc[(~data['is_consolidated']) & (result['売上高'].isna()), '売上高'] = data.loc[(~data['is_consolidated']), '経常収益、保険業']
    return result
