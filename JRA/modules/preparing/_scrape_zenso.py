import os
import time
from tqdm.notebook import tqdm
import requests
import pandas as pd
import bs4

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
    # encodingを指定してから.text, 理由は後述。
    res.encoding = 'Shift_JIS'
    return res.text

def extract_index_info(html: str, race_id: str) -> pd.DataFrame:
    try:
        df = pd.read_html(html, attrs={'class': 'c1'}, encoding='UTF-8')[0].iloc[23:25]

        df = df[df.columns[:-1][::-1]].T
        df = pd.DataFrame(
            df.values.astype(str), 
            index=[race_id] * len(df), 
            columns=['前クラス', '前コース']
        )
        df["馬番"] = range(1, len(df) + 1)
        
    except ValueError as e:
        columns=['前クラス', '前コース']
        df = pd.DataFrame(0, index=["20" + race_id] * 16, columns=columns)    
        df["馬番"] = range(1, len(df) + 1)
    return df

def scrape_zenso(race_id_list: list, dirpath : str = 'h:\\Codes\\keibaAI\\data\\shisu_html', extension: str = '.html') -> pd.DataFrame:
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

dirpath = 'h:\\Codes\\keibaAI\\data\\shisu_html'
os.makedirs(dirpath, exist_ok=True)  # ディレクトリを作る


# index_info = run(race_id_list, dirpath)