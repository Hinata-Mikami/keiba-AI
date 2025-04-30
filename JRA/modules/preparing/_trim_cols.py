import pandas as pd
import re
import numpy as np
from modules import preparing

def add_missing_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    指定されたカラムリストのうち、DataFrameに存在しないカラムを
    すべてNaNの値で初期化して追加した新しいDataFrameを返す。

    Parameters:
        df (pd.DataFrame): 元のDataFrame
        col_list (list): 追加を確認するカラム名のリスト

    Returns:
        pd.DataFrame: 必要なカラムが追加されたDataFrame
    """
    col_list =['最 高', '５走 平均', '距 離', 'コ ｜ ス', '3走', '2走', '前走', '評価.1', '枠']
    for col in col_list:
        if col not in df.columns:
            df.loc[:, col] = np.nan
    return df


    # '前course_len' の設定
def extract_course_len(course):
    if isinstance(course, str):
        match = re.search(r'[芝ダ](\d{4})', course)
        if match:
            return float(int(match.group(1)) / 100)
    return np.nan

def make_zen_type(df : pd.DataFrame) -> pd.DataFrame:
# 条件に基づいて新しい列を作成
    # df['前race_type_芝'] = df['前コース'].apply(lambda x: True if isinstance(x, str) and x.startswith('芝') else False)
    # df['前race_type_ダ'] = df['前コース'].apply(lambda x: True if isinstance(x, str) and x.startswith('ダ') else False)

    # df['前course_len'] = df['前コース'].apply(extract_course_len)
    # df = df.drop(columns=['前コース'], axis = 1)
    return df

#距離・クラス差分を表す列の追加.　その他必要な処理
def make_diffs (data : pd.DataFrame) -> pd.DataFrame:
    data.loc[:, 'type_diff_芝toダ'] = data['前race_type_芝'] & data['race_type_ダート']
    data.loc[:, 'type_diff_ダto芝'] = data['前race_type_ダ'] & data['race_type_芝']

    data.drop(columns = '前race_type_芝', axis=1)
    data.drop(columns = '前race_type_ダ', axis = 1)
    data.drop(columns = '前course_len', axis = 1)    
    
    data.loc[:, 'course_len_diff'] = data['course_len'] - data['前course_len']
    data.loc[:, 'course_len_diff'] = data['course_len_diff'].where(data['前course_len'].notna(), 0)
    data.drop(columns = '前course_len', axis = 1)
    
    # 各クラスの条件を満たす場合に対応する値を設定
    conditions = [
        data['race_class_1勝クラス'],
        data['race_class_2勝クラス'],
        data['race_class_3勝クラス'],
        data['race_class_オープン'],
        data['race_class_G3'],
        data['race_class_G2'],
        data['race_class_G1']
    ]

    choices = [1, 2, 3, 4, 5, 6, 7]

    # race_class列を作成。条件を満たさない場合は0
    data.loc[:, 'race_class'] = 0  # まず全て0に初期化
    for condition, choice in zip(conditions, choices):
        data.loc[condition, 'race_class'] = choice  # 条件を満たす場合に値を設定

    # race_class_diff列を追加
    data.loc[:, 'race_class_diff'] = data['race_class'] - data['前クラス']
    
    # # '前race_class'はOP，新馬，未勝利が全て4に。新馬，未勝利->1勝を1にする処理。
    # data.loc[~data['race_class_diff'].isin([-2, -1, 0, 1, 2]), 'race_class_diff'] = 1

    # race_class列を削除
    data = data.drop(columns=['前クラス'], axis = 1)
    
    
    data['逃げ馬'] = data['逃げ馬'].astype(bool)
    data['先行馬'] = data['先行馬'].astype(bool)
    
    
    # 辞書を作成して対応関係を定義
    mapping = {'A': 4, 'B': 3, 'C': 2, 'D': 1}

    # map()を使って評価.1を変換し、nanはそのままにする
    data['評価.1'] = data['評価.1'].map(mapping)
    
    return data
    
# 新馬戦，未勝利戦，障害戦のデータをdrop     
def drop_3_classes (data : pd.DataFrame) -> pd.DataFrame:   
    contains_mishouri = (data['race_class_未勝利'] == True) 
    contains_shimba = (data['race_class_新馬'] == True)
    contains_shogai = (data['race_class_障害'] == True)

    # 全ての条件を論理和 (OR) を使って組み合わせる
    rows_to_drop = contains_mishouri | contains_shimba | contains_shogai
    # rows_to_drop = contains_shimba | contains_shogai
    # いずれかの条件に合致する行を削除する
    data.drop(data[rows_to_drop].index, axis=0, inplace=True)    
    
    return data


def drop_cols(data : pd.DataFrame) -> pd.DataFrame:
    delete_list = ['評価.1', '体重', 'age_days', '体重変化', '前course_len', 'interval','weather_晴', 'weather_曇', 'weather_小雨', 'weather_雨', 'weather_雪', 'weather_小雪', 'race_class_新馬', 'race_class_未勝利', 'race_class_障害','around_障害', 'race_type_障害', 'ground_state_不良', 'ground_state_稍重', 'ground_state_重', 'ground_state_良', 'breeder_id', 'owner_id','着順_5R', '賞金_5R', '着差_5R', '着順_course_len_5R', '賞金_course_len_5R', '着差_course_len_5R', '着順_race_type_5R', '賞金_race_type_5R', '着差_race_type_5R', '着順_開催_5R', '賞金_開催_5R', '着差_開催_5R', '着順_9R', '賞金_9R', '着差_9R', '着順_course_len_9R', '賞金_course_len_9R', '着差_course_len_9R', '着順_race_type_9R', '賞金_race_type_9R', '着差_race_type_9R', '着順_開催_9R', '賞金_開催_9R', '着差_開催_9R', '着順_allR', '賞金_allR', '着差_allR', '着順_course_len_allR', '賞金_course_len_allR', '着差_course_len_allR', '着順_race_type_allR', '賞金_race_type_allR', '着差_race_type_allR',  '着順_開催_allR', '賞金_開催_allR', '着差_開催_allR', '頭数人気_1R', '頭数人気_2R', '頭数人気_3R', '頭数人気_4R', '頭数人気_5R', '通過順位_1R', '通過順位_2R', '通過順位_3R', '通過順位_4R', '通過順位_5R', '前race_type_芝', '前race_type_ダ', '頭数_1R', '頭数_2R', '頭数_3R', '頭数_4R', '頭数_5R', '枠', 'around_左', 'around_直線', 'around_右']
    new_dl= ['通過1C_2R', '通過1C_3R', '通過1C_4R', '通過1C_5R', 
             '通過2C_2R', '通過2C_3R', '通過2C_4R', '通過2C_5R',
             '通過3C_2R', '通過3C_3R', '通過3C_4R', '通過3C_5R',
             '通過4C_2R', '通過4C_3R', '通過4C_4R', '通過4C_5R']
    for col in (delete_list+new_dl):
        data = data.drop(columns=col, axis = 1)
        
    return data

def drop_horseid(data : pd.DataFrame) -> pd.DataFrame:
    data = data.drop(columns='horse_id')
    return data
        
        
def drop_kaisai(data : pd.DataFrame) -> pd.DataFrame:
    
    kaisai_no_use = ['30', '34', '35', '36', '42', '43', '44', '45', '46', '47', '48', '50', '51', '53', '54', '55', '56', '58', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88']

    for kaisai in kaisai_no_use:
        data = data.drop(columns=('開催_' + kaisai), axis = 1)
        
    return data


def pick_kaisai(data : pd.DataFrame, x : int) -> pd.DataFrame:
    if x == 1: s = '01'
    if x == 2: s = '02'
    if x == 3: s = '03'
    if x == 4: s = '04'
    if x == 5: s = '05'
    if x == 6: s = '06'
    if x == 7: s = '07'
    if x == 8: s = '08'
    if x == 9: s = '09'
    if x == 10: s = '10'
    
    col = '開催_' + s
    data = data[data[col] == True]
    
    kaisai_use = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

    for kaisai in kaisai_use:
        data = data.drop(columns=('開催_' + kaisai), axis = 1)
        
    return data
    
    
        
def drop_peds(data : pd.DataFrame) -> pd.DataFrame:
    for i in range(0, 62):
        n = str(i)
        data = data.drop(columns=('peds_' + n), axis = 1)
        
    return data

def drop_class(data : pd.DataFrame) -> pd.DataFrame:
    delete_list = ['race_class_1勝クラス', 'race_class_2勝クラス', 'race_class_3勝クラス', 'race_class_G1', 'race_class_G2', 'race_class_G3','race_class_オープン']
    for col in delete_list:
        data = data.drop(columns=col, axis = 1)
        
    return data

def drop_shisu(data : pd.DataFrame) -> pd.DataFrame:
    delete_list = ['up_index_3', 'up_index_4', 'up_index_5', 'pace_index_3', 'pace_index_4', 'pace_index_5', 'leading_index_3', 'leading_index_4', 'leading_index_5', 'up_index_1', 'up_index_2', 'leading_index_1', 'leading_index_2', 'pace_index_1', 'pace_index_2',  'speed_index_2', 'speed_index_3','speed_index_4','speed_index_5']

    for col in delete_list:
        data = data.drop(columns=col, axis = 1)   
        
    return data  
        
def drop_shisu_ex(data : pd.DataFrame) -> pd.DataFrame:
    delete_list = ['pace_index_max', 'leading_index_max', 'up_index_max',  'pace_index_avg', 'leading_index_avg', 'up_index_avg', '最 高', '５走 平均', '距 離', 'コ ｜ ス', '3走', '2走']

    for col in delete_list:
        data = data.drop(columns=col, axis = 1) 
        
    return data

def pick_summer(data : pd.DataFrame, b: bool) -> pd.DataFrame:
    if b:
        # 各年の07-01から10-01までのデータのみを抽出
        years = range(2010, 2025)
        query_string = ' | '.join([f'("{year}-07-01" <= date <= "{year}-10-01")' for year in years])

        # クエリを使って条件に一致する行を抽出
        data = data.query(query_string)
    else :
        # 各年の07-01から10-01までのデータをdrop
        years = range(2010, 2025)
        query_string = ' | '.join([f'("{year}-07-01" < date < "{year}-10-01")' for year in years])

        # クエリを使って条件に一致する行のインデックスを取得
        drop_index = data.query(query_string).index

        # 取得したインデックスを使って行を削除
        data.drop(drop_index, axis=0, inplace=True)
    
    return data


def turf_or_dirt (df : pd.DataFrame, b : bool) -> pd.DataFrame:
    
    if b:
       # ダートのデータをdrop
        contains_dirt = (df['race_type_ダート'] == True)
        df.drop(df[contains_dirt].index, axis=0, inplace=True)

        df.drop(columns= 'race_type_ダート', axis = 1)
        df.drop(columns= 'race_type_芝', axis = 1) 
    else :
        # 芝のデータをdrop
        contains_shiba = (df['race_type_芝'] == True)
        df.drop(df[contains_shiba].index, axis=0, inplace=True)

        df.drop(columns= 'race_type_ダート', axis = 1)
        df.drop(columns= 'race_type_芝', axis = 1)
        
    return df


def lt_me_1700 (df : pd.DataFrame, b : bool) -> pd.DataFrame:
    if b:
        # 'course_len'が17未満の行のみを抽出
        df = df[df['course_len'] < 17]
        
    else :
        df = df[df['course_len'] >= 17]
    
    return df

def drop_zen_ninki (df:pd.DataFrame) -> pd.DataFrame:
    delete_list = ['人気_1R', '人気_2R', '人気_3R', '人気_4R', '人気_5R']

    for col in delete_list:
        df = df.drop(columns=col, axis = 1) 
        
    return df

def make_avg_diffs (df:pd.DataFrame) -> pd.DataFrame:
    diffs_list = ['斤量', 
                #   'leading_index_1', 'pace_index_1', 'up_index_1', 'speed_index_1',
                #   'leading_index_2', 'pace_index_2', 'up_index_2', 'speed_index_2',
                #   'leading_index_3', 'pace_index_3', 'up_index_3', 'speed_index_3', 
                #   'leading_index_4', 'pace_index_4', 'up_index_4', 'speed_index_4', 
                #   'leading_index_5', 'pace_index_5', 'up_index_5', 'speed_index_5', 
                  'leading_index_max', 'pace_index_max', 'up_index_max', 'speed_index_max', 
                  'leading_index_avg', 'pace_index_avg', 'up_index_avg', 'speed_index_avg','speed_index_avg3',
                  '最 高', '５走 平均', '距 離', 'コ ｜ ス', '3走', '2走', '前走']
    
    df['通過1C_avg'] = df[['通過1C_1R', '通過1C_2R', '通過1C_3R', '通過1C_4R', '通過1C_5R']].replace(0, np.nan).mean(axis=1)
    df['通過2C_avg'] = df[['通過2C_1R', '通過2C_2R', '通過2C_3R', '通過2C_4R', '通過2C_5R']].replace(0, np.nan).mean(axis=1)
    df['通過3C_avg'] = df[['通過3C_1R', '通過3C_2R', '通過3C_3R', '通過3C_4R', '通過3C_5R']].replace(0, np.nan).mean(axis=1)
    df['通過4C_avg'] = df[['通過4C_1R', '通過4C_2R', '通過4C_3R', '通過4C_4R', '通過4C_5R']].replace(0, np.nan).mean(axis=1)
    
    newdiffslist = ['通過1C_avg', '通過2C_avg', '通過3C_avg', '通過4C_avg', '通過1C_1R', '通過2C_1R', '通過3C_1R', '通過4C_1R']
    for col in diffs_list + newdiffslist:
        mean_col = df.groupby('race_id')[col].transform('mean')
        df[col + "diff"] = np.where(df[col].isna(), mean_col, df[col] - mean_col)

    return df

def length_flag(df):
    """
    DataFrameの各行の'course_len'列の値を参照し、距離カテゴリを新しいカラムに追加する。
    
    条件:
        - 16未満: '短距離'カラムをTrueに
        - 16以上20未満: 'マイル'カラムをTrueに
        - 20以上25未満: '中距離'カラムをTrueに
        - 25以上: '長距離'カラムをTrueに
        - その他はFalse
    
    Args:
        df (pd.DataFrame): 'course_len'列を含むDataFrame
    
    Returns:
        pd.DataFrame: 各カテゴリカラムが追加されたDataFrame
    """
    # 各カテゴリ列をFalseで初期化
    df['短距離'] = False
    df['マイル'] = False
    df['中距離'] = False
    df['長距離'] = False

    # 条件を設定し、対応する列にTrueを割り当て
    df.loc[df['course_len'] < 16, '短距離'] = True
    df.loc[(df['course_len'] >= 16) & (df['course_len'] < 20), 'マイル'] = True
    df.loc[(df['course_len'] >= 20) & (df['course_len'] < 25), '中距離'] = True
    df.loc[df['course_len'] >= 25, '長距離'] = True

    return df

def nisai_hinba(df):
    def process_dataframe(df):
        # '2歳戦'列の値を設定
        df['2歳戦'] = df.groupby('race_id')['年齢'].transform(lambda x: (x == 2).all())

        # '牝馬限定'列の値を設定
        df['牝馬限定'] = df.groupby('race_id')['性_牝'].transform(lambda x: x.all())

        return df


    # 関数の実行
    result_df = process_dataframe(df)
    
    return result_df

def fix_object(df):

    # エラーを出している列を指定
    columns_to_fix = [
        "前回_逃げ", "前回_先行", 
        "前回_差し", "前回_追い", "前回_後方", 
        "young_jockey_only", "handicap"
    ]


    # 対象の列を`bool`型に変換
    for column in columns_to_fix:
        if column in df.columns:
            df[column] = df[column].replace({"True": True, "False": False}).astype(bool)
            
    no_use = ['前race_type_ダ','前race_type_芝', '通過順位_1R', '通過順位_2R', '通過順位_3R', '通過順位_4R', '通過順位_5R', '頭数人気_1R', '頭数人気_2R', '頭数人気_3R', '頭数人気_4R', '頭数人気_5R', '体重', '体重変化', 'weather_晴', 'weather_曇', 'weather_小雨', 'weather_雨', 'weather_雪', 'weather_小雪', 'race_class_新馬', 'race_class_未勝利', 'race_class_障害','around_障害', 'race_type_障害', 'ground_state_不良', 'ground_state_稍重', 'ground_state_重', 'ground_state_良']
    
    for col in no_use:
        df = df.drop(columns=col, axis = 1)   
            
    return df

def drop_zenso(data : pd.DataFrame) -> pd.DataFrame:
    
    data = data.drop(columns=('前走'), axis = 1)
        
    return data

def G_WIN5(df : pd.DataFrame, race_id_list : list) -> pd.DataFrame:
    """
    指定した条件を満たす行を抽出する関数。
    
    条件：
    1. 'race_class_G1' 列が True
    2. 'race_class_G2' 列が True
    3. 'race_class_G3' 列が True
    4. 'race_id' の値が race_id_list に含まれる
    
    :param df: フィルタリング対象のDataFrame
    :param race_id_list: 抽出したい 'race_id' のリスト
    :return: 条件を満たす行のみを含むDataFrame
    """
    return df[(df['race_class_G1'] | df['race_class_G2'] | df['race_class_G3']) | df['race_id'].isin(race_id_list)]

def pick_1to3wins(df : pd.DataFrame) -> pd.DataFrame:

    return df[(df['race_class_1勝クラス'] | df['race_class_2勝クラス'] | df['race_class_3勝クラス'])]
   
def pick_open(df : pd.DataFrame) -> pd.DataFrame:

    return df[df['race_class_オープン']]

          
def trim_cols(data : pd.DataFrame) -> pd.DataFrame:

    #毎回実行
    data = add_missing_columns(data)
    # data = make_zen_type(data)
    data = make_diffs(data)     
    data = drop_3_classes(data)
    
    data = drop_kaisai(data)

    #開催場所
    # 東京:5 中山:6 中京:7 京都:8 阪神:9
    # data = pick_kaisai(data, 6)

    #選択実行
    #pedsのdrop
    data = drop_peds(data)

    #classのdrop
    # data = drop_class(data)

    #pace, leading, up指数(max, avgを除く)のdrop
    # data = drop_shisu(data)

    #True・・・夏競馬用，False・・・通常期間用
    # data = pick_summer(data, False)

    #True・・・芝用，False・・・ダート用
    # data = turf_or_dirt(data, False)

    #True・・・~1600m, False・・・1700m~
    # data = lt_me_1700(data, True)
    data = make_avg_diffs(data)
    data = length_flag(data)
    data = nisai_hinba(data)
    # data = drop_cols(data)
    data = fix_object(data)
    
    return data

def adjust_cols(data):
    data = add_missing_columns(data)

    data = make_diffs(data)     
    data = drop_3_classes(data)

    data = drop_kaisai(data)

    data = drop_peds(data)

    data = make_avg_diffs(data)

    # data = drop_zen_ninki(data)
    data = length_flag(data)
    data = nisai_hinba(data)

    data = fix_object(data)
    
    tmp = preparing.scrape_info_of_start(data)
    data = data.merge(tmp, on=['race_id', '馬番'], how='left')
    
    data = data.set_index('race_id')
    data = preparing.drop_horseid(data)
    
    return data
    
    