import numpy as np
import pandas as pd
import re

def add_max_and_avg(df : pd.DataFrame) -> pd.DataFrame:
    collist = ['leading_index_1', 'pace_index_1', 'up_index_1', 'speed_index_1', 'leading_index_2', 'pace_index_2', 'up_index_2', 'speed_index_2', 'leading_index_3', 'pace_index_3', 'up_index_3', 'speed_index_3', 'leading_index_4', 'pace_index_4', 'up_index_4', 'speed_index_4', 'leading_index_5', 'pace_index_5', 'up_index_5', 'speed_index_5']
    
    for col in collist:
        df[col] = df[col].astype(float)

# 各列の最大値を計算して追加
    df['leading_index_max'] = df[['leading_index_1', 'leading_index_2', 'leading_index_3', 'leading_index_4', 'leading_index_5']].max(axis=1)
    df['pace_index_max'] = df[['pace_index_1', 'pace_index_2', 'pace_index_3', 'pace_index_4', 'pace_index_5']].max(axis=1)
    df['up_index_max'] = df[['up_index_1', 'up_index_2', 'up_index_3', 'up_index_4', 'up_index_5']].max(axis=1)
    df['speed_index_max'] = df[['speed_index_1', 'speed_index_2', 'speed_index_3', 'speed_index_4', 'speed_index_5']].max(axis=1)

    # 0を除いたものの平均を計算して追加
    df['leading_index_avg'] = df[['leading_index_1', 'leading_index_2', 'leading_index_3', 'leading_index_4', 'leading_index_5']].replace(0, np.nan).mean(axis=1)
    df['pace_index_avg'] = df[['pace_index_1', 'pace_index_2', 'pace_index_3', 'pace_index_4', 'pace_index_5']].replace(0, np.nan).mean(axis=1)
    df['up_index_avg'] = df[['up_index_1', 'up_index_2', 'up_index_3', 'up_index_4', 'up_index_5']].replace(0, np.nan).mean(axis=1)
    df['speed_index_avg'] = df[['speed_index_1', 'speed_index_2', 'speed_index_3', 'speed_index_4', 'speed_index_5']].replace(0, np.nan).mean(axis=1)
    df['speed_index_avg3'] = df[['speed_index_1', 'speed_index_2', 'speed_index_3']].replace(0, np.nan).mean(axis=1)
    
    return df

def create_kyakushitsu_ratio_columns(df, column_name='脚質'):
    # '脚質'カラムを文字列型に変換
    df[column_name] = df[column_name].astype(str)
    
    # 空文字列を '00' に置き換え、不正なデータを0にする
    df[column_name] = df[column_name].apply(lambda x: x.zfill(8) if x.isdigit() and len(x) <= 8 else '00000000')
    
    # 各脚質の回数を取得
    df['脚質_逃げ'] = df[column_name].str[0:2].astype(int)
    df['脚質_先行'] = df[column_name].str[2:4].astype(int)
    df['脚質_差し'] = df[column_name].str[4:6].astype(int)
    df['脚質_追い'] = df[column_name].str[6:8].astype(int)
    
    # 合計を計算
    total = df[['脚質_逃げ', '脚質_先行', '脚質_差し', '脚質_追い']].sum(axis=1)
    
    # 割合を計算して各カラムに格納
    df['脚質_逃げ'] = df['脚質_逃げ'] / total
    df['脚質_先行'] = df['脚質_先行'] / total
    df['脚質_差し'] = df['脚質_差し'] / total
    df['脚質_追い'] = df['脚質_追い'] / total
    
    # 新しいカラム'逃げ馬'と'先行馬'を追加
    df['逃げ馬'] = (df['脚質_逃げ'] > df[['脚質_先行', '脚質_差し', '脚質_追い']].max(axis=1))
    df['先行馬'] = (df['脚質_先行'] > df[['脚質_逃げ', '脚質_差し', '脚質_追い']].max(axis=1))
    
    # totalが0の場合はNaNにしておく
    df.replace([float('inf'), -float('inf')], float('nan'), inplace=True)
    
    # '脚質'カラムを削除
    df.drop(columns=[column_name], inplace=True)
    
    return df

