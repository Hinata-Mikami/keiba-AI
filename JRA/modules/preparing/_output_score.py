import pandas as pd
import glob
import os
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

# ターゲットエンコーディング時に「馬の成績」として扱う項目
TARGET_COLS = [
        HorseResultsCols.RANK,
        HorseResultsCols.PRIZE,
        HorseResultsCols.RANK_DIFF, 
        # 'first_corner',
        # 'final_corner',
        # 'first_to_rank',
        # 'first_to_final',
        # 'final_to_rank',
        # 'time_seconds'
        ]
# horse_id列と共に、ターゲットエンコーディングの対象にする列
GROUP_COLS = [
        'course_len',
        'race_type',
        HorseResultsCols.PLACE
        ]

horse_info_processor = preprocessing.HorseInfoProcessor(
    filepath=LocalPaths.RAW_HORSE_INFO_PATH)
horse_results_processor = preprocessing.HorseResultsProcessor(
    filepath=LocalPaths.RAW_HORSE_RESULTS_PATH)
peds_processor = preprocessing.PedsProcessor(filepath=LocalPaths.RAW_PEDS_PATH) 


def output_score(race_day_list):
    
    keiba_ai = training.KeibaAIFactory.load(LocalPaths.BASE_DIR + 'models/20241004/basemodel_shisu_v5.5.pickle') 
    # 一時的に出馬表を保存するパスを指定
    filepath = LocalPaths.BASE_DIR + 'data/tmp/shutuba.pickle'
    
    
    for day in race_day_list:
        print('__________________________________________')
        today = day[0:4]+'/'+day[4:6]+'/'+day[6:8]
        print(today)
        # 前日全レース予想用のレースidとレース発走時刻を取得
        target_race_id_list, target_race_time_list = preparing.scrape_race_id_race_time_list(day)
        print (target_race_id_list)
        print (target_race_time_list)
        

        for race_id, race_time in zip(target_race_id_list, target_race_time_list):
            # 出馬表の取得
            preparing.scrape_shutuba_table(race_id, today, filepath)

            # 前日予想の場合、馬体重を0（0）に補正
            pd2 = pd.read_pickle(filepath)
            pd2[ResultsCols.WEIGHT_AND_DIFF] = '0(0)'
            # 前日予想の場合、天候と馬場状態が公開されていない場合はこちらを有効にする
            pd2['weather'] = '晴'
            pd2['ground_state'] = '良'
            pd2.to_pickle(filepath)
            
            if (pd2['race_class'] == '未勝利').any(): print ("passed : 未勝利戦\n")
            elif (pd2['race_class'] == '新馬').any(): print ("passed : 新馬戦\n")
            elif (pd2['race_class'] == '障害').any(): print ("passed : 障害戦\n")

            else:
                speed_shisu = preparing.scrape_shisu([race_id])
                speed_shisu = preparing.trim_shisu(speed_shisu)
                zenso_info = preparing.scrape_zenso([race_id])
                zenso_info = preparing.trim_zenso(zenso_info)
                time_info = preparing.premium_time_df([race_id])
                # chokyo_info = preparing.chokyo_df([race_id])
                zenso_info.index.name = 'race_id'
                speed_shisu.index.name = 'race_id'   
                add_df0 = zenso_info.merge(speed_shisu, on=['race_id', '馬番'], how='left')
                add_df1 = time_info.merge(add_df0, on=['race_id', '馬番'], how='left')
                # add_df = chokyo_info.merge(add_df1, on=['race_id', '馬番'], how='left')
                add_df = preparing.analyze_race_files(add_df1, True)
                    
                # 出馬表の加工
                shutuba_table_processor = preprocessing.ShutubaTableProcessor(filepath)
                # テーブルのマージ
                shutuba_data_merger = preprocessing.ShutubaDataMerger(
                    shutuba_table_processor,
                    horse_results_processor,
                    horse_info_processor,
                    peds_processor,
                    target_cols=TARGET_COLS,
                    group_cols=GROUP_COLS
                )
                shutuba_data_merger.merge()
                # 特徴量エンジニアリング
                feature_enginnering_shutuba = preprocessing.FeatureEngineering(shutuba_data_merger) \
                    .add_interval()\
                    .add_agedays()\
                    .dumminize_ground_state()\
                    .dumminize_race_type()\
                    .dumminize_sex()\
                    .dumminize_weather()\
                    .encode_horse_id()\
                    .encode_jockey_id()\
                    .encode_trainer_id()\
                    .encode_owner_id()\
                    .encode_breeder_id()\
                    .dumminize_kaisai()\
                    .dumminize_around()\
                    .dumminize_race_class()
                        
                #指数系をさらにマージ
                feature_enginnering_shutuba.featured_data.index.name = 'race_id'
                add_df = add_df.set_index('race_id')
                d = feature_enginnering_shutuba.featured_data.merge(add_df, on=['race_id', '馬番'], how='left')
                d = preparing.trim_cols(d)
                
                X1 = d.drop(['date'], axis=1).reindex(columns=keiba_ai._KeibaAI__datasets.X_test.columns)

                # 当日の出走情報テーブル（前処理前）
                df_tmp = shutuba_table_processor.raw_data[:1] 
                i = 0
                for num in list(Master.PLACE_DICT.values()):
                    if num == race_id[4:6]:
                        print(list(Master.PLACE_DICT)[i] + race_id[10:12] + 'R ' +race_time    + '発走 ' + str(df_tmp.iat[0, 12])
                            + str(df_tmp.iat[0, 10]) + 'm ' + str(df_tmp.iat[0, 13]) + ' ' + str(df_tmp.iat[0, 15]))
                        break
                    i += 1

                print(keiba_ai.calc_score(X1, policies.BasicScorePolicy).sort_values('score', ascending=False))
                
                
