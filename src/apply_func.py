import pandas as pd
from src import calc_sales_summary
from src import calc_equity_to_asset_ratio
from src import calc_roa
from src import calc_roe
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

def format_values(data):
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
