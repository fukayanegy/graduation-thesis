import pandas as pd

def male(data):
    element_id = 'jpcrp_cor:NumberOfMaleDirectorsAndOtherOfficers'
    context_id = 'FilingDateInstant'
    rAndD_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(rAndD_row) == 0:
        return None
    rAndD = rAndD_row.loc[0, '値']
    try:
        rAndD = int(rAndD)
    except ValueError:
        rAndD = 0
    return rAndD

def female(data):
    element_id = 'jpcrp_cor:NumberOfFemaleDirectorsAndOtherOfficers'
    context_id = 'FilingDateInstant'
    rAndD_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(rAndD_row) == 0:
        return None
    rAndD = rAndD_row.loc[0, '値']
    try:
        rAndD = int(rAndD)
    except ValueError:
        rAndD = 0
    return rAndD

def female_rete(data):
    element_id = 'jpcrp_cor:RatioOfFemaleDirectorsAndOtherOfficers'
    context_id = 'FilingDateInstant'
    rAndD_row = data[(data['要素ID'] == element_id) & (data['コンテキストID'] == context_id)].reset_index(drop=True)
    if len(rAndD_row) == 0:
        return None
    rAndD = rAndD_row.loc[0, '値']
    try:
        rAndD = float(rAndD)
    except ValueError:
        rAndD = 0
    return rAndD