def calc_score(day, race_id_list, keiba_ai, keiba_ai2, keiba_ai3, keiba_ai4, keiba_ai5, keiba_ai6):

    filepath = LocalPaths.BASE_DIR + '/data/tmp/shutuba.pickle'
    today = today = day[0:4]+'/'+day[4:6]+'/'+day[6:8]
        

    for race_id in race_id_list:
        # 出馬表の取得
        preparing.scrape_shutuba_table(race_id, today, filepath)

        # 前日予想の場合、馬体重を0（0）に補正
        pd2 = pd.read_pickle(filepath)
        pd2[ResultsCols.WEIGHT_AND_DIFF] = '0(0)'
        # 前日予想の場合、天候と馬場状態が公開されていない場合はこちらを有効にする
        pd2['weather'] = '晴'
        pd2['ground_state'] = '良'
        pd2.to_pickle(filepath)
            
        if (pd2['race_class'] == '未勝利').any(): 
            print ("passed : 未勝利戦\n") 
            return ([], [], -1, [], None, None)

        elif (pd2['race_class'] == '新馬').any(): 
            print ("passed : 新馬戦\n")
            return ([], [], -1, [], None, None)

        elif (pd2['race_class'] == '障害').any(): 
            print ("passed : 障害戦\n")
            return ([], [], -1, [], None, None)


        else:
            speed_shisu = preparing.scrape_shisu([race_id])
            speed_shisu = preparing.trim_shisu(speed_shisu)
            zenso_info = preparing.scrape_zenso([race_id])
            zenso_info = preparing.trim_zenso(zenso_info)
            time_info = preparing.premium_time_df([race_id])
            # chokyo_info = preparing.chokyo_df([race_id])
            zenso_info.index.name = 'race_id'
            speed_shisu.index.name = 'race_id'
            add_df = zenso_info.merge(speed_shisu, on=['race_id', '馬番'], how='left')
            add_df = time_info.merge(add_df, on=['race_id', '馬番'], how='left')
            # add_df = chokyo_info.merge(add_df1, on=['race_id', '馬番'], how='left')
            add_df = preparing.analyze_race_files(add_df, True)
                    
            # 出馬表の加工
            shutuba_table_processor = preprocessing.ShutubaTableProcessor(filepath)
            # テーブルのマージ
            shutuba_data_merger = preprocessing.ShutubaDataMerger(
                    shutuba_table_processor,
                    horse_results_processor,
                    horse_info_processor,
                    peds_processor,
                    target_cols=TARGET_COLS,
                    group_cols=GROUP_COLS
                )
            shutuba_data_merger.merge()
            # 特徴量エンジニアリング
            feature_enginnering_shutuba = preprocessing.FeatureEngineering(shutuba_data_merger) \
                    .add_interval()\
                    .add_agedays()\
                    .dumminize_ground_state()\
                    .dumminize_race_type()\
                    .dumminize_sex()\
                    .dumminize_weather()\
                    .encode_jockey_id()\
                    .encode_trainer_id()\
                    .encode_owner_id()\
                    .encode_breeder_id()\
                    .dumminize_kaisai()\
                    .dumminize_around()\
                    .dumminize_race_class()
                        
            # 指数系をさらにマージ
            feature_enginnering_shutuba.featured_data.index.name = 'race_id'
            add_df = add_df.set_index('race_id')
            d1 = feature_enginnering_shutuba.featured_data.merge(add_df, on=['race_id', '馬番'], how='left')
            tmp = preparing.scrape_info_of_start(d1)
            d1 = d1.merge(tmp, on=['race_id', '馬番'], how='left')
            d1 = d1.set_index('race_id')
            # d1 = preparing.trim_cols(d)
            # d1 = preparing.drop_horseid(d1)
            d1 = preparing.adjust_cols(d1)
            nisai = d1['2歳戦'].iloc[0]
            hinba = d1['牝馬限定'].iloc[0]

            print(f"nisai {nisai} hinba {hinba}")

            X1 = d1.drop(['date'], axis=1).reindex(columns=keiba_ai._KeibaAI__datasets.X_test.columns)
            score_1 = keiba_ai.calc_score(X1, policies.BasicScorePolicy)
            score_1.rename(columns={'score': 'score_x'}, inplace=True)
            df_L3F = score_1.rename(columns={'score_x': 'L3F'}, inplace=True)
            print(df_L3F)
            df_L3F = preparing.add_L3F_features_2(df_L3F)
            
            d2 = d1.merge(df_L3F,  on=['馬番'], how='left')
            print(d2)
            
            X2 = d1.drop(['date'], axis=1).reindex(columns=keiba_ai2._KeibaAI__datasets.X_test.columns)
            
            X3 = d1.drop(['date'], axis=1).reindex(columns=keiba_ai3._KeibaAI__datasets.X_test.columns)
            
            X4 = d1.drop(['date'], axis=1).reindex(columns=keiba_ai4._KeibaAI__datasets.X_test.columns)
            
            X5 = d2.drop(['date'], axis=1).reindex(columns=keiba_ai5._KeibaAI__datasets.X_test.columns)   # L3F 使用
        
            X6 = d1.drop(['date'], axis=1).reindex(columns=keiba_ai6._KeibaAI__datasets.X_test.columns)
            


            # score_1 = keiba_ai.calc_score(X1, policies.BasicScorePolicy)
            score_2 = keiba_ai2.calc_score(X2, policies.BasicScorePolicy)
            score_3 = keiba_ai3.calc_score(X3, policies.BasicScorePolicy)
            score_4 = keiba_ai4.calc_score(X4, policies.BasicScorePolicy)
            score_5 = keiba_ai4.calc_score(X5, policies.BasicScorePolicy)
            score_6 = keiba_ai4.calc_score(X6, policies.BasicScorePolicy)
            
            # scores_0 = score_1.merge(score_2, on=['race_id', '馬番'], how='left')
            # scores_0 = scores_0.merge(score_3, on=['race_id', '馬番'], how='left')
            # scores_0 = scores_0.merge(score_4, on=['race_id', '馬番'], how='left')
            
            # score_1.rename(columns={'score': 'score_x'}, inplace=True)
            score_2.rename(columns={'score': 'score_y'}, inplace=True)
            score_3.rename(columns={'score': 'score_z'}, inplace=True)
            score_4.rename(columns={'score': 'score_w'}, inplace=True)
            score_5.rename(columns={'score': 'score_v'}, inplace=True)
            score_6.rename(columns={'score': 'score_u'}, inplace=True)
            dfs = [score_1, score_2, score_3, score_4, score_5, score_6]
            # print(score_4)
            from functools import reduce
            scores_0 = reduce(lambda left, right: left.merge(right, on=['race_id', '馬番'], how='left'), dfs)
            scores = scores_0.merge(X1, on=['race_id', '馬番'], how='left')

            
            # 当日の出走情報テーブル（前処理前）
            df_tmp = shutuba_table_processor.raw_data[:1] 
            i = 0
            for num in list(Master.PLACE_DICT.values()):
                if num == race_id[4:6]:
                    loc = list(Master.PLACE_DICT)[i]
                    R = race_id[10:12]
                i += 1
            
            
            return (scores, loc, R, df_tmp, nisai, hinba)