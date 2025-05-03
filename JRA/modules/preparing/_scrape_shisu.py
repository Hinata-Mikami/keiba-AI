import os
import time
from tqdm.notebook import tqdm
import requests
import pandas as pd
import bs4
import re  # ここを追加
from modules.constants import LocalPaths


class LoopSleeper:
    def __init__(self):
        self._t = 0

    def sleep(self, sleeptime: float) -> None:
        """前回実行時の時間を記憶し、その差から実際にsleepする時間を決定しsleepする。

        Example
        ----------
        loop_sleep(1)  # 初回は0秒sleep
        ↓
        何らかの処理  # 0.2秒経過
        ↓
        loop_sleep(1)  # (1 - 0.2 =) 0.8秒sleep
        ↓
        何らかの処理  # 2秒経過
        ↓
        loop_sleep(1)  # 引数でmax1秒に指定しているので0秒sleep

        Parameters
        ----------
        sleeptime : float
            sleepしたい時間(秒)
        """
        if sleeptime < 0:
            raise ValueError('sleeptimeは0以上の値を指定してください。')
        now = time.time()
        elapased_t = now - self._t
        # additional_t: 0 ~ sleeptime(sec)
        additional_t = min(max(0, sleeptime-elapased_t), sleeptime)
        time.sleep(additional_t)
        self._t = now + additional_t

# 必ずループ外でインスタンス化（クラス定義の直下でインスタンスも定義しておくと良い）
loop_sleeper = LoopSleeper()

def scrape_from_jiro8(race_id: str) -> str:
    loop_sleeper.sleep(0.5)
    res = requests.get('http://jiro8.sakura.ne.jp/index.php?code=' + race_id)

    res.encoding = 'Shift_JIS'
    return res.text

def extract_index_info(html: str, race_id: str) -> pd.DataFrame:
    try:
        df1 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[32:36]
        df2 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[48:52]
        df3 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[64:68]
        df4 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[80:84]
        df5 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[96:100]
        df6 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[101:102]
        df7 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[26:27]
        df8 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[29:30]
        df9 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[42:43]
        df10 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[45:46]
        df11 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[58:59]
        df12 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[61:62]
        df13 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[74:75]
        df14 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[77:78]
        df15 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[90:91]
        df16 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[93:94]
        df17 = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[28:29]
        
        
        df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16, df17], axis=0)
        df = df[df.columns[:-1][::-1]].T
        df = pd.DataFrame(
            df.values, 
            index=[race_id] * len(df), 
            columns=['leading_index_1', 'pace_index_1', 'up_index_1', 'speed_index_1', 'leading_index_2', 'pace_index_2', 'up_index_2', 'speed_index_2', 'leading_index_3', 'pace_index_3', 'up_index_3', 'speed_index_3', 'leading_index_4', 'pace_index_4', 'up_index_4', 'speed_index_4', 'leading_index_5', 'pace_index_5', 'up_index_5', 'speed_index_5', '脚質', '頭数人気_1R', '通過順位_1R', '頭数人気_2R', '通過順位_2R', '頭数人気_3R', '通過順位_3R', '頭数人気_4R', '通過順位_4R', '頭数人気_5R', '通過順位_5R', '前回脚質']
        )
        df["馬番"] = range(1, len(df) + 1)
        
    except ValueError as e:
        columns = [
            'leading_index_1', 'pace_index_1', 'up_index_1', 'speed_index_1',
            'leading_index_2', 'pace_index_2', 'up_index_2', 'speed_index_2',
            'leading_index_3', 'pace_index_3', 'up_index_3', 'speed_index_3',
            'leading_index_4', 'pace_index_4', 'up_index_4', 'speed_index_4',
            'leading_index_5', 'pace_index_5', 'up_index_5', 'speed_index_5', '脚質', '頭数人気_1R', '通過順位_1R', '頭数人気_2R', '通過順位_2R', '頭数人気_3R', '通過順位_3R', '頭数人気_4R', '通過順位_4R', '頭数人気_5R', '通過順位_5R', '前回脚質'
        ]
        df = pd.DataFrame(0, index=["20" + race_id] * 16, columns=columns)    
        df["馬番"] = range(1, len(df) + 1)
    return df

def scrape_shisu(race_id_list: list, dirpath : str = LocalPaths.BASE_DIR + '/data/shisu_html', extension: str = '.html') -> pd.DataFrame:
    df_list = []
    
    for race_id in tqdm(race_id_list):
        shisupath = os.path.join(dirpath, race_id + '.html')
        if os.path.isfile(shisupath):
            print('race_id {} skipped because html has already loaded.'.format(race_id))
            with open(shisupath, 'r', encoding='Shift_JIS', errors='ignore') as file:
                html = file.read()
        else :
            print(race_id)
            tlimed_id = race_id[2:]
            html = scrape_from_jiro8(tlimed_id)
            filepath = os.path.join(dirpath, race_id + extension)
            
            with open(filepath, 'wt', encoding='Shift_JIS', errors='ignore') as f:
                f.write(html)
                
        df = extract_index_info(html, race_id)
        df_list.append(df)
    return pd.concat(df_list)

def get_ninki(race_id_list: list, dirpath : str = LocalPaths.BASE_DIR + '/data/shisu_html', extension: str = '.html') -> pd.DataFrame:
    df_list = []
    
    for race_id in tqdm(race_id_list):
        shisupath = os.path.join(dirpath, race_id + '.html')
        if os.path.isfile(shisupath):
            print('race_id {} skipped because html has already loaded.'.format(race_id))
            with open(shisupath, 'r', encoding='Shift_JIS', errors='ignore') as file:
                html = file.read()
        else :
            print(race_id)
            tlimed_id = race_id[2:]
            html = scrape_from_jiro8(tlimed_id)
            filepath = os.path.join(dirpath, race_id + extension)
            
            with open(filepath, 'wt', encoding='Shift_JIS', errors='ignore') as f:
                f.write(html)
                
        df = extract_ninki(html, race_id)
        df_list.append(df)
    return pd.concat(df_list)

def extract_ninki(html: str, race_id: str) -> pd.DataFrame:
    df = pd.read_html(html, attrs={'class': 'c1'})[0].iloc[8:9]

    df = df[df.columns[:-1][::-1]].T
    df = pd.DataFrame(
        df.values, 
        index=[race_id] * len(df), 
        columns=['人気オッズ']
    )
    df["馬番"] = range(1, len(df) + 1)
    df["race_id"] = race_id
    
    
    def parse_odds(value):
        match = re.match(r"([\d.]+) \((\d+)\)", str(value))
        if match:
            return float(match.group(1)), int(match.group(2))
        return None, None
    
    df[['単勝オッズ', '人気']] = df['人気オッズ'].apply(lambda x: pd.Series(parse_odds(x)))
    df.drop(columns=['人気オッズ'], inplace=True)
        
        

    return df