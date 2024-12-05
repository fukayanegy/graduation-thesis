import requests
import pandas as pd
import urllib.request
import urllib.error
import sys
import os
import zipfile
import json
# import chardet

# APIのエンドポイント
url = 'https://disclosure.edinet-fsa.go.jp/api/v2/documents.json'

api_key = '66b55baf5f8e4056940b872f7856db5f'

def get_docid(day):
    params = {
        'date': day,
        'type': 2,
        "Subscription-Key": api_key
    }

    # APIリクエストを送信
    response = requests.get(url, params=params)

    # レスポンスのJSONデータを取得
    data = response.json()

    if data['metadata']['status'] == '404':
        return pd.DataFrame()

    # データフレームに変換
    documents = data['results']
    df = pd.DataFrame(documents)

    if df.empty:
        return pd.DataFrame()

    df = df[(df['docTypeCode'] == '120') & (df['fundCode'].isnull())].reset_index(drop=True)
    df = (df[['docID', 'secCode', 'csvFlag']])

    return df
