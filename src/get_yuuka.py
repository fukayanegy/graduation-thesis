import requests
import pandas as pd
import numpy as np
import io
import zipfile

api_key = '66b55baf5f8e4056940b872f7856db5f'

def get_pdf_docs(docID):
    url = f'https://api.edinet-fsa.go.jp/api/v2/documents/{docID}'
    params = {
            'type': 2,
            'Subscription-Key': api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        with open(f"{docID}.pdf", "wb") as file:
            file.write(response.content)
        print('sucsess to pdf')
    else:
        print("Error status_code : ", response.status_code)
        return (None)

def zip_csv(z, filerName):
    file_list = z.namelist()
    data = pd.DataFrame({
        "要素ID": [filerName],
        "項目名": [0],
        "コンテキストID": [0],
        "相対年度": [0],
        "連結・個別": [0],
        "期間・時点": [0],
        "ユニットID": [0],
        "単位": [0],
        "値": [0],
    })

    for file_name in file_list:
        if file_name.endswith('.csv'):
            with z.open(file_name) as csvfile:
                df = pd.read_csv(csvfile,
                                 encoding='utf-16',
                                 on_bad_lines='skip',
                                 sep='\t')
                data = pd.concat([data, df], ignore_index=True)
    return data

def get_csv_docs(docID, filerName):
    url = f'https://api.edinet-fsa.go.jp/api/v2/documents/{docID}'
    dummy_data = pd.DataFrame({
        "要素ID": [0],
        "項目名": [0],
        "コンテキストID": [0],
        "相対年度": [0],
        "連結・個別": [0],
        "期間・時点": [0],
        "ユニットID": [0],
        "単位": [0],
        "値": [0],
    })
    params = {
            'type': 5,
            'Subscription-Key': api_key,
            }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        zip_file = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_file, 'r') as z:
            data = zip_csv(z, filerName)
        return (data)
    else:
        print("Error status_code : ", response.status_code)
        return (dummy_data)

def get_comp_data(date):
    url = 'https://disclosure.edinet-fsa.go.jp/api/v2/documents.json'
    params = {
            'date': date,
            'type': 2,
            'Subscription-Key': api_key,
            }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_doclist(date, is_pdf):
    result = pd.DataFrame({
        "seqNumber"             : [0],
        "docID"                 : [0],
        "edinetCode"            : [0],
        "": [0],
        "": [0],
    })
    data = get_comp_data(date)
    for i in range(len(data['results'])):
        ratio_of_female_mg = None
        net_sales = None
        if (data['results'][i]['fundCode'] == None
            and data['results'][i]['docTypeCode'] == '120'):
            if is_pdf:
                if (data['results'][i]['pdfFlag'] == '1'):
                    pdf = get_pdf_docs(data['results'][i]['docID'])
            else:
                if (data['results'][i]['csvFlag'] == '1'):
                    csv_data = get_csv_docs(data['results'][i]['docID'],
                                            data['results'][i]['filerName'])
                    women_data = csv_data[csv_data["項目名"].str.contains("管理職に占める女性労働者の割合", na=False)]
                    women_data.loc[:, '値'] = pd.to_numeric(women_data['値'], errors='coerce')
                    net_sales_data = csv_data[(csv_data["要素ID"] == 'jppfs_cor:NetSales') & (csv_data['コンテキストID'] == 'CurrentYearDuration_NonConsolidatedMember')]
                    net_sales_data.loc[:, '値'] = pd.to_numeric(net_sales_data['値'], errors='coerce')
                    if len(women_data != 0):
                        women_data = women_data.replace('-', np.nan)
                        ratio_of_female_mg = women_data['値'].mean()
                    if len(net_sales_data) != 0:
                        net_sales_data = net_sales_data.replace('-', np.nan)
                        net_sales = net_sales_data['値'].mean()
        if isinstance(ratio_of_female_mg, (int, float)) and isinstance(net_sales, (int, float)):
            new_row = {'Name': data['results'][i]['filerName'],
                       'ratio_of_female_mg': ratio_of_female_mg,
                       'net_sales': net_sales,
                       }
            result.loc[len(result)] = new_row
    return result

if __name__ == '__main__':
    df = pd.read_pickle('data/docID_data.pickle')
    date_level = df.index.get_level_values('date')
    secCode_level = df.index.get_level_values('secCode')
    print(df)
    # get_csv_docs()
    # for i in range(3):
    #     if (int(date_level[i][:4]) == 2015):
    #         continue
    #     data, data_name = get_doclist(i, 'hoge')
    #     # data.to_pickle(f'database/{data_name}.pickle')
    #     print(f'{i} : database/{data_name}.pickle')
