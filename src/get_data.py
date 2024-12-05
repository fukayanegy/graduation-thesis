import pandas as pd

def make_data():
    data = pd.read_pickle('data/docID_data.pickle')
    board_data = pd.read_pickle('test_data/test5.pickle')
    board_data = board_data[['men_board_num', 'women_board_num', 'women_board_ratio']]
    data_hoge = pd.read_pickle('test_data/test4.pickle')
    ns_final = pd.read_pickle('data/final_data.pickle')
    data['year'] = data_hoge['year']
    data_1 = pd.read_pickle('data/売上高.pickle')
    # data_2 = pd.read_pickle('data/当期純利益.pickle')
    data_3 = pd.read_pickle('data/研究開発費.pickle')
    data_4 = pd.read_pickle('data/純資産額.pickle')
    data_5 = pd.read_pickle('data/経常利益.pickle')
    data_6 = pd.read_pickle('data/総資産額.pickle')
    data_7 = pd.read_pickle('data/自己資本比率.pickle')
    data_8 = pd.read_pickle('data/ROE.pickle')
    data_1['year'] = data['year']
    data_1 = data_1[~data_1['year'].isna()]
    data = data[~data['year'].isna()]
    data_1['result'] = data_1['ns_br_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['ns_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['ns']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['revenue_ifrs_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['gp_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['r_excus']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['r_excus_total']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['経常収益_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['経常収益_br_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['経常収益']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['経常収益_br']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上収益IFRS_br_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上収益IFRS_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上収益IFRS_br']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上収益IFRS']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上高US_GAAP_br_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上高US_GAAP_nc']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上高US_GAAP_br']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['売上高US_GAAP']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['経常収益_保険業']
    data_1.loc[data_1['result'].isna(), 'result'] = data_1['経常収益_保険業_nc']
    data['売上高'] = data_1['result']
    data.loc[data['売上高'] == '－', '売上高'] = np.nan
    data.loc[~data['売上高'].isna(), '売上高'] = data.loc[~data['売上高'].isna(), '売上高'].astype(int)
    data['売上高'] = data['売上高'].infer_objects()
    data['売上高'] = data['売上高'].fillna(data['売上高'].mean())

    data_3['result'] = data_3['RandD']
    data['研究開発費'] = data_3['result']
    data['研究開発費_dummy'] = np.where(
        (data['研究開発費'].isna()) | (data['研究開発費'] == 0) | (data['研究開発費'] == -1),
        0,  # 条件を満たす場合
        1   # 条件を満たさない場合
    )
    data.loc[data['研究開発費_dummy'] == 0, '研究開発費'] = np.nan
    data.loc[data['研究開発費'] == '－', '研究開発費'] = np.nan
    data.loc[~data['研究開発費'].isna(), '研究開発費'] = data.loc[~data['研究開発費'].isna(), '研究開発費'].astype(int)
    data['研究開発費'] = data['研究開発費'].infer_objects()
    data['研究開発費'] = data['研究開発費'].fillna(0)

    data['純資産額'] = data_4['na_br_nc']
    data['経常利益'] = data_5['oi_nc']
    data['総資産額'] = data_6['ta_br_nc']
    data['自己資本比率'] = data_7['etar_br_nc']
    data['ROE'] = data_8['roe_br_nc']
    data.loc[data['ROE'] == '－', 'ROE'] = np.nan
    data.loc[~data['ROE'].isna(), 'ROE'] = data.loc[~data['ROE'].isna(), 'ROE'].astype(float)
    data['ROE'] = data['ROE'].infer_objects()
    data['ROE'] = data['ROE'].fillna(data['ROE'].mean())
    data['男性取締役人数'] = board_data['men_board_num']
    data['女性取締役人数'] = board_data['women_board_num']
    data['女性取締役割合'] = board_data['women_board_ratio']
    data = data.reset_index()
    data = data.drop(['33業種区分', '17業種区分', '規模区分', 'csvFlag', 'date'], axis=1)
    print(data)
    data.to_csv('data/final_data.csv')
