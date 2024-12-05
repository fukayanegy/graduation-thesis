import pandas as pd
from src import calc_utils

def calc_net_assets(row, data):
    '''
    純資産額
    '''
    ele_id1 = 'jpcrp_cor:NetAssetsSummary'
    ele_id2 = 'jpcrp_cor:NetAssetsSummaryOfBusinessResults'
    row['純資産額'] = calc_utils.calc_row_data(data, ele_id1, True, True)
    row['純資産額_nc'] = calc_utils.calc_row_data(data, ele_id1, True, False)
    row['純資産額_br'] = calc_utils.calc_row_data(data, ele_id2, True, True)
    row['純資産額_br_nc'] = calc_utils.calc_row_data(data, ele_id2, True, False)
    return row

def calc_total_assets(row, data):
    '''
    総資産額
    '''
    ele_id1 = 'jpcrp_cor:TotalAssetsSummary'
    ele_id2 = 'jpcrp_cor:TotalAssetsSummaryOfBusinessResults'
    context_id = 'CurrentYearInstant'
    row['総資産額'] = calc_utils.calc_row_data(data, ele_id1, True, True)
    row['総資産額_nc'] = calc_utils.calc_row_data(data, ele_id1, True, False)
    row['総資産額_br'] = calc_utils.calc_row_data(data, ele_id2, True, True)
    row['総資産額_br_nc'] = calc_utils.calc_row_data(data, ele_id2, True, False)
    return row

def calc_ordinary_income(row, data):
    '''
    経常利益又は経常損失
    '''
    ele_id1 = 'jppfs_cor:OrdinaryIncome'
    ele_id2 = 'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults'
    context_id = 'CurrentYearDuration'
    row['経常利益'] = calc_utils.calc_row_data(data, ele_id1, False, True)
    row['経常利益_nc'] = calc_utils.calc_row_data(data, ele_id1, False, False)
    row['経常利益_br'] = calc_utils.calc_row_data(data, ele_id2, False, True)
    row['経常利益_br_nc'] = calc_utils.calc_row_data(data, ele_id2, False, False)
    return row
