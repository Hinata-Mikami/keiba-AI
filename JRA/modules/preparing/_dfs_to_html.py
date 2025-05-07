import pandas as pd
import glob
import datetime
import warnings
from tqdm.auto import tqdm
from modules.constants import Master
from modules.constants import LocalPaths
from modules.constants import HorseResultsCols
from modules.constants import ResultsCols
from modules import preparing
from modules import preprocessing
from modules import training
from modules import simulation
from modules import policies
import os
from contextlib import redirect_stdout


def dfs_to_html(date, ids, keiba_ai, keiba_ai2, keiba_ai3, keiba_ai4):
    
    file_name = date + ".html"
    folder_path = "./score_html"
    file_path = os.path.join(folder_path, file_name)
    
    scripts = """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/css/foundation.min.css" rel="stylesheet"/>
    <link href="https://cdn.datatables.net/v/zf/jq-3.6.0/dt-1.13.4/b-2.3.6/b-html5-2.3.6/date-1.4.1/fh-3.3.2/sb-1.4.2/datatables.min.css" rel="stylesheet"/>
    
    <script src="https://cdn.datatables.net/v/zf/jq-3.6.0/dt-1.13.4/b-2.3.6/b-html5-2.3.6/date-1.4.1/fh-3.3.2/sb-1.4.2/datatables.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/js/foundation.min.js"></script>

    <script>
        $(document).ready(function() {
            $('.my-table').DataTable({
                select: true,
                displayLength: 20,
                buttons: ['copy'],
                fixedHeader: true,
                dom: 'iQrtBlp',
            });
        });
    </script>

    <style>
        /* 全体のフォントと背景色 */
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
        }
        /* ヘッダーとサマリーのスタイル */
        .header-title {
            font-size: 2.5em;
            margin: 20px 0;
            color: #333;
            text-align: center;
        }
        .summary-title {
            font-size: 2.5em;
            margin: 10px 0;
            color: #444;
        }
        /* テーブルのスタイル */
        .my-table {
            font-size: 0.7em;
            width: 90%;
            margin: 20px 0;
            height: 20px; /* 行の高さを固定 */
            line-height: 20px; /* 行の高さに合わせて縦方向の中央揃え */
            /*overflow: hidden;  セルからはみ出したテキストを隠す */
            white-space: nowrap;  /*テキストを折り返さず1行にする */
            text-overflow: ellipsis; /* 省略記号(...)を表示 */
        }
        /* レース情報のスタイル */
        .race-info {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #555;
        }
        /* 大きなフォントサイズのクラス */
        .large-font {
            font-size: 1.5em; /* 大きなフォントサイズを指定 */
            color: #222;
        }
        
         /* 枠の色 */
        .frame-1 { background-color: white; }
        .frame-2 { background-color: black; color: white; }
        .frame-3 { background-color: red; color: white; }
        .frame-4 { background-color: blue; color: white; }
        .frame-5 { background-color: yellow; }
        .frame-6 { background-color: green; color: white; }
        .frame-7 { background-color: orange; color: white; }
        .frame-8 { background-color: pink; }

        /* スコア色分け */
        .highest { background-color: Tomato; }
        .top-25 { background-color: Yellow; }
        .bottom-25 { background-color: #90D7EC; }
        /* 特定値の色分け */
        .value-1 { background-color: yellow; }
        .value-2 { background-color: skyblue; }
        .value-3 { background-color: orange; }

        /* 範囲色分け */
        .range-low { background-color: Tomato; }
        .range-high { background-color: skyblue; }
    </style>
    

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // すべてのテーブルを取得
            const tables = document.querySelectorAll('.my-table');

            tables.forEach(table => {
                // 「枠」列の色を設定（列インデックス1が「枠」）
                table.querySelectorAll('tbody tr').forEach(row => {
                    const frameCell = row.cells[1]; // 「枠」列の位置（1列目がインデックス0）
                    const frameValue = frameCell.textContent.trim();
                    frameCell.classList.add('frame-' + frameValue);
                });

                // 色付けする列のインデックスと列名を定義
                const scoreColumns = [3, 4, 5, 14, 15, 16, 17, 18, 19, 20, 21, 22];
                const specificValueColumn = 7;
                const rangeColumn = 8;

                // スコア列の色付け
                scoreColumns.forEach(colIndex => {
                    const cells = Array.from(table.querySelectorAll(`tbody tr td:nth-child(${colIndex + 1})`));
                    const values = cells.map(cell => parseFloat(cell.textContent) || 0).sort((a, b) => a - b);

                    const max = values[values.length - 1];
                    const top25Threshold = values[Math.floor(values.length * 0.75)];
                    const top50Threshold = values[Math.floor(values.length * 0.50)];
                    const bottom25Threshold = values[Math.floor(values.length * 0.25)];

                    cells.forEach(cell => {
                        const cellValue = parseFloat(cell.textContent) || 0;
                        if (cellValue === max) {
                            cell.classList.add('highest');
                        } else if (cellValue >= top25Threshold) {
                            cell.classList.add('top-25');
                        } else if (cellValue <= bottom25Threshold) {
                            cell.classList.add('bottom-25');
                        }
                    });
                });

                // 特定値に基づく色分け（列インデックス 5）
                table.querySelectorAll(`tbody tr td:nth-child(${specificValueColumn + 1})`).forEach(cell => {
                    const cellValue = parseInt(cell.textContent, 10);
                    if (cellValue === 1) {
                        cell.classList.add('value-1');
                    } else if (cellValue === 2) {
                        cell.classList.add('value-2');
                    } else if (cellValue === 3) {
                        cell.classList.add('value-3');
                    }
                });

                // 範囲に基づく色分け（列インデックス 6）
                table.querySelectorAll(`tbody tr td:nth-child(${rangeColumn + 1})`).forEach(cell => {
                    const cellValue = parseFloat(cell.textContent) || 0;
                    if (cellValue < 10) {
                        cell.classList.add('range-low');
                    } else if (cellValue >= 100) {
                        cell.classList.add('range-high');
                    }
                });
            });
        });
    </script>

    """


    # サマリーセクション
    summary_html = f"""
    <header>
        <div class="header-title"> {date} SUMMARY </div>
        <div class="summary-title"> 今日の波乱想定レース </div>
    </header>
    """
    
    
    dfs = []
    # keiba_ai = training.KeibaAIFactory.load('models/20250327/basemodel_shisu_v11.0.pickle')
    # keiba_ai2 = training.KeibaAIFactory.load('models/20250329/basemodel_shisu_v13.1.pickle')
    # keiba_ai3 = training.KeibaAIFactory.load('models/20250329/basemodel_shisu_v13.0.pickle')     
    # keiba_ai4 = training.KeibaAIFactory.load('models/20250426/basemodel_v15.0_L3F.pickle')   
    are_races = []
    points = []
    nums = []
    scores = []
    pops = []
    
    
    html = scripts
    # サマリーのHTML構成
    html += summary_html
    
    html_tables = """ """
    
    if ids == []:
        with redirect_stdout(open(os.devnull, 'w')):
            race_id_list, race_time_list = preparing.scrape_race_id_race_time_list(date)
    else:
        race_id_list = ids
        race_time_list = ['0:00'] * len(ids)
    
    for race_id, race_time in zip(race_id_list, race_time_list):
        with redirect_stdout(open(os.devnull, 'w')):
            (df, loc, R, df_tmp, nisai, hinba) = preparing.calc_score(date, [race_id], keiba_ai, keiba_ai2, keiba_ai3, keiba_ai4)
        # print(df)
        if R != -1:
            df0 = preparing.scrape_race_info(race_id)

            df = df0.merge(df, on=['馬番'], how='left')
            df.set_index('馬番')
            df["score_x"] *= 100
            # df['score_x'] += 50
            df["score_y"] *= 100
            df["score_z"] *= 100
            df["score_w"] *= 10
            
            # Assuming df is already defined
            # Replace NaN values with 0 (or any other integer value)
            df["score_x"].fillna(0, inplace=True)
            df["score_y"].fillna(0, inplace=True)
            df["score_z"].fillna(0, inplace=True)
            df["score_w"].fillna(0, inplace=True)
            pace = df["score_w"].mean().round(2)
            df["score_x"] = df["score_x"].astype(float).round(1)
            df["score_y"] = df["score_y"].astype(float).round(1)
            df["score_z"] = df["score_z"].astype(float).round(1)
            df["score_w"] = df["score_w"].astype(float).round(2)
            # df['AI Score'] = df["score_x"] + df["score_y"] 
            df = df.rename(columns={'score_x': 'v11.0 実力' })
            df = df.rename(columns={'score_y': 'v13.1 穴馬'})
            df = df.rename(columns={'score_z': 'v13.0 穴馬'})
            df = df.rename(columns={'score_w': 'ラスト3F'})
            df = df.rename(columns={'５走 平均': '平均'})
            df = df.rename(columns={'斤量_x': '斤量'})
            df["馬名"] = df["馬名"].str.split().str[1]
            
            # 各行で最大値を持つカラム名を取得
            max_cols = df[['脚質_逃げ', '脚質_先行', '脚質_差し', '脚質_追い']].idxmax(axis=1)

            # カラム名に基づくマッピング
            mapping = {
                '脚質_逃げ': '逃',
                '脚質_先行': '先',
                '脚質_差し': '差',
                '脚質_追い': '追'
            }
            df['脚質'] = max_cols.map(mapping)
            
            
            # df = df.drop(columns = ['脚質_逃げ', '脚質_先行', '脚質_差し', '脚質_追い', '枠番',  '斤量_y', 'jockey_id',  '年齢',  'n_horses',  'course_len', 'race_type_芝',  'race_type_ダート',    '性_牡',    '性_牝',    '性_セ',  '開催_01',  '開催_02',  '開催_03', '開催_04',  '開催_05',  '開催_06',  '開催_07',  '開催_08',  '開催_09',  '開催_10',  'race_class_1勝クラス', 'race_class_2勝クラス',  'race_class_3勝クラス',  'race_class_オープン',  'race_class_G3', 'race_class_G2',  'race_class_G1',  'leading_index_1',  'pace_index_1',  'leading_index_max',  'pace_index_max', 'leading_index_avg',  'pace_index_avg', 'speed_index_avg3', '逃げ馬',    '先行馬', '距 離',  'コ ｜ ス',     '3走',     '2走', '評価.1', 'type_diff_芝toダ',  'type_diff_ダto芝',  'course_len_diff',  'race_class', 'race_class_diff'], axis = 1)
            df = df.rename(columns={'up_index_1': '上り指1R'})
            df = df.rename(columns={'up_index_max': '上り指MAX'})
            df = df.rename(columns={'up_index_avg': '上り指AVG'})
            df = df.rename(columns={'speed_index_1': 'スピ指1R'})
            df = df.rename(columns={'speed_index_max': 'スピ指MAX'})
            df = df.rename(columns={'speed_index_avg': 'スピ指AVG'})
    
            df['上り指AVG'] = df['上り指AVG'].round(1)
            df['上り指MAX'] = df['上り指MAX'].round(1)
            df['上り指1R'] = df['上り指1R'].round(1)
            df['スピ指1R'] = df['スピ指1R'].round(1)
            df['スピ指MAX'] = df['スピ指MAX'].round(1)
            df['スピ指AVG'] = df['スピ指AVG'].round(1)

            
            
            for i in ["1", "2", "3", "4"]:
                for j in ["1", "2", "3", "4", "5"]:
                    df = df.drop(columns = ["通過"+i+"C_"+j+"R"], axis = 1)
            
            if '単勝 オッズ' in df.columns:
                df = df.reindex(columns=['枠_x', '馬番', 'v11.0 実力', 'v13.1 穴馬', 'v13.0 穴馬' ,'ラスト3F',  '人 気', '単勝 オッズ',  '馬名', '性齢', '斤量', '騎手', '脚質', '最 高', '平均', '前走', '上り指MAX', '上り指AVG', '上り指1R', 'スピ指MAX', 'スピ指AVG', 'スピ指1R'])

            else:
                df = df.reindex(columns=['枠_x', '馬番','v11.0 実力', 'v13.1 穴馬', 'v13.0 穴馬', 'ラスト3F', '人 気', '予想 オッズ',  '馬名', '性齢', '斤量', '騎手', '脚質',  '最 高', '平均', '前走', '上り指MAX', '上り指AVG', '上り指1R', 'スピ指MAX', 'スピ指AVG', 'スピ指1R'])


            dfs.append(df)
            
            df1 = df
            # df0 = df1.sort_values('v11.0 実力', ascending=False)
            # num_11 = df0.iat[0, 1]
            # num_12 = df0.iat[1, 1]
            # num_13 = df0.iat[2, 1]
            # num_14 = df0.iat[3, 1]
            # try:
            #     num_15 = df0.iat[4, 1]
            # except IndexError:
            #     num_15 = 0
                    
            # try:
            #     num_16 = df0.iat[5, 1]
            # except IndexError:
            #     num_16 = 0
                
            # pop_11 = int(df0.iat[0, 5])
            # pop_12 = int(df0.iat[1, 5])
            # pop_13 = int(df0.iat[2, 5])
            # pop_14 = int(df0.iat[3, 5])
            # try:
            #     pop_15 = int(df0.iat[4, 5])
            # except IndexError:
            #     pop_15 = 0
                    
            # try:
            #     pop_16 = int(df0.iat[5, 5])
            # except IndexError:
            #     pop_16 = 0
                
            # sc_11 = df0.iat[0, 2]
            # sc_12 = df0.iat[1, 2]
            # sc_13 = df0.iat[2, 2]
            # sc_14 = df0.iat[3, 2]
            # try:
            #     sc_15 = df0.iat[4, 2]
            # except IndexError:
            #     sc_15 = 0
                    
            # try:
            #     sc_16 = df0.iat[5, 2]
            # except IndexError:
            #     sc_16 = 0

            df2 = df1.sort_values('v11.0 実力', ascending=False)
            num_51 = df2.iat[0, 1]
            num_52 = df2.iat[1, 1]
            num_53 = df2.iat[2, 1]
            num_54 = df2.iat[3, 1]
            num_55 = df2.iat[4, 1]
            try:
                num_56 = df2.iat[5, 1]
            except IndexError:
                num_56 = 0
            pop_51 = int(df2.iat[0, 6])
            pop_52 = int(df2.iat[1, 6])
            pop_53 = int(df2.iat[2, 6])
            pop_54 = int(df2.iat[3, 6])
            pop_55 = int(df2.iat[4, 6])
            try:
                pop_56 = int(df2.iat[5, 6])
            except IndexError:
                pop_56 = 0
                
            sc_51 = df2.iat[0, 3]
            sc_52 = df2.iat[1, 3]
            sc_53 = df2.iat[2, 3]
            sc_54 = df2.iat[3, 3]
            try:
                sc_55 = df2.iat[4, 3]
            except IndexError:
                sc_55 = 0
                    
            try:
                sc_56 = df2.iat[5, 3]
            except IndexError:
                sc_56 = 0

            if df_tmp.iat[0, 15] == '晴': cl = 13
            else: cl = 15
        
            young, handi = preparing.check_info(race_id)
            print(young, handi)
            
            info = ""
            if nisai == True:
                info = info + " 2歳 "
            if hinba == True:
                info = info + " 牝馬限定 "
            if young == True:
                info = info + " 若手騎手競走 "
            if handi == True:
                info = info + " ハンデ "
        
            # レース情報とテーブル
            race_info_html = f"""
            <div class="race-info">
                <head><span class="large-font">
                {loc}{R}R {race_time}発走 {df_tmp.iat[0, 11]}{df_tmp.iat[0, 10]}m {df_tmp.iat[0, cl]} {info}<br>
                </span></head>
                Point : {pop_51 + pop_52 + pop_53} Pace : {pace} <br>
            </div>
            """
            html_tables += race_info_html + df.to_html(classes='my-table') + "<br><br>"

                # オープンクラスモデル (ver 7.7.1)<br>
                # ◎:{num_11}({pop_11}人気) 〇:{num_12}({pop_12}人気)  ▲:{num_13}({pop_13}人気)  △I:{num_14}({pop_14}人気)  △II:{num_15}({pop_15}人気)<br>
                # 1・2・3勝クラスモデル (ver 7.7.3)<br>
                # ◎:{num_51}({pop_51}人気) 〇:{num_52}({pop_52}人気)  ▲:{num_53}({pop_53}人気)  △I:{num_54}({pop_54}人気)  △II:{num_55}({pop_55}人気)<br>

            
            if (pop_51 + pop_52 + pop_53) >= 10:
                location = loc + R + 'R ' + race_time + '発走' + info
                are_races.append(location)
                points.append(pop_51 + pop_52 + pop_53)
                nums.append(num_51)
                nums.append(num_52)
                nums.append(num_53)
                nums.append(num_54)
                nums.append(num_55)
                nums.append(num_56)
                scores.append(sc_51)
                scores.append(sc_52)
                scores.append(sc_53)
                scores.append(sc_54)
                scores.append(sc_55)
                scores.append(sc_56)
                pops.append(pop_51)
                pops.append(pop_52)
                pops.append(pop_53)
                pops.append(pop_54)
                pops.append(pop_55)
                pops.append(pop_56)
                
    
            print(race_id + " output completed.")
            
    # サマリー出力（文字化けしないよう `<div>` のみを追加）
    for n in range(len(are_races)):
        html += f"""
        <div class="race-info">
            <font size="5">Point : {points[n]} {are_races[n]}<br></font>
            <font size="4">
                ◎:{nums[6*n]}({pops[6*n]}人気/{scores[6*n]}) 〇:{nums[6*n+1]}({pops[6*n+1]}人気/{scores[6*n+1]})  
                ▲:{nums[6*n+2]}({pops[6*n+2]}人気/{scores[6*n+2]}) △I:{nums[6*n+3]}(想定{pops[6*n+3]}/{scores[6*n+3]})  
                △II:{nums[6*n+4]}({pops[6*n+4]}人気/{scores[6*n+4]})
            </font>
        </div>
        """

    # レースのDataFrame HTMLテーブル部分
    html += html_tables

    html += "</body></html>"

    # UTF-8で保存
    os.makedirs(folder_path, exist_ok=True)
    with open(file_path, mode='w', encoding='utf-8-sig') as f:
        f.write(html)

            
    print("Html generated successfully. The file name is "+ file_name)
        
        
