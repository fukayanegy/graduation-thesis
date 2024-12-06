import pandas as pd
from src import calc_utils

def calc_employees(row, data):
    ele_id1 = 'jpcrp_cor:NumberOfEmployees'
    ele_id2 = 'jpcrp_cor:AverageAgeYearsInformationAboutReportingCompanyInformationAboutEmployees'
    ele_id3 = 'jpcrp_cor:AverageLengthOfServiceYearsInformationAboutReportingCompanyInformationAboutEmployees'
    ele_id4 = 'jpcrp_cor:AverageAnnualSalaryInformationAboutReportingCompanyInformationAboutEmployees'
    con_id = 'CurrentYearInstant'
    con_id_nc = 'CurrentYearInstant_NonConsolidatedMember'

    row['従業員数'] = calc_utils.calc_row_string_data(data, ele_id1,     con_id)
    row['平均年齢'] = calc_utils.calc_row_string_data(data, ele_id2,     con_id)
    row['平均勤続年数'] = calc_utils.calc_row_string_data(data, ele_id3, con_id)
    row['平均年間給与'] = calc_utils.calc_row_string_data(data, ele_id4, con_id)

    row['従業員数_nc'] = calc_utils.calc_row_string_data(data, ele_id1,     con_id_nc)
    row['平均年齢_nc'] = calc_utils.calc_row_string_data(data, ele_id2,     con_id_nc)
    row['平均勤続年数_nc'] = calc_utils.calc_row_string_data(data, ele_id3, con_id_nc)
    row['平均年間給与_nc'] = calc_utils.calc_row_string_data(data, ele_id4, con_id_nc)

    return row
