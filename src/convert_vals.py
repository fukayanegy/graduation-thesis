import pandas as pd

def convert_int(value):
    try:
        return int(value)
    except ValueError:
        return None

def convert_vals(data, column_name, value_type):
    data[column_name] = data[column_name].replace('－', None)
    data[column_name] = data[column_name].replace('-', None)
    data.loc[(~data[column_name].isna()), column_name] = data.loc[(~data[column_name].isna()), column_name].astype(value_type)
    return data
