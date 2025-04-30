import numpy as np
import pandas as pd



# 新しい列を追加するための関数を定義
def extract_course_info(course):
    
    # courseが文字列でない場合は文字列に変換
    if not isinstance(course, str):
        course = str(course)

    race_type_shiba = '芝' in course
    race_type_dirt = 'ダ' in course
    # コースの長さを数値部分から抽出し、100で割る   
    # courseから数字を抽出
    digits = ''.join(filter(str.isdigit, course))
    
    # 数字が抽出できなかった場合の処理
    if digits:
        course_len = float(digits) / 100
    else:
        course_len = None  # もしくは適切なデフォルト値
        
    return race_type_shiba, race_type_dirt, course_len



def map_race_rank(race):
    race = str(race)
    if race.startswith('500'):
        return 1
    elif race.startswith('1000'):
        return 2
    elif race.startswith('1600'):
        return 3
    elif race.endswith('オープン'):
        return 4
    elif race.endswith('GIII'):
        return 5
    elif race.endswith('GII'):
        return 6
    elif race.endswith('GI'):
        return 7
    else:
        return 0

def trim_zenso(df : pd.DataFrame) -> pd.DataFrame:
    # 新しい列を適用して作成
    df['前クラス'] = df['前クラス'].astype(str)
    df['前クラス'] = df['前クラス'].apply(map_race_rank)
    df['前race_type_芝'], df['前race_type_ダ'], df['前course_len'] = zip(*df['前コース'].apply(extract_course_info))
    df = df.drop(columns=['前コース'], axis = 1)
    
    return df