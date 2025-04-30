import os
import time
from tqdm.notebook import tqdm
import requests
import pandas as pd
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from modules.constants import UrlPaths, LocalPaths

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


def scrape_premium(race_id: str, skip) -> pd.DataFrame:
    url = 'https://race.netkeiba.com/race/speed.html?race_id='+race_id+'&rf=shutuba_submenu'
    
    dirpath : str = LocalPaths.BASE_DIR + 'data/timeshisu_html'
    
    # Login credentials
    USER = "mikami1354@icloud.com"
    PASS = "RespectKumiSasaki0122"
    login_info = {"login_id": USER, "pswd": PASS}
    # Headers with referer information
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Referer": "https://race.netkeiba.com/"
    }
    
    shisupath = os.path.join(dirpath, race_id + '.html')
    if os.path.isfile(shisupath) & skip:
        print('race_id {} skipped because html has already loaded.'.format(race_id))
        # with open(shisupath, 'r', encoding='EUC-JP', errors='ignore') as file:
        with open(shisupath, 'r') as file:
            html = file.read()
    else:    
        session = requests.Session()
        url_login = "https://regist.netkeiba.com/account/?pid=login&action=auth"
        session.post(url_login, data=login_info, headers=headers)
        
        # リトライ設定
        retry_strategy = Retry(
            total=5,  # 最大リトライ回数
            status_forcelist=[429, 500, 502, 503, 504],  # リトライ対象のHTTPステータス
            allowed_methods=["HEAD", "GET", "OPTIONS"],  # リトライするHTTPメソッド
            backoff_factor=10  # リトライ間隔
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        # Fetch the webpage
        html = session.get(url, headers=headers, timeout=10)
        time.sleep(1.5)
        
    # Decode using EUC-JP encoding
    decoded_html = html.content.decode('EUC-JP')

    # Parse the HTML content with BeautifulSoup (optional, only if specific parsing is required)
    soup = BeautifulSoup(decoded_html, 'html.parser')
    
    # pd.read_html returns a list of DataFrames
    dfs = pd.read_html(decoded_html)
        
    df = dfs[0]
    # MultiIndexを解除してフラットにする
    df.columns = df.columns.get_level_values(1)
    df['race_id'] = race_id
    df.index = [race_id] * len(df)
    df['馬番'] = df['馬 番']
    # 対象列を取得
    target_columns = df.columns.drop(['馬番', 'race_id'])
        

    # 文字列の処理
    for col in target_columns:
        df[col] = df[col].astype(str)
        # アスタリスクが含まれる場合は、数値部分を取得
        df[col] = df[col].str.replace('*', '', regex=False).str.split().str[-1]
            
        # df[col] = df[col].str.split().str[1]  # 空白で分割し、後半の数字のみを取得
        df[col] = pd.to_numeric(df[col], errors='coerce')  # 数字に変換し、'未'やエラーをNaNに

    
    try:
        # 不要な列を削除する
        df = df.drop(columns=['馬 番', '枠', '印', '馬名', '性齢', '斤量', '騎手', '単勝 オッズ', '人 気'], axis=1)
        
    except KeyError:
        df = df.drop(columns=['馬 番', '枠', '印', '馬名', '性齢', '斤量', '騎手', '予想 オッズ', '人 気'], axis=1)
        
    return df
    


def premium_time_df(race_id_list : list, skip = True) -> pd.DataFrame:
    df = pd.DataFrame()
    n = 0
    for race_id in race_id_list:
        i = 1
        n += 1
        
        while (i < 100):
            try:
                df0 = scrape_premium(race_id, skip)
                print(race_id+'(' + str(n) + '/' + str(len(race_id_list)) + ')' + ' timeshisu scraping completed (Att ' + str(i) + ').')
                i = 100
                
            except ValueError:
                print(race_id+ ' skipped because no tables found.')
                df0 = pd.DataFrame()
                i = 100
                
            except KeyError as e:
                print("KeyError Detected (Att " +str(i)+")")
                print(e)
                i += 1
        
        df = pd.concat([df, df0], ignore_index=False)
        
    return df


def scrape_race_info(race_id: str) -> pd.DataFrame:
    url = 'https://race.netkeiba.com/race/speed.html?race_id='+race_id+'&rf=shutuba_submenu'
    i = 0
    
    while i<100:
        try:
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
                total=5,  # 最大リトライ回数
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
            dfs = pd.read_html(decoded_html)
                
            df = dfs[0]
            # MultiIndexを解除してフラットにする
            df.columns = df.columns.get_level_values(1)
            df['race_id'] = race_id
            df.index = [race_id] * len(df)
            df['馬番'] = df['馬 番']
            # 対象列を取得
            # target_columns = df.columns.drop(['馬番', 'race_id'])
                

            # # 文字列の処理
            # for col in target_columns:
            #     df[col] = df[col].astype(str)
            #     # アスタリスクが含まれる場合は、数値部分を取得
            #     df[col] = df[col].str.replace('*', '', regex=False).str.split().str[-1]
                    
            #     # df[col] = df[col].str.split().str[1]  # 空白で分割し、後半の数字のみを取得
            #     df[col] = pd.to_numeric(df[col], errors='coerce')  # 数字に変換し、'未'やエラーをNaNに
            i = 100
        
        except KeyError:
            print("KeyError detected at _scrape_nkshisu.py/scrape_race_info (att "+str(i)+"). Retrying..." )
            i = i + 1

    
    try:
        df = df[['枠', '馬番', '馬名', '性齢', '斤量', '騎手', '単勝 オッズ', '人 気']]
        
    except KeyError:
        df = df[['枠', '馬番', '馬名', '性齢', '斤量', '騎手', '予想 オッズ', '人 気']]
        
    return df