'''
# 自己資本比率
### 取得する期間
- CurrentYearDuration

### 取得するデータ
- 自己資本比率、経営指標等      (jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults)
- 自己資本比率                  ()
'''

import pandas as pd
from src import calc_utils

def calc_equity_to_asset_ratio(row, data):
    ele_id1 = 'jpcrp_cor:EquityToAssetRatioSummary'
    ele_id2 = 'jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults'
    row['自己資本比率'] = calc_utils.calc_row_data(data, ele_id1, False, True)
    row['自己資本比率_nc'] = calc_utils.calc_row_data(data, ele_id1, False, False)
    row['自己資本比率_br'] = calc_utils.calc_row_data(data, ele_id2, False, True)
    row['自己資本比率_br_nc'] = calc_utils.calc_row_data(data, ele_id2, False, False)
    return row
