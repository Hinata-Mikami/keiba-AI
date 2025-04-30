import os
import time
from tqdm.notebook import tqdm
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.exceptions import SSLError

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
    url = 'https://race.netkeiba.com/race/oikiri.html?race_id='+race_id+'&rf=race_submenu'
    
    # Login credentials
    USER = "mikami1354@icloud.com"
    PASS = "RespectKumiSasaki0122"
    login_info = {"login_id": USER, "pswd": PASS}
    # Headers with referer information
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Referer": "https://race.netkeiba.com/"
    }
    
    loop_sleeper.sleep(0.5)
    session = requests.Session()
    url_login = "https://regist.netkeiba.com/account/?pid=login&action=auth"
    session.post(url_login, data=login_info, headers=headers)
    
    # リトライ設定
    retry_strategy = Retry(
        total=10,  # 最大リトライ回数
        status_forcelist=[429, 500, 502, 503, 504],  # リトライ対象のHTTPステータス
        allowed_methods=["HEAD", "GET", "OPTIONS"],  # リトライするHTTPメソッド
        backoff_factor=10  # リトライ間隔
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)

    # Fetch the webpage
    html = session.get(url, headers=headers, timeout=10)
    
    # Decode using EUC-JP encoding
    decoded_html = html.content.decode('EUC-JP')

    # Parse the HTML content with BeautifulSoup (optional, only if specific parsing is required)
    soup = BeautifulSoup(decoded_html, 'html.parser')
    # pd.read_html returns a list of DataFrames
    try:
        dfs = pd.read_html(decoded_html)
        df = dfs[0]
        
        return df
    
    except ValueError:
        print(race_id+ ' skipped because no tables found.')
        return pd.DataFrame()  # Return an empty DataFrame in case of failure


def chokyo_df(race_id_list : list) -> pd.DataFrame:
    df = pd.DataFrame()
    for race_id in race_id_list:
        i = 1
        
        while i < 100:
            try:
                df0 = scrape_premium(race_id)
                print(race_id+ ' chokyo_info scraping completed (Att '+str(i)+')')
                i = 100
            except SSLError:
                print('SSLError detected. sleeping... (Att '+str(i)+')')
                time.sleep(10)
                i = i + 1

        
        df = pd.concat([df, df0], ignore_index=False)
    
    df['馬番'] = df['馬 番']
    df['race_id'] = race_id
    # df = df.drop(columns=['馬 番',  '印', '馬名', '日付', 'コース', '馬場', '乗り役', '調教タイム ラップ表示', '位置', '脚色', '評価'], axis=1)
    
    try:
        df = df.drop(columns=['映像'], axis=1)
    except KeyError:
        df = df
        
    return df