import pandas as pd
import re
from src import calc_utils
# import calc_utils

'''
2557    S10077SF    ソリトンシステムズ      2016    男7, 女2, 比率22.2%
10190   S1009Y08    オプテックスグループ    2017    男9, 女0, 比率00.0%
11793   S100DHU4    オーバル                2018    男6, 女0, 比率00.0%

result.loc[2557 , 'male_num'] = 7
result.loc[10190, 'male_num'] = 9
result.loc[11793, 'male_num'] = 6
result.loc[2557 , 'female_num'] = 2
result.loc[10190, 'female_num'] = 0
result.loc[11793, 'female_num'] = 0
'''

def zenkaku_to_hankaku(text):
    zenkaku_to_hankaku_table = str.maketrans('０１２３４５６７８９　－―─-‐（）％、', '0123456789 00000()% ')
    result = text.translate(zenkaku_to_hankaku_table)
    result = re.sub(r'\s+', ' ', result)
    return result

def extract_directors_info(data):
    pattern = r"男性\s*(\d+)\s*名\s*女性\s*(\d+)\s*名.*比率\s*(\d+(?:\.\d+)?)\s*%"
    result = re.search(pattern, data)
    if result:
        male = result.group(1)
        female = result.group(2)
        ratio = result.group(3)
        return male, female, ratio

    pattern = r"男性\s*(\d+)\s*名\s*女性\s*(\d+).*比率\s*(\d+(?:\.\d+)?)"
    result = re.search(pattern, data)
    if result:
        male = result.group(1)
        female = result.group(2)
        ratio = result.group(3)
        return male, female, ratio

    pattern = r"男性\s*(\d+)\s*名\s*女性\s*(\d+)\s*名"
    result = re.search(pattern, data)
    if result:
        male = result.group(1)
        female = result.group(2)
        return male, female, None
    return None, None, None

def get_directors_info(row, data):
    ele_id1 = 'jpcrp_cor:NumberOfMaleDirectorsAndOtherOfficers'
    ele_id2 = 'jpcrp_cor:NumberOfFemaleDirectorsAndOtherOfficers'
    ele_id3 = 'jpcrp_cor:RatioOfFemaleDirectorsAndOtherOfficers'
    ele_id4 = 'jpcrp_cor:InformationAboutOfficersTextBlock'
    context_id = 'FilingDateInstant'

    row['役員のうち男性の人数'] = calc_utils.calc_row_string_data(data, ele_id1, context_id)
    row['役員のうち女性の人数'] = calc_utils.calc_row_string_data(data, ele_id2, context_id)
    row['役員のうち女性の割合'] = calc_utils.calc_row_string_data(data, ele_id3, context_id)
    if row['役員のうち女性の人数'] == '－':
        row['役員のうち女性の人数'] = 0
        row['役員のうち女性の割合'] = 0.0
    if (calc_utils.calc_row_string_data(data, ele_id2, context_id) == None) or (calc_utils.calc_row_string_data(data, ele_id1, context_id) == None):
        text_data = calc_utils.calc_row_string_data(data, ele_id4, context_id)
        text_data = zenkaku_to_hankaku(text_data)
        row['役員のうち男性の人数'], row['役員のうち女性の人数'], row['役員のうち女性の割合'] = extract_directors_info(text_data)
    return row

if __name__ == '__main__':
    # text = ' ５ 【役員の状況】男性16名　女性 -名　（役員のうち女性の比率 -％）(１) 取締役の状況役名職名氏名生年月日略歴任期所有株式数（千株）'
    # text = '５【役員の状況】男性　11名　女性　‐名　　（役員のうち女性の比率　‐％）役名職名氏名生年月日略歴任期所有株式数（千株）'
    # text = '５ 【役員の状況】男性11名　女性０名（役員のうち女性の比率は０％）役名職名氏名生年月日略歴任期所有株式数(千株)'
    text = '５【役員の状況】男性名７名　女性２名　（役員のうち女性の比率22.2％）役名職名氏名生年月日略歴任期所有株式数（百株）'
    text = zenkaku_to_hankaku(text)
    print(text)
    print(extract_directors_info(text))
