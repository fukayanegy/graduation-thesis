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
    row = calc_roe.calc_roe(row, data)
    row = get_randd.get_randd(row, data)
    row = calc_roa.calc_net_assets(row, data)
    row = calc_roa.calc_total_assets(row, data)
    row = calc_roa.calc_ordinary_income(row, data)
    row = directors_rate.get_directors_info(row, data)
    row = calc_equity_to_asset_ratio.calc_equity_to_asset_ratio(row, data)
    row = employees.calc_employees(row, data)
    return row