def dfs_to_html_for_test (dates : list, file_name : str):

    folder_path = "./score_html"
    file_path = os.path.join(folder_path, file_name)
    
    scripts = """
        <link href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/css/foundation.min.css" rel="stylesheet"/>
        <link href="https://cdn.datatables.net/v/zf/jq-3.6.0/dt-1.13.4/b-2.3.6/b-html5-2.3.6/date-1.4.1/fh-3.3.2/sb-1.4.2/datatables.min.css" rel="stylesheet"/>
        
        <script src="https://cdn.datatables.net/v/zf/jq-3.6.0/dt-1.13.4/b-2.3.6/b-html5-2.3.6/date-1.4.1/fh-3.3.2/sb-1.4.2/datatables.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.4.3/js/foundation.min.js"></script>

        <script>
            $(document).ready(function() {$('.my-table').DataTable({
                select: true,
                displayLength: 25,
                buttons: ['copy'],
                fixedHeader: true,
                dom: 'iQrtBlp',
            });})
        </script>
        """
    html = scripts
    
    
    for date in dates:
        
        print("##########################################")
        print(date + " started.")
        
        dfs = []
        keiba_ai = training.KeibaAIFactory.load('models/20241004/basemodel_shisu_v5.5.pickle')
        keiba_ai2 = training.KeibaAIFactory.load('models/20241003/basemodel_shisu_v5.3.pickle')
        with redirect_stdout(open(os.devnull, 'w')):
            race_id_list, _ = preparing.scrape_race_id_race_time_list(date)
        
        
        for race_id in race_id_list:
            with redirect_stdout(open(os.devnull, 'w')):
                (df, loc, R, df_tmp, _, _) = preparing.calc_score(date, [race_id], keiba_ai, keiba_ai2)
            if R != -1:
                df0 = preparing.scrape_race_info(race_id)
                df = df0.merge(df, on=['馬番'], how='left')
                df.set_index('馬番')
                df["score_x"] *= 100
                df["score_y"] *= 100
                df["score_x"] = df["score_x"].fillna(0).astype(float).round(1)
                df["score_y"] = df["score_y"].fillna(0).astype(float).round(1)
                df['AI Score'] = df["score_x"] + df["score_y"] 
                df = df.rename(columns={'score_x': 'AI (v5.5)'})
                df = df.rename(columns={'score_y': 'AI (v5.3)'})
                df = df.rename(columns={'５走 平均': '平均'})
                df = df.rename(columns={'斤量_x': '斤量'})
                df["馬名"] = df["馬名"].str.split().str[1]
                
                # 各行で最大値を持つカラム名を取得
                max_cols = df[['脚質_逃げ', '脚質_先行', '脚質_差し', '脚質_追い']].idxmax(axis=1)

                # カラム名に基づくマッピング
                mapping = {
                    '脚質_逃げ': '逃',
                    '脚質_先行': '先',
                    '脚質_差し': '差',
                    '脚質_追い': '追'
                }
                df['脚質'] = max_cols.map(mapping)
                
                
                # df = df.drop(columns = ['脚質_逃げ', '脚質_先行', '脚質_差し', '脚質_追い', '枠番',  '斤量_y', 'jockey_id',  '年齢',  'n_horses',  'course_len', 'race_type_芝',  'race_type_ダート',    '性_牡',    '性_牝',    '性_セ',  '開催_01',  '開催_02',  '開催_03', '開催_04',  '開催_05',  '開催_06',  '開催_07',  '開催_08',  '開催_09',  '開催_10',  'race_class_1勝クラス', 'race_class_2勝クラス',  'race_class_3勝クラス',  'race_class_オープン',  'race_class_G3', 'race_class_G2',  'race_class_G1',  'leading_index_1',  'pace_index_1',   'leading_index_max',  'pace_index_max', 'leading_index_avg',  'pace_index_avg', 'speed_index_avg3', '逃げ馬',    '先行馬', '距 離',  'コ ｜ ス',     '3走',     '2走', '評価.1', 'type_diff_芝toダ',  'type_diff_ダto芝',  'course_len_diff',  'race_class', 'race_class_diff'], axis = 1)
                df = df.rename(columns={'up_index_1': '上り指1R'})
                df = df.rename(columns={'up_index_max': '上り指MAX'})
                df = df.rename(columns={'up_index_avg': '上り指AVG'})
                df = df.rename(columns={'speed_index_1': 'スピ指1R'})
                df = df.rename(columns={'speed_index_max': 'スピ指MAX'})
                df = df.rename(columns={'speed_index_avg': 'スピ指AVG'})
                df['上り指AVG'] = df['上り指AVG'].round(0)
                df['上り指MAX'] = df['上り指MAX'].round(0)
                df['上り指1R'] = df['上り指1R'].round(0)
                df['スピ指1R'] = df['スピ指1R'].round(0)
                df['スピ指MAX'] = df['スピ指MAX'].round(0)
                df['スピ指AVG'] = df['スピ指AVG'].round(0)
                
                for i in ["1", "2", "3", "4"]:
                    for j in ["1", "2", "3", "4", "5"]:
                        df = df.drop(columns = ["通過"+i+"C_"+j+"R"], axis = 1)
                
                if '単勝 オッズ' in df.columns:
                    df = df.reindex(columns=['枠', '馬番','AI Score', 'AI (v5.3)', 'AI (v5.5)', '人 気', '単勝 オッズ',  '馬名', '性齢', '斤量', '騎手', '脚質', '最 高', '平均', '前走', '上り指MAX', '上り指AVG', '上り指1R', 'スピ指MAX', 'スピ指AVG', 'スピ指1R'])

                else:
                    df = df.reindex(columns=['枠', '馬番','AI Score', 'AI (v5.3)', 'AI (v5.5)', '人 気', '予想 オッズ',  '馬名', '性齢', '斤量', '騎手', '脚質', '最 高', '平均', '前走', '上り指MAX', '上り指AVG', '上り指1R', 'スピ指MAX', 'スピ指AVG', 'スピ指1R'])


                dfs.append(df)
                
                df1 = df
                df0 = df1.sort_values('AI Score', ascending=False)
                num_11 = df0.iat[0, 1]
                num_12 = df0.iat[1, 1]
                num_13 = df0.iat[2, 1]
                num_14 = df0.iat[3, 1]
                try:
                    num_15 = df0.iat[4, 1]
                except IndexError:
                    num_15 = 0
                    
                try:
                    num_16 = df0.iat[5, 1]
                except IndexError:
                    num_16 = 0



                if df_tmp.iat[0, 15] == '晴': cl = 13
                else: cl = 15
            
                html_info = f"""
                <!DOCTYPE html>
                <html lang="ja">
                <head>
                    <meta charset="Shift-JIS">
                </head>
                <body>
                    <header>
                        <font size="3">
                            {date} {loc}{R}R {df_tmp.iat[0, 11]}{df_tmp.iat[0, 10]}m {df_tmp.iat[0, cl]}<br>
                        </font>
                        <font size="3">
                            {num_11} - {num_12} - {num_13} - {num_14} - {num_15} - {num_16}<br>
                        </font>
                    </header>
                </body>
                </html>
                """
                
                html = html + html_info +"<br>"
                
                print(race_id + " fin.")

    with open(file_path, mode='w') as f:
        f.write(html)
                
    print("Html generated successfully. The file name is "+ file_name)