import pandas as pd

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
        row_data = 'Error'
    return row_data

def calc_row_data_str(data, include_str):
    row_data_row = data[
            (data['要素ID'].str.contains(include_str, na=False))
                        ].reset_index(drop=True)
    if len(row_data_row) == 0:
        return None, None
    else:
        return (row_data_row.loc[0, '値']), (row_data_row.loc[1, '値'])

def get_netsales(row, data):
    data = data[(data['相対年度'] == "当期末") | (data['相対年度'] == "当期") | (data['相対年度'] == "提出日時点")]
    data = data[(data['ユニットID'] == "JPY") |
                (data['ユニットID'] == "JPYPerShares") |
                (data['ユニットID'] == "pure") |
                (data['ユニットID'] == "shares")]
    data = data[(data['コンテキストID'] == 'CurrentYearDuration') |
                (data['コンテキストID'] == 'CurrentYearDuration_NonConsolidatedMember') |
                (data['コンテキストID'] == 'CurrentYearInstant') |
                (data['コンテキストID'] == 'CurrentYearInstant_NonConsolidatedMember') |
                (data['コンテキストID'] == 'FilingDateInstant')]
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
    if row['name'] == '日本電設工業':
        row['売上高']    = calc_row_data(data, 'jpcrp030000-asr_E00115-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults', 'CurrentYearDuration')
        row['売上高_nc'] = calc_row_data(data, 'jpcrp030000-asr_E00115-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    elif row['name'] == '新日本空調':
        row['売上高']    = calc_row_data(data, 'jpcrp030000-asr_E00227-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults', 'CurrentYearDuration')
        row['売上高_nc'] = calc_row_data(data, 'jpcrp030000-asr_E00227-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    elif row['name'] == '東洋エンジニアリング':
        row['売上高']    = calc_row_data(data, 'jpcrp030000-asr_E01661-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults', 'CurrentYearDuration')
        row['売上高_nc'] = calc_row_data(data, 'jpcrp030000-asr_E01661-000:NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults', 'CurrentYearDuration_NonConsolidatedMember')
    elif row['name'] == 'レイズネクスト':
        row['売上高'], row['売上高_nc'] = calc_row_data_str(data, 'NetSalesOfCompletedConstructionContractsSummaryOfBusinessResults')
    return row
