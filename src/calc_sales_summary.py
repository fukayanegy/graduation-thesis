import pandas as pd
from src.calc_utils import calc_row_data_str

'''
    data.at[(23890, '2023-03-27'), 'result'] = 98515000000 + (98515000000 - 88768000000)
    data.at[(80320, '2023-06-23'), 'result'] = (545279000000)

    data.at[(87500, '2016-06-24'), 'result'] = (7333947000000)
    data.at[(87500, '2017-06-26'), 'result'] = (6456796000000)
    data.at[(87500, '2018-06-25'), 'result'] = (7037827000000)
    data.at[(87500, '2019-06-24'), 'result'] = (7184093000000)
    data.at[(87500, '2020-06-23'), 'result'] = (7114099000000)
    data.at[(87500, '2021-06-22'), 'result'] = (7827806000000)
    data.at[(87500, '2022-06-21'), 'result'] = (8209708000000)
    data.at[(87500, '2023-06-27'), 'result'] = (9519445000000)

    result.loc[1601, '売上高'] = 98515000000 + (98515000000 - 88768000000)
    result.loc[8847, '売上高'] = 85241450000
    result.loc[8848, '売上高'] = 89491193000
    result.loc[8849, '売上高'] = 101923502000
    result.loc[8850, '売上高'] = 97331686000
    result.loc[8851, '売上高'] = 89611525000
'''

def calc_row_data(data, element_id, context_id):
    row_data_row = data[
            (data['要素ID'] == element_id) &
            (data['コンテキストID'] == context_id)
            ].reset_index(drop=True)
    if len(row_data_row) == 0:
        return None
    elif len(row_data_row) == 1:
        row_data = row_data_row.loc[0, '値']
    else:
        # print(len(row_data_row))
        row_data = row_data_row.loc[0, '値']
    return row_data


def get_netsales(row, data):
    row['売上高'] = calc_row_data(data, 'jppfs_cor:NetSales', 'CurrentYearDuration')
    row['売上高_nc'] = calc_row_data(data, 'jppfs_cor:NetSales', 'CurrentYearDuration_NonConsolidatedMember')
    row['売上高、経営指標等'] = calc_row_data(data, 'jpcrp_cor:NetSalesSummaryOfBusinessResults', 'CurrentYearDuration')
    row['売上高、経営指標等_nc'] = calc_row_data(data, 'jpcrp_cor:NetSalesSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    row['売上収益、経営指標等'] = calc_row_data(data, 'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults', 'CurrentYearDuration')
    row['売上収益、経営指標等_nc'] = calc_row_data(data, 'jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    row['売上収益（IFRS）、経営指標等'] = calc_row_data(data, 'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults', 'CurrentYearDuration')
    row['売上収益（IFRS）、経営指標等_nc'] = calc_row_data(data, 'jpcrp_cor:RevenueIFRSSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    row['経常収益、経営指標等'] = calc_row_data(data, 'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults', 'CurrentYearDuration')
    row['経常収益、経営指標等_nc'] = calc_row_data(data, 'jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    row['営業収入、経営指標等'] = calc_row_data(data, 'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults', 'CurrentYearDuration')
    row['営業収入、経営指標等_nc'] = calc_row_data(data, 'jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    row['経常収益、保険業']    = calc_row_data(data, 'jppfs_cor:OperatingIncomeINS', 'CurrentYearDuration')
    row['経常収益、保険業_nc'] = calc_row_data(data, 'jppfs_cor:OperatingIncomeINS', 'CurrentYearDuration_NonConsolidatedMember')
    row['売上高（US GAAP）、経営指標等'] = calc_row_data(data, 'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults', 'CurrentYearDuration')
    row['売上高（US GAAP）、経営指標等_nc'] = calc_row_data(data, 'jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    row['営業総収入、経営指標等'] = calc_row_data(data, 'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults', 'CurrentYearDuration')
    row['営業総収入、経営指標等_nc'] = calc_row_data(data, 'jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    row['売上収益、経営指標等2'] = calc_row_data(data, 'jpcrp_cor:RevenueKeyFinancialData', 'CurrentYearDuration')
    row['売上収益、経営指標等2_nc'] = calc_row_data(data, 'jpcrp_cor:RevenueKeyFinancialData', 'CurrentYearDuration_NonConsolidatedMember')
    return row

def get_netsales_other(row, data):
    ele_id = 'NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults'
    ele_id2 = 'NetSalesIFRSSummaryOfBusinessResults'
    ele_id3 = 'NetSalesAndOtherOperatingRevenueSummaryOfBusinessResults'
    ele_id4 = 'NetSalesAndOperatingRevenue2SummaryOfBusinessResults'

    context_id = 'CurrentYearDuration'
    context_id_nc = 'CurrentYearDuration_NonConsolidatedMember'
    row['売上高_other'] = calc_row_data_str(data, ele_id, context_id)
    row['売上高_other_nc'] = calc_row_data_str(data, ele_id, context_id_nc)
    row['売上高_other_ifrs'] = calc_row_data_str(data, ele_id2, context_id)
    row['売上高_other_ifrs_nc'] = calc_row_data_str(data, ele_id2, context_id_nc)
    row['売上高_other2'] = calc_row_data_str(data, ele_id3, context_id)
    row['売上高_other2_nc'] = calc_row_data_str(data, ele_id3, context_id_nc)
    row['売上高_other3'] = calc_row_data_str(data, ele_id4, context_id)
    row['売上高_other3_nc'] = calc_row_data_str(data, ele_id4, context_id_nc)
    return row
