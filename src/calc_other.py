import pandas as pd

def calc_ordinary_income(data):
    '''
    経常利益または経常損失
    '''
    element_id = 'jpcrp_cor:OrdinaryIncomeLossSummaryOfBusinessResults'
    context_id = 'CurrentYearDuration'
    ordinary_income_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(ordinary_income_row) == 0:
        return None
    ordinary_income = ordinary_income_row.loc[0, '値']
    try:
        ordinary_income = int(ordinary_income)
    except ValueError:
        ordinary_income = -1
    return ordinary_income

def calc_employees(data):
    '''
    従業員数
    '''
    element_id = 'jpcrp_cor:NumberOfEmployees'
    context_id = 'CurrentYearInstant'
    employees_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(employees_row) == 0:
        return None
    employees = employees_row.loc[0, '値']
    try:
        employees = int(employees)
    except ValueError:
        employees = -1
    return employees


def calc_capital_stock(data):
    '''
    資本金
    '''
    element_id = 'jppfs_cor:CapitalStock'
    context_id = 'CurrentYearInstant'
    capital_stock_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(capital_stock_row) == 0:
        return None
    capital_stock = capital_stock_row.loc[0, '値']
    try:
        capital_stock = int(capital_stock)
    except ValueError:
        capital_stock = -1
    return capital_stock

def calc_shareholding_rate(data):
    '''
    発行済株式の総数に対する所有株式数の割合
    '''
    element_id = 'jpcrp_cor:ShareholdingRatio'
    context_id = 'CurrentYearInstant'
    shareholding_rate_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(shareholding_rate_row) == 0:
        return None
    shareholding_rate = shareholding_rate_row.loc[0, '値']
    try:
        shareholding_rate = int(shareholding_rate)
    except ValueError:
        shareholding_rate = -1
    return shareholding_rate
