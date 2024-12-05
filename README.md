## data
### industoyr

    industry_dict = {
            "水産・農林業"      : 50,
            "鉱業"              : 1050,
            "建設業"            : 2050,
            "食料品"            : 3050,
            "繊維製品"          : 3100,
            "パルプ・紙"        : 3150,
            "化学"              : 3200,
            "医薬品"            : 3250,
            "石油・石炭製品"    : 3300,
            "ゴム製品"          : 3350,
            "ガラス・土石製品"  : 3400,
            "鉄鋼"              : 3450,
            "非鉄金属"          : 3500,
            "金属製品"          : 3550,
            "機械"              : 3600,
            "電気機器"          : 3650,
            "輸送用機器"        : 3700,
            "精密機器"          : 3750,
            "その他製品"        : 3800,
            "電気・ガス業" : 4050,
            "陸運業" : 5050,
            "海運業" : 5100,
            "空運業" : 5150,
            "倉庫・運輸関連" : 5200,
            "情報・通信業" : 5250,
            "卸売業" : 6050,
            "小売業" : 6100,
            "銀行業" : 7050,
            "証券、商品先物取引業" : 7100,
            "保険業" : 7150,
            "その他金融業" : 7200,
            "不動産業" : 8050,
            "サービス業" : 9050,
            }


### 
def get_yuuka(i, name):
    docid_data = pd.read_pickle('data/docID_data.pickle')
    date_level = docid_data.index.get_level_values('date')
    result = get_csv_docs(docid_data.iloc[i]['docID'], docid_data.iloc[i]['銘柄名'])

    result.to_excel(f'data/{name}_{date_level[i][:4]}.xlsx')

    result1 = result[(result['要素ID'] == 'jpcrp_cor:NumberOfMaleDirectorsAndOtherOfficers')][['要素ID', '項目名','値']].reset_index(drop=True)
    result2 = result[(result['要素ID'] == 'jpcrp_cor:NumberOfFemaleDirectorsAndOtherOfficers')][['要素ID', '項目名','値']].reset_index(drop=True)
    result3 = result[(result['要素ID'] == 'jpcrp_cor:NumberOfFemaleDirectorsAndOtherOfficers')][['要素ID', '項目名','値']].reset_index(drop=True)
    if len(result1) != 0:
        try:
            men_board_num = int(zenkaku_to_hankaku(result1['値'].iloc[0]))
        except ValueError:
            men_board_num = 0

        try:
            women_board_num = int(zenkaku_to_hankaku(result2['値'].iloc[0]))
        except ValueError:
            women_board_num = 0
        board_num = men_board_num + women_board_num

        try:
            ratio = float(zenkaku_to_hankaku(result3['値'].iloc[0]))
        except ValueError:
            ratio = 0.0

        return board_num, men_board_num, women_board_num, ratio

    if (int(date_level[i][:4]) < 2019):
        result.to_excel(f'data/{name}_{date_level[i][:4]}.xlsx')
        return 11, 10, 1, 1/11
        result1 = (result[(result['項目名'].str.contains('役員の状況', na=False))][['要素ID', '項目名','値']].reset_index(drop=True))
        result2 = search_str(result1['値'].iloc[0][:50])
        return result2
    else:
        result.to_excel(f'data/{name}_{date_level[i][:4]}.xlsx')
        return 11, 10, 1, 1/11
        result1 = result[(result['要素ID'] == 'jpcrp_cor:InformationAboutOfficersTextBlock')][['要素ID', '項目名','値']].reset_index(drop=True)
        if len(result1) != 0:
            result2 = search_str(result1['値'].iloc[0])
            return result2
    return -2, -2, -2, -2
