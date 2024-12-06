import pandas as pd
import os

def download_excel(docID):
    list1 = os.listdir('database')
    list2 = os.listdir('database2')
    if f'{docID}.pickle' in list1:
        data = pd.read_pickle(f'database/{docID}.pickle')
    elif f'{docID}.pickle' in list2:
        data = pd.read_pickle(f'database2/{docID}.pickle')
    data.to_excel(f'/mnt/c/WSLTMPDIR/{docID}.xlsx', index=False)
