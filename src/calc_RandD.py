import pandas as pd
import re

japanese_number_map = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '百': 100, '千': 1000, '万': 10_000, '億': 100_000_000
}

def j_to_n(japanese_number):
    units = {
        "兆": 10**12,
        "億": 10**8,
        "万": 10**4,
        "千": 10**3,
        "百万": 10**6,
    }
    
    result = 0
    temp_number = 0

    pattern = r"(\d+)([兆億百万千万]*)"
    matches = re.findall(pattern, japanese_number)

    for match in matches:
        number, unit = match
        number = int(number)
        
        if unit in units:
            result += number * units[unit]
        else:
            temp_number += number

    return result + temp_number

def japanese_to_number(text):
    number = 0
    temp = 0
    unit = 1
    for char in reversed(text):
        if char in japanese_number_map:
            if japanese_number_map[char] >= 10:
                unit = japanese_number_map[char]
                if temp == 0:
                    temp = 1
            else:
                temp = japanese_number_map[char]
        else:
            number += temp * unit
            temp = 0
            unit = 1
    number += temp * unit
    return number

def convert_amount_to_number(amount):
    amount = amount.replace(',', '')
    match = re.match(r'(\d+)?(億)?(\d+)?(百万|千|万)?円', amount)
    if not match:
        return None
    number = 0

    if match.group(1):
        number += int(match.group(1)) * 100_000_000 if match.group(2) else int(match.group(1))

    if match.group(3):
        multiplier = {'百万': 1_000_000, '千': 1_000, '万': 10_000}.get(match.group(4), 1)
        number += int(match.group(3)) * multiplier

    elif re.search(r'[一二三四五六七八九十百千万億]', amount):
        number = japanese_to_number(amount.replace('円', ''))
    return number

def zenkaku_to_hankaku(text):
    zenkaku_to_hankaku_table = str.maketrans('０１２３４５６７８９　－―（）', '0123456789 00()')
    return text.translate(zenkaku_to_hankaku_table)

def search_str(text):
    pattern01 = r'該当事項はありません。'
    match01 = re.search(pattern01, text)
    pattern02 = r'特記すべき事項はありません。'
    match02 = re.search(pattern02, text)

    if match01:
        return True
    elif match02:
        return True
    else:
        return False

def search_yen(text):
    text = zenkaku_to_hankaku(text)
    pattern01 = r'(\d{1,3}(,\d{3})*|[一二三四五六七八九十百千万億]+)(億)?(\d{1,3}(,\d{3})*|[一二三四五六七八九十百千万]+)?(百万|千)?円'
    matches = re.finditer(pattern01, text)
    amounts = [match.group(0) for match in matches]
    result = [j_to_n(amount) for amount in amounts]
    if len(result) == 0:
        return None
    return max(result)

def calc_RandD(row):
    '''
    研究開発費
    '''
    text_block_2 = '一般管理費及び当期製造費用に含まれる研究開発費 [テキストブロック]'
    if row['研究開発費、研究開発活動'] != None:
        row['RandD'] = row['研究開発費、研究開発活動']
        row['RandD_bool'] = True
    elif row['研究開発費、販売費及び一般管理費'] != None:
        row['RandD'] = row['研究開発費、販売費及び一般管理費']
        row['RandD_bool'] = True
    elif row['研究開発活動 [テキストブロック]']:
        row['RandD'] = search_yen(row['研究開発活動 [テキストブロック]'])
        if row['RandD'] == None:
            row['RandD_bool'] = False
        else:
            row['RandD_bool'] = True
    elif row[text_block_2] != None:
        if search_str(row[text_block_2]):
            row['RandD'] = 0
            row['RandD_bool'] = False
        else:
            row['RandD'] = search_yen(row['研究開発活動 [テキストブロック]'])
            row['RandD_bool'] = True
            if row['RandD'] == None:
                row['RandD'] = 0
                row['RandD_bool'] = False
    else:
        row['RandD'] = 0
        row['RandD_bool'] = False
    return row
