import pandas as pd

def calc_leverage(data):
    '''
    自己資本比率
    '''
    element_id = 'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults'
    context_id = 'CurrentYearInstant'
    leverage_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(leverage_row) == 0:
        return None
    leverage = leverage_row.loc[0, '値']
    try:
        leverage = float(leverage)
    except ValueError:
        leverage = -1.0
    return leverage
