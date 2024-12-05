import pandas as pd
from src import calc_utils

# calc_row_string_data
def get_randd(row, data):
    ele_id1 = 'jpcrp_cor:ResearchAndDevelopmentExpensesResearchAndDevelopmentActivities'
    ele_id2 = 'jppfs_cor:ResearchAndDevelopmentExpensesSGA'
    ele_id3 = 'jpcrp_cor:ResearchAndDevelopmentActivitiesTextBlock'
    ele_id4 = 'jpcrp_cor:ResearchAndDevelopmentExpensesIncludedInGeneralAndAdministrativeExpensesAndManufacturingCostForCurrentPeriodTextBlock'

    row['研究開発費、研究開発活動'] = calc_utils.calc_row_data(data, ele_id1, False, True)
    row['研究開発費、販売費及び一般管理費'] = calc_utils.calc_row_data(data, ele_id2, False, True)
    row['研究開発活動 [テキストブロック]'] = calc_utils.calc_row_string_data(data, ele_id3, 'FilingDateInstant')
    row['一般管理費及び当期製造費用に含まれる研究開発費 [テキストブロック]'] = calc_utils.calc_row_string_data(data, ele_id4, 'CurrentYearDuration')
    return row
