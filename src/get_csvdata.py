import requests
import pandas as pd
import numpy as np
import io
import zipfile

api_key = '66b55baf5f8e4056940b872f7856db5f'

def zip_csv(zip_file):
    file_list = zip_file.namelist()
    data = pd.DataFrame({
    })
    for file_name in file_list:
        if file_name.endswith('.csv'):
            with zip_file.open(file_name) as csvfile:
                df = pd.read_csv(csvfile,
                                 encoding='utf-16',
                                 on_bad_lines='skip',
                                 sep='\t')
                data = pd.concat([data, df], ignore_index=True)
    return data

def get_csvdata(docID):
    url = f'https://api.edinet-fsa.go.jp/api/v2/documents/{docID}'
    params = {
            'type': 5,
            'Subscription-Key': api_key,
            }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        zip_file = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_file, 'r') as z:
            data = zip_csv(z)
        return (data)
    else:
        print("Error status_code : ", response.status_code)
        return (pd.DataFrame({}))

if __name__ == '__main__':
    data = get_csvdata('S10057H6')
    print(data)
