import requests
import pandas as pd
import numpy as np
import io
import zipfile

api_key = '66b55baf5f8e4056940b872f7856db5f'
docID_URL = 'https://disclosure.edinet-fsa.go.jp/api/v2/documents.json'

def get_all_data(date):
    params = {
            'date': date,
            'type': 2,
            'Subscription-Key': api_key,
            }
    response = requests.get(docID_URL, params=params)
    data = response.json()
    return data

def get_docid_list(date, result):
    all_data = get_all_data(date)
    for i in range(len(all_data['results'])):
        if (all_data['results'][i]['fundCode'] == None and
            all_data['results'][i]['docTypeCode'] == '120'):
            new_row = pd.DataFrame({
                'date'      : date,
                'year'      : date[:4],
                'docID'     : [all_data['results'][i]['docID']],
                'secCode'   : [all_data['results'][i]['secCode']],
                'filerName' : [all_data['results'][i]['filerName']],
                })
            result = pd.concat([result, new_row], ignore_index=True)
    return result

if __name__ == '__main__':
    result = pd.DataFrame({})
    data = get_docid_list('2023-06-27', result)
    print(data)
