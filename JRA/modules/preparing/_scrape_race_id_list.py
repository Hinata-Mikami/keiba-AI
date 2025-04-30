import pandas as pd
import datetime
import time
import re
from tqdm.auto import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
from selenium.webdriver.common.by import By

from modules.constants import UrlPaths
from ._prepare_chrome_driver import prepare_chrome_driver

def scrape_kaisai_date(from_: str, to_: str):
    """
    yyyy-mmの形式でfrom_とto_を指定すると、間のレース開催日一覧が返ってくる関数。
    to_の月は含まないので注意。
    """
    print('getting race date from {} to {}'.format(from_, to_))
    # 間の年月一覧を作成
    date_range = pd.date_range(start=from_, end=to_, freq="M")
    # 開催日一覧を入れるリスト
    kaisai_date_list = []
    for year, month in tqdm(zip(date_range.year, date_range.month), total=len(date_range)):
        # 取得したdate_rangeから、スクレイピング対象urlを作成する。
        # urlは例えば、https://race.netkeiba.com/top/calendar.html?year=2022&month=7 のような構造になっている。
        query = [
            'year=' + str(year),
            'month=' + str(month),
        ]
        url = UrlPaths.CALENDAR_URL + '?' + '&'.join(query)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        req = Request(url, headers=headers)
        html = urlopen(req).read()
    
        time.sleep(1.5)

        soup = BeautifulSoup(html, "html.parser")
        a_list = soup.find('table', class_='Calendar_Table').find_all('a')
        for a in a_list:
            kaisai_date_list.append(re.findall('(?<=kaisai_date=)\d+', a['href'])[0])
    return kaisai_date_list

def scrape_race_id_list(kaisai_date_list: list, waiting_time=10):
    """
    開催日をyyyymmddの文字列形式でリストで入れると、レースid一覧が返ってくる関数。
    ChromeDriverは要素を取得し終わらないうちに先に進んでしまうことがあるので、
    要素が見つかるまで(ロードされるまで)の待機時間をwaiting_timeで指定。
    """
    race_id_list = []
    driver = prepare_chrome_driver()
    # 取得し終わらないうちに先に進んでしまうのを防ぐため、暗黙的な待機（デフォルト10秒）
    driver.implicitly_wait(waiting_time)
    max_attempt = 2
    print('getting race_id_list')
    for kaisai_date in tqdm(kaisai_date_list):
        try:
            query = [
                'kaisai_date=' + str(kaisai_date)
            ]
            url = UrlPaths.RACE_LIST_URL + '?' + '&'.join(query)
            print('scraping: {}'.format(url))
            driver.get(url)
            time.sleep(1.5)

            for i in range(1, max_attempt):
                try:
                    a_list = driver.find_element(By.CLASS_NAME, 'RaceList_Box').find_elements(By.TAG_NAME, 'a')
                    time.sleep(1)
                    break
                except Exception as e:
                    # 取得できない場合は、リトライを実施
                    print(f'error:{e} retry:{i}/{max_attempt} waiting more {waiting_time} seconds')
                    time.sleep(waiting_time)

            for a in a_list:
                race_id = re.findall('(?<=shutuba.html\?race_id=)\d+|(?<=result.html\?race_id=)\d+',
                    a.get_attribute('href'))
                if len(race_id) > 0:
                    race_id_list.append(race_id[0])
        except Exception as e:
            print(e)
            break

    driver.close()
    driver.quit()
    return race_id_list


import re
from selenium.webdriver.common.by import By

def scrape_win5_list(kaisai_date_list: list, waiting_time=10):
    """
    開催日をyyyymmddの文字列形式のリストを渡すと、
    win5対象レースのrace_id一覧を返す関数。
    ChromeDriverは要素取得前に先に進む場合があるため、
    要素が見つかるまでの待機時間をwaiting_timeで指定。
    """
    race_id_list = []
    driver = prepare_chrome_driver()
    driver.implicitly_wait(waiting_time)
    print('getting win5 race_id_list')
    
    for kaisai_date in kaisai_date_list:
        try:
            url = 'https://race.netkeiba.com/top/win5.html?date=' + kaisai_date
            print('scraping: {}'.format(url))
            driver.get(url)
            
            # 「対象レース」テーブル内の「レース」行の<td>内にある<a>タグを全て取得
            race_links = driver.find_elements(By.XPATH,
                "//table[@class='win5raceresult2']//tr[td[contains(text(),'レース')]]/td/a"
            )
            for link in race_links:
                href = link.get_attribute("href")
                # href内のrace_idの部分を正規表現で抽出
                match = re.search(r"race_id=(\d+)", href)
                if match:
                    race_id_list.append(match.group(1))
        except Exception as e:
            print(e)
            break
        time.sleep(1.5)

    driver.close()
    driver.quit()
    return race_id_list
