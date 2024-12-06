import pandas as pd

def calc_row_data(data, element_id, is_instant, is_stdmember):
    data = data[(data['ユニットID'] == "JPY") |
                (data['ユニットID'] == "JPYPerShares") |
                (data['ユニットID'] == "pure") |
                (data['ユニットID'] == "shares")]
    row_data = None
    if is_instant:
        if is_stdmember:
            data = data[
                    (data['コンテキストID'] == 'CurrentYearInstant')
                    ]
        else:
            data = data[(data['コンテキストID'] == 'CurrentYearInstant_NonConsolidatedMember')]
    else:
        if is_stdmember:
            data = data[
                    (data['コンテキストID'] == 'CurrentYearDuration')
                    ]
        else:
            data = data[(data['コンテキストID'] == 'CurrentYearDuration_NonConsolidatedMember')]
    row_data_row = data[
            (data['要素ID'] == element_id)
            ].reset_index(drop=True)
    if len(row_data_row) == 0:
        return None
    else:
        for i in range(len(row_data_row)):
            if (row_data_row.loc[i, '値'] == '－'):
                row_data = '-'
            else:
                row_data = row_data_row.loc[0, '値']
    return row_data

def calc_row_string_data(data, element_id, context_id):
    result = None
    data = data[
            (data['要素ID'] == element_id) &
            (data['コンテキストID'] == context_id)
            ].reset_index(drop=True)
    if len(data) == 0:
        pass
    elif len(data) == 1:
        result = data.loc[0, '値']
    else:
        # print(len(data))
        result = data.loc[0, '値']
    return result

def calc_row_data_str(data, include_str):
    row_data_row = data[
            (data['要素ID'].str.contains(include_str, na=False))
                        ].reset_index(drop=True)
    if len(row_data_row) == 0:
        return None, None
    else:
        return (row_data_row.loc[0, '値']), (row_data_row.loc[1, '値'])
