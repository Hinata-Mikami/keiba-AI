import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re
import pandas as pd
import time
import os
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from requests.exceptions import HTTPError
import urllib.request

from modules.constants import UrlPaths, LocalPaths
import requests
from modules import preparing
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from pandas.errors import ParserError
from requests.exceptions import SSLError

import requests
from requests.exceptions import RequestException



def analyze_race_files(df, skip):
    # """
    # DataFrameの'race_id'列を基に指定された条件を満たすかをチェックし、
    # 'hinba_only', 'young_jockey_only', 'handicap'列を追加する。

    # Args:
    #     df (pd.DataFrame): 'race_id'列を含むDataFrame。
    #     skip (Bool): skipして上書きする。

    # Returns:
    #     pd.DataFrame: 新しいカラムを追加したDataFrame。
    # """
    # 新しいカラムを初期化
    # df['hinba_only'] = False
    df['young_jockey_only'] = False
    df['handicap'] = False
    df = df.reset_index()
    # race_idごとに結果を一時的に格納する辞書を用意
    race_results = {}
    n = 1
    # 重複を排除した race_id の一覧を取得
    unique_race_ids = df['race_id'].unique()

    for race_id in unique_race_ids:
        
        url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id + "&rf=race_list"

        time.sleep(1.1)  # サーバーへの負担を減らす
        print(f"{race_id} :: {n}/{len(unique_race_ids)}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        # req = Request(url, headers=headers)
        att = 1
        while att < 10:
            try:
                response = requests.get(url, headers=headers)
                response.encoding = 'EUC-JP'
                response.raise_for_status()  # HTTP エラーがあれば例外をスロー
                html_content = response.text
                att = 100
            except HTTPError:
                print(f"HTTPError detected. Retry after 10 seconds... attempt {att}")
                time.sleep(10)
                att += 1
            except SSLError:
                print(f"SSLError detected. Retry after 10 seconds... attempt {att}")
                time.sleep(10)
                att += 1
            except RequestException:
                print(f"RequestException detected. Retry after 10 seconds... attempt {att}")
                time.sleep(10)
                att += 1
    

        soup = BeautifulSoup(html_content, 'html.parser')
        text_to_check = soup.get_text()

        # 条件をチェックして結果を辞書に格納
        race_results[race_id] = {
            # 'hinba_only': ("牝(" in text_to_check) or ("牝[" in text_to_check),
            'young_jockey_only': "見習騎手" in text_to_check,
            'handicap': "ハンデ" in text_to_check,
        }

        n += 1


    # DataFrameに結果をマージ
    for index, row in df.iterrows():
        race_id = row['race_id']
        # df.at[index, 'hinba_only'] = race_results[race_id]['hinba_only']
        df.at[index, 'young_jockey_only'] = race_results[race_id]['young_jockey_only']
        df.at[index, 'handicap'] = race_results[race_id]['handicap']


    return df


def check_info (race_id):

    url = "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id + "&rf=race_list"
    # 相手サーバーに負担をかけないように1秒待機する
    time.sleep(1)
    print(url)
    # スクレイピング実行
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    req = Request(url, headers=headers)
    att = 1
    while att < 100:
        try:
            html_content = urlopen(req).read()
            att = 100
        except urllib.error.HTTPError:
            print(f"HTTPError detected. Retry after 1 seconds ... att {att}")
            time.sleep(1)
            att = att + 1


    # BeautifulSoupでHTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    # テキストを抽出してチェック
    text_to_check = soup.get_text()
    # フラグの設定
    # hinba_only = ("牝(" in text_to_check) | ("牝[" in text_to_check)
    young_jockey_only = "見習騎手" in text_to_check
    handicap = "ハンデ" in text_to_check
    
    return (young_jockey_only, handicap)



def scrape_info_of_start(df: pd.DataFrame) -> pd.DataFrame:
    # """
    # DataFrameに基づいて、'horse_id'および指定された日付より前の出遅れ割合を計算する関数。
    # df: DataFrame - 'horse_id', 'date'カラムを持つ。
    
    # Returns:
    #     horse_idごとの出遅れ割合を含むDataFrame。
    # """
    results = []

    n = 0
    for index, row in df.iterrows():
        n += 1
        race_id = row.name
        umaban = row['馬番']
        horse_id = row['horse_id']
        target_date = pd.to_datetime(row['date'])

        print(f"Processing {n}/{len(df)}: horse_id={horse_id}, date={target_date}")

        # scrape_horse_premiumから馬データを取得
        df_horse = scrape_horse_premium(horse_id, skip=True)

        if df_horse.empty:
            print(f"No data for horse_id: {horse_id}")
            late_start_ratio = 0

                # 結果を保存
            results.append({
                "馬番" : umaban,
                "race_id" : race_id,
                "出遅れ割合": late_start_ratio
            })

        else:
            # 日付をdatetime形式に変換
            df_horse['日付'] = pd.to_datetime(df_horse['日付'], format='%Y/%m/%d')

            # target_date以前のレースデータをフィルタリング
            df_filtered = df_horse[df_horse['日付'] < target_date]

            # 出遅れ回数をカウント
            if '備考' in df_filtered.columns:
                df_filtered.loc[:, '備考'] = df_filtered['備考'].astype(str).fillna('')  # 明示的に .loc を使用
            else:
                df_filtered['備考'] = ''  # '備考'列が存在しない場合は空文字列を設定
                
            late_start_count = df_filtered['備考'].str.contains('出遅れ', na=False).sum()
            # late_start_count = (df_filtered['備考'].str.contains('出遅れ', na=False).sum())+(df_filtered['備考'].str.contains('躓く', na=False).sum())+(df_filtered['備考'].str.contains('出脚鈍い', na=False).sum())+(df_filtered['備考'].str.contains('アオる', na=False).sum())

            # target_date以前のレース数
            race_count = len(df_filtered)

            # 出遅れ割合を計算（レース数が0の場合は0.0）
            late_start_ratio = late_start_count / race_count if race_count > 0 else 0.0

            # 結果を追加
            results.append({
                "馬番" : umaban,
                "race_id" : race_id,
                "出遅れ割合": late_start_ratio
            })

    # 結果をDataFrameに変換して返す
    return pd.DataFrame(results)


def scrape_info_of_start_1race(df: pd.DataFrame) -> pd.DataFrame:

    # """
    # 引数のDataFrameに基づいて、horse_idごとに過去のレース情報を取得し、
    # 指定された日付以前の出遅れ割合を計算してDataFrameに追加する関数。

    # Args:
    #     df (pd.DataFrame): 'horse_id', 'date'カラムを持つ。

    # Returns:
    #     pd.DataFrame: 出遅れ割合を追加したDataFrame。
    # """
    results = []

    # horse_idごとに処理
    unique_horse_ids = df['horse_id'].unique()
    race_date = pd.to_datetime(entry['date'])
    
    for n, horse_id in enumerate(unique_horse_ids, 1):
        print(f"Processing horse {n}/{len(unique_horse_ids)}: {horse_id}")

        # スクレイピングして馬のデータを取得
        df_horse = scrape_horse_premium(horse_id, skip=False)
        

        if df_horse.empty:
            print(f"No data for horse_id: {horse_id}")
            late_start_ratio = 0

            race_id = df['race_id']
                # 結果を保存
            results.append({
                "race_id" : race_id,
                "horse_id": horse_id,
                "date": race_date,
                "出遅れ割合": late_start_ratio
            })
        
        
        else :
            # 日付をdatetime形式に変換
            df_horse['日付'] = pd.to_datetime(df_horse['日付'], format='%Y/%m/%d')

            # df内のこのhorse_idのエントリを処理
            horse_entries = df[df['horse_id'] == horse_id]

            for _, entry in horse_entries.iterrows():
                

                # 指定の日付以前のレースデータをフィルタリング
                df_filtered = df_horse[df_horse['日付'] < race_date]

                # 出遅れ回数をカウント
                df_filtered.loc[:, '備考'] = df_filtered['備考'].fillna('')
                late_start_count = df_filtered['備考'].str.contains('出遅れ', na=False).sum()
                # late_start_count = (df_filtered['備考'].str.contains('出遅れ', na=False).sum())+(df_filtered['備考'].str.contains('躓く', na=False).sum())+(df_filtered['備考'].str.contains('出脚鈍い', na=False).sum())+(df_filtered['備考'].str.contains('アオる', na=False).sum())

                # 日付以前のレース数
                race_count = len(df_filtered)

                # 出遅れ割合を計算（レース数が0の場合は0.0）
                late_start_ratio = late_start_count / race_count if race_count > 0 else 0.0

                race_id = df['race_id']
                # 結果を保存
                results.append({
                    "race_id" : race_id,
                    "horse_id": horse_id,
                    "date": race_date,
                    "出遅れ割合": late_start_ratio
                })
                


    # 結果をDataFrameに変換
    results_df = pd.DataFrame(results)

    # 元のDataFrameにマージ
    df = df.merge(results_df, on=['horse_id', 'date'], how='left')

    return df



def scrape_horse_premium(horse_id, skip=False, max_retries=10) -> pd.DataFrame:
    """
    指定された馬IDのプレミアムデータを取得。
    horse_id: str - 馬ID
    skip: bool - スキップフラグ
    max_retries: int - 最大リトライ回数

    Returns:
        馬のデータフレーム
    """
    filename = f'./data/html/horse_premium/{horse_id}.html'

    # ファイルが既に存在する場合
    if skip and os.path.isfile(filename):
        print(f'horse_id {horse_id} skipped')
    else:
        # URLとヘッダーを設定
        url = f'https://db.netkeiba.com/horse/{horse_id}'
        USER = "mikami1354@icloud.com"
        PASS = "RespectKumiSasaki0122"
        login_info = {"login_id": USER, "pswd": PASS}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Referer": "https://race.netkeiba.com/"
        }

        session = requests.Session()
        url_login = "https://regist.netkeiba.com/account/?pid=login&action=auth"
        session.post(url_login, data=login_info)

        # リトライ設定
        retry_strategy = Retry(
            total=max_retries,  
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=10  
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        # HTMLを取得
        for attempt in range(max_retries):
            try:
                response = session.get(url, headers=headers)
                response.encoding = 'euc-jp'  # 適切なエンコーディングを指定
                html = response.text

                # HTMLが空かどうかを確認
                if not html.strip():
                    raise ValueError("Empty HTML document received")

                # 保存
                with open(filename, 'w', encoding='euc-jp', errors='ignore') as f:
                    f.write(html)

                # 成功したらループを抜ける
                time.sleep(1)
                break
            except (OSError, ValueError) as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed with error: {e}")
                time.sleep(10)
                if attempt + 1 == max_retries:
                    raise  # 最大リトライ回数を超えたらエラーを再送出

    # 保存したHTMLを読み込む
    with open(filename, 'r', encoding='euc-jp', errors='ignore') as file:
        html = file.read()

    # BeautifulSoupでHTML解析
    soup = BeautifulSoup(html, 'html.parser')

    # PandasでHTMLテーブルを読み込む
    dfs = pd.read_html(html)
    
    try:
        df = dfs[2]  # 必要なテーブルを指定
    except IndexError:
        df = pd. DataFrame()
    return df


            
def get_race_result(race_id, skip=False) -> pd.DataFrame:
    """
    """
    
    filename = os.path.join("./data/html/race_premium/", race_id+'.bin')

    # skipがTrueで、かつbinファイルがすでに存在する場合は飛ばす
    if skip and os.path.isfile(filename):
        # print('race_id {} skipped'.format(race_id))
        pass
    else:
        
        # race_idからurlを作る
        url = f"https://race.netkeiba.com/race/result.html?race_id={race_id}"
        # print(url)
        # 相手サーバーに負担をかけないように1秒待機する
        time.sleep(1.2)
        # スクレイピング実行
        # html = urlopen(url).read()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        req = Request(url, headers=headers)
        att = 1
        while att < 100:
            try:
                html = urlopen(req).read()
                att = 100
            except urllib.error.HTTPError:
                print(f"HTTPError detected. Retry after 10 seconds ... att {att}")
                time.sleep(10)
                att = att + 1
            except SSLError:
                print(f"SSLError detected. Retry after 10 seconds ... att {att}")
                time.sleep(10)
                att = att + 1
                
        # htmlをsoupオブジェクトに変換
        soup = BeautifulSoup(html, "lxml")
        # # レースデータが存在するかどうかをチェック
        # data_intro_exists = bool(soup.find("div", attrs={"class": "data_intro"}))

        # if not data_intro_exists:
        #     print('race_id {} skipped. This page is not valid.'.format(race_id))
        #     return pd.DataFrame()

        # else:
        # 保存するファイルパスを指定
        with open(filename, 'wb') as f:
            # 保存
            f.write(html)


    # 保存したHTMLを読み込む
    with open(filename, 'r', encoding='euc-jp', errors='ignore') as file:
        html = file.read()

    # BeautifulSoupでHTML解析
    soup = BeautifulSoup(html, 'html.parser')

    # PandasでHTMLテーブルを読み込む
    dfs = pd.read_html(html)
    
    try:
        df = dfs[0]  # 必要なテーブルを指定
    except IndexError:
        df = pd. DataFrame()
    return df

import pandas as pd
from tqdm import tqdm
 
def scrape_L3F_time(race_id_list, skip=False) -> pd.DataFrame:
    """
    指定されたレースIDのL3Fタイムを取得する関数。
    各馬について 残り3F地点の通過タイムとそのレース平均との差を計算し、time_4C として出力。
    """
    result_list = []

    for race_id in tqdm(race_id_list):
        try:
            df = get_race_result(race_id, skip=skip)
            if df is None or df.empty:
                continue

            # 必要なカラムの整形
            valid_df = df.copy()
            valid_df['馬番'] = valid_df['馬 番']
            valid_df['time'] = df['タイム'].apply(time_to_seconds)
            valid_df['L3F'] = pd.to_numeric(valid_df['後3F'], errors='coerce')

            # 有効なデータのみ抽出
            # valid_df = df.dropna(subset=['time', 'L3F'])
            # print(valid_df)

            # 残り3F地点の通過タイム = 走破タイム - 上がり
            valid_df['t_4C'] = valid_df['time'] - valid_df['L3F']

            # 平均値を算出して、差分を計算
            mean_4C = valid_df['t_4C'].mean()
            # print(mean_4C)
            valid_df['time_4C'] = valid_df['t_4C'] - mean_4C

            # 必要なカラムを抽出
            out_df = valid_df[['馬番', 'time_4C']].copy()
            out_df['race_id'] = race_id

            result_list.append(out_df[['race_id', '馬番','time_4C']])

        except Exception as e:
            print(f"Error processing race_id {race_id}: {e}")
            continue

    # 結果を結合して1つのDataFrameに
    if result_list:
        return pd.concat(result_list, ignore_index=True)
    else:
        return pd.DataFrame(columns=['race_id', '馬番', 'time_4C'])
    
def time_to_seconds(time_str):
    """
    '1:23.4' → 83.4 のように変換
    """
    if pd.isna(time_str):
        return None
    try:
        if ':' in time_str:
            minutes, seconds = time_str.split(':')
            return int(minutes) * 60 + float(seconds)
        else:
            return float(time_str)
    except:
        return None

import pandas as pd

def add_L3F_features(df):
    # L3F_avgをrace_idごとの平均で計算
    df['L3F_avg'] = df.groupby('race_id')['L3F'].transform('mean')
    
    # L3F_min3をrace_idごとに上位3頭の平均で計算
    def calc_min3_avg(group):
        top3_mean = group.nsmallest(3, 'L3F')['L3F'].mean()
        return pd.Series([top3_mean] * len(group), index=group.index)

    df['L3F_min3'] = df.groupby('race_id', group_keys=False).apply(calc_min3_avg)
    
    return df