def extract_heads_and_popularity(df, heads_col, pop_col, column_name):
    df[column_name] = df[column_name].fillna('').astype(str)

    def extract_head_pop(x):
        if 'ﾄ' in x and '番' in x:
            parts = x.split('ﾄ')
            head_str = parts[0]
            remaining = parts[1]
            pop_str = remaining.split('番')[-1]

            head_digits = ''.join([c for c in head_str if c.isdigit()])
            pop_digits = ''.join([c for c in pop_str if c.isdigit()])

            head = int(head_digits) if head_digits else 0
            pop = int(pop_digits) if pop_digits else 0

            return (head, pop)
        else:
            # 既存のカラムが存在する場合は、それを使用する
            return (None, None)

    # 頭数と人気を抽出してそれぞれのカラムに割り当て
    df[[heads_col, pop_col]] = df[column_name].apply(lambda x: pd.Series(extract_head_pop(x)))

    # Noneの値は既存のカラムの値で置き換え
    df[heads_col].fillna(df[heads_col], inplace=True)
    df[pop_col].fillna(df[pop_col], inplace=True)

    return df

def process_race_data(df, s):
    # カラム名を生成
    heads_col = f'頭数_'+s+'R'
    pop_col = f'人気_'+s+'R'
    passage_cols = [f'通過{i}C_'+s+'R' for i in range(1, 5)]

    # 頭数と人気を抽出して対応するカラムに格納
    df = extract_heads_and_popularity(df, heads_col, pop_col, '頭数人気_'+s+'R')

    # 人気を頭数で割った割合を計算して保存
    def calc_pop_ratio(row):
        if row[heads_col] is not None and row[pop_col] is not None:
            if row[heads_col] != 0:
                return row[pop_col] / row[heads_col]
            else:
                return row[pop_col]
        else:
            return None

    df[pop_col] = df.apply(calc_pop_ratio, axis=1)
    df[pop_col] = df[pop_col].astype(float)
    df[heads_col] = df[heads_col].astype(float)

    # '通過順位_XR'を文字列型に変換し、不正なデータを修正
    df['通過順位_'+s+'R'] = df['通過順位_'+s+'R'].fillna('').astype(str)
    df['通過順位_'+s+'R'] = df['通過順位_'+s+'R'].apply(lambda x: x if x.isdigit() and len(x) == 8 else '00000000')

    # '通過順位_XR'から'通過1C_XR', '通過2C_XR', '通過3C_XR', '通過4C_XR'を作成
    for i, col in enumerate(passage_cols):
        df[col] = df.apply(
            lambda row: int(row['通過順位_'+s+'R'][2*i:2*i+2]) / row[heads_col]
            if row[heads_col] and row[heads_col] != 0 else np.nan,  # Noneや0を避ける
            axis=1
        )

    return df



def trim_shisu(df : pd.DataFrame) -> pd.DataFrame:
    
    df = add_max_and_avg(df)
    df = create_kyakushitsu_ratio_columns(df)
    
    for s in ['1', '2', '3', '4', '5']:
        df = process_race_data(df, s)
        
    df['前回_逃げ'] = df['前回脚質'].str.contains('逃', na=False)
    df['前回_先行'] = df['前回脚質'].str.contains('先', na=False)
    df['前回_差し'] = df['前回脚質'].str.contains('差', na=False)
    df['前回_追い'] = df['前回脚質'].str.contains('追', na=False)
    df['前回_後方'] = df['前回脚質'].str.contains('後', na=False)
    
    # '脚質'カラムを削除
    df.drop(columns=['前回脚質'], inplace=True)
    
    return df