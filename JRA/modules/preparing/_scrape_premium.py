import os
import time
from tqdm.notebook import tqdm
import requests
import pandas as pd
from bs4 import BeautifulSoup

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

def scrape_premium(race_id: str) -> pd.DataFrame:

    url = 'https://race.sp.netkeiba.com/barometer/score.html?race_id=' + race_id + '&rf=shutuba_submenu'
    
    # Login credentials
    USER = "mikami1354@icloud.com"
    PASS = "RespectKumiSasaki0122"
    login_info = {"login_id": USER, "pswd": PASS}

    loop_sleeper.sleep(0.5)
    session = requests.Session()
    url_login = "https://regist.netkeiba.com/account/?pid=login&action=auth"
    session.post(url_login, data=login_info)
    
    # Fetch the webpage
    html = session.get(url)
    
    # response = session.get(url)
    # soup = BeautifulSoup(response.text, "html.parser")
    # dfs = pd.read_html(str(soup))
    # pd.read_html returns a list of DataFrames
    dfs = pd.read_html(html.content)
    
    if dfs:
        for i, df in enumerate(dfs):
            if (len(df) >= 2) and (len(dfs[i-1]) == 1): j = i
            
        print('race_id '+ race_id + ' barometer is loaded.')
        df = dfs[j]
        # MultiIndexを解除してフラットにする
        df.columns = df.columns.get_level_values(1)
        df['race_id'] = race_id

        # '今回 偏差値'列を処理
        df['今回 偏差値'] = df['今回 偏差値'].astype(str)
        
        # '前走'列がない場合や空の場合に対応する処理
        if '前走' in df.columns:
            # '前走'列にNaNがある場合に備えて、NaNを文字列に変換し、str操作が可能なようにする
            df['前走'] = df['前走'].fillna('')  # NaNを空文字に置き換え
            df['前走'] = df['前走'].astype(str)  # 念のため全て文字列に変換
        else:
            df['前走'] = ''  # '前走'列が存在しない場合は、空の列を追加

        # 調子偏差値の計算
        df['調子偏差値'] = pd.to_numeric(df['今回 偏差値'].str[0:2], errors='coerce')

        # 前走偏差値を計算する際の処理（空文字列やNaNの場合は自動的にNaNになる）
        df['前回偏差値'] = pd.to_numeric(df['前走'].str[-2:], errors='coerce')

        # 上昇度を計算。ただし、'前回偏差値'がNaNの場合はNaNとなるようにする
        df['上昇度'] = df['調子偏差値'] - df['前回偏差値']

        # DataFrameを並べ替え
        df = df.sort_values('馬番')

        # 不要な列を削除する
        df = df.drop(columns=['着順', '今回 偏差値', '前走', '2走', '3走', '4走', '5走', '馬名 性齢 騎手 斤量', 'オッズ 人気'], axis=1, errors='ignore')
        
        return df
    else:
        raise ValueError("No tables found on the page.")
        return pd.DataFrame()  # Return an empty DataFrame in case of failure



def premium_df(race_id_list : list) -> pd.DataFrame:
    df = pd.DataFrame()
    for race_id in race_id_list:
        df0 = scrape_premium(race_id)
        df = pd.concat([df, df0], ignore_index=False)
        
    return df