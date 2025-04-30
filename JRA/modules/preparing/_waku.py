import os
import time
from tqdm.notebook import tqdm
import requests
import pandas as pd
import bs4


#参考(検定を使用)　https://cani.fool.jp/total/waku/1wakuindex.htm
def waku (df : pd.DataFrame) -> pd.DataFrame:
    
    #札幌競馬場
    if df['開催_01'] == True:
        if['course_type_芝'] == True:
            if df['course_len'] == 12.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 70.2
                elif df['枠'] == 2:
                    df['枠別勝率'] = 54.3
                elif df['枠'] == 3:
                    df['枠別勝率'] = 64.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 67.4
                elif df['枠'] == 5:
                    df['枠別勝率'] = 79.4
                elif df['枠'] == 6:
                    df['枠別勝率'] = 74.3
                elif df['枠'] == 7:
                    df['枠別勝率'] = 82.1
                elif df['枠'] == 8:
                    df['枠別勝率'] = 90.2
                    
            if df['course_len'] == 15.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 74.1
                elif df['枠'] == 2:
                    df['枠別勝率'] = 79.9
                elif df['枠'] == 3:
                    df['枠別勝率'] = 73.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 68.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 63.2
                elif df['枠'] == 6:
                    df['枠別勝率'] = 82.9
                elif df['枠'] == 7:
                    df['枠別勝率'] = 71.7
                elif df['枠'] == 8:
                    df['枠別勝率'] = 64.7
                    
            if df['course_len'] == 18.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 92.0
                elif df['枠'] == 2:
                    df['枠別勝率'] = 74.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 59.4
                elif df['枠'] == 4:
                    df['枠別勝率'] = 75.4
                elif df['枠'] == 5:
                    df['枠別勝率'] = 60.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 52.0
                elif df['枠'] == 7:
                    df['枠別勝率'] = 95.5
                elif df['枠'] == 8:
                    df['枠別勝率'] = 73.5
                    
            if df['course_len'] == 20.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 83.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 74.9
                elif df['枠'] == 3:
                    df['枠別勝率'] = 69.1
                elif df['枠'] == 4:
                    df['枠別勝率'] = 57.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 87.8
                elif df['枠'] == 6:
                    df['枠別勝率'] = 68.6
                elif df['枠'] == 7:
                    df['枠別勝率'] = 64.2
                elif df['枠'] == 8:
                    df['枠別勝率'] = 67.3
                    
            if df['course_len'] == 26.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 76.7
                elif df['枠'] == 2:
                    df['枠別勝率'] = 97.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 59.8
                elif df['枠'] == 4:
                    df['枠別勝率'] = 59.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 68.0
                elif df['枠'] == 6:
                    df['枠別勝率'] = 64.0
                elif df['枠'] == 7:
                    df['枠別勝率'] = 53.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 94.9  
                    
        elif['course_type_ダ'] == True:
            if df['course_len'] == 10.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 56.4
                elif df['枠'] == 2:
                    df['枠別勝率'] = 53.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 56.0
                elif df['枠'] == 4:
                    df['枠別勝率'] = 66.7
                elif df['枠'] == 5:
                    df['枠別勝率'] = 72.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 68.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 99.6
                elif df['枠'] == 8:
                    df['枠別勝率'] = 76.7
                    
            if df['course_len'] == 17.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 75.3
                elif df['枠'] == 2:
                    df['枠別勝率'] = 51.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 53.9
                elif df['枠'] == 4:
                    df['枠別勝率'] = 74.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 73.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 98.9
                elif df['枠'] == 7:
                    df['枠別勝率'] = 84.4
                elif df['枠'] == 8:
                    df['枠別勝率'] = 70.8
                    
            if df['course_len'] == 24.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 65.7
                elif df['枠'] == 2:
                    df['枠別勝率'] = 56.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 56.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 70.9
                elif df['枠'] == 5:
                    df['枠別勝率'] = 61.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 60.7
                elif df['枠'] == 7:
                    df['枠別勝率'] = 90.4
                elif df['枠'] == 8:
                    df['枠別勝率'] = 76.7     
            
    # 函館競馬場
    elif df['開催_02'] == True:
        if['course_type_芝'] == True:
            if df['course_len'] == 12.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 72.9
                elif df['枠'] == 2:
                    df['枠別勝率'] = 82.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 54.1
                elif df['枠'] == 4:
                    df['枠別勝率'] = 76.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 71.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 87.2
                elif df['枠'] == 7:
                    df['枠別勝率'] = 58.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 74.2
                
            if df['course_len'] == 18.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 57.3
                elif df['枠'] == 2:
                    df['枠別勝率'] = 72.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 88.1
                elif df['枠'] == 4:
                    df['枠別勝率'] = 64.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 72.5
                elif df['枠'] == 6:
                    df['枠別勝率'] = 76.8
                elif df['枠'] == 7:
                    df['枠別勝率'] = 72.4
                elif df['枠'] == 8:
                    df['枠別勝率'] = 74.5
                    
            if df['course_len'] == 20.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 68.5
                elif df['枠'] == 2:
                    df['枠別勝率'] = 83.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 52.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 74.6
                elif df['枠'] == 5:
                    df['枠別勝率'] = 94.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 95.8
                elif df['枠'] == 7:
                    df['枠別勝率'] = 59.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 50.7
                    
            if df['course_len'] == 26.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 70.8
                elif df['枠'] == 2:
                    df['枠別勝率'] = 75.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 89.0
                elif df['枠'] == 4:
                    df['枠別勝率'] = 65.2
                elif df['枠'] == 5:
                    df['枠別勝率'] = 68.8
                elif df['枠'] == 6:
                    df['枠別勝率'] = 79.3
                elif df['枠'] == 7:
                    df['枠別勝率'] = 78.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 66.7
                    
        elif['course_type_ダ'] == True:
            if df['course_len'] == 10.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 82.2
                elif df['枠'] == 2:
                    df['枠別勝率'] = 76.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 91.8
                elif df['枠'] == 4:
                    df['枠別勝率'] = 56.6
                elif df['枠'] == 5:
                    df['枠別勝率'] = 60.3
                elif df['枠'] == 6:
                    df['枠別勝率'] = 85.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 54.4
                elif df['枠'] == 8:
                    df['枠別勝率'] = 84.1
                    
            if df['course_len'] == 17.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 87.7
                elif df['枠'] == 2:
                    df['枠別勝率'] = 64.8
                elif df['枠'] == 3:
                    df['枠別勝率'] = 90.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 50.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 87.3
                elif df['枠'] == 6:
                    df['枠別勝率'] = 66.9
                elif df['枠'] == 7:
                    df['枠別勝率'] = 87.6
                elif df['枠'] == 8:
                    df['枠別勝率'] = 63.9
                    
            if df['course_len'] == 24.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 62.8
                elif df['枠'] == 2:
                    df['枠別勝率'] = 50.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 51.4
                elif df['枠'] == 4:
                    df['枠別勝率'] = 73.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 75.9
                elif df['枠'] == 6:
                    df['枠別勝率'] = 57.0
                elif df['枠'] == 7:
                    df['枠別勝率'] = 91.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 79.3
                    
    elif df['開催_03'] == True:
        if['course_type_芝'] == True:
            if df['course_len'] == 10.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 65.9
                elif df['枠'] == 2:
                    df['枠別勝率'] = 73.1
                elif df['枠'] == 3:
                    df['枠別勝率'] = 81.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 63.8
                elif df['枠'] == 5:
                    df['枠別勝率'] = 83.8
                elif df['枠'] == 6:
                    df['枠別勝率'] = 53.0
                elif df['枠'] == 7:
                    df['枠別勝率'] = 78.8
                elif df['枠'] == 8:
                    df['枠別勝率'] = 82.2
                    
            if df['course_len'] == 12.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 98.1
                elif df['枠'] == 2:
                    df['枠別勝率'] = 97.6
                elif df['枠'] == 3:
                    df['枠別勝率'] = 84.8
                elif df['枠'] == 4:
                    df['枠別勝率'] = 77.2
                elif df['枠'] == 5:
                    df['枠別勝率'] = 53.2
                elif df['枠'] == 6:
                    df['枠別勝率'] = 60.3
                elif df['枠'] == 7:
                    df['枠別勝率'] = 53.8
                elif df['枠'] == 8:
                    df['枠別勝率'] = 67.2
                    
            if df['course_len'] == 17.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 87.9
                elif df['枠'] == 2:
                    df['枠別勝率'] = 62.6
                elif df['枠'] == 3:
                    df['枠別勝率'] = 79.3
                elif df['枠'] == 4:
                    df['枠別勝率'] = 76.6
                elif df['枠'] == 5:
                    df['枠別勝率'] = 72.2
                elif df['枠'] == 6:
                    df['枠別勝率'] = 74.7
                elif df['枠'] == 7:
                    df['枠別勝率'] = 70.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 55.3
                    
            if df['course_len'] == 18.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 55.9
                elif df['枠'] == 2:
                    df['枠別勝率'] = 74.6
                elif df['枠'] == 3:
                    df['枠別勝率'] = 95.3
                elif df['枠'] == 4:
                    df['枠別勝率'] = 90.9
                elif df['枠'] == 5:
                    df['枠別勝率'] = 79.5
                elif df['枠'] == 6:
                    df['枠別勝率'] = 61.6
                elif df['枠'] == 7:
                    df['枠別勝率'] = 62.5
                elif df['枠'] == 8:
                    df['枠別勝率'] = 57.6
                    
            if df['course_len'] == 20.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 61.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 65.4
                elif df['枠'] == 3:
                    df['枠別勝率'] = 84.2
                elif df['枠'] == 4:
                    df['枠別勝率'] = 94.4
                elif df['枠'] == 5:
                    df['枠別勝率'] = 85.2
                elif df['枠'] == 6:
                    df['枠別勝率'] = 70.0
                elif df['枠'] == 7:
                    df['枠別勝率'] = 61.4
                elif df['枠'] == 8:
                    df['枠別勝率'] = 58.9
                    
            if df['course_len'] == 26.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 70.7
                elif df['枠'] == 2:
                    df['枠別勝率'] = 88.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 81.4
                elif df['枠'] == 4:
                    df['枠別勝率'] = 59.8
                elif df['枠'] == 5:
                    df['枠別勝率'] = 69.0
                elif df['枠'] == 6:
                    df['枠別勝率'] = 68.3
                elif df['枠'] == 7:
                    df['枠別勝率'] = 60.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 72.3
        
        elif['course_type_ダ'] == True:
            if df['course_len'] == 10.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 93.0
                elif df['枠'] == 2:
                    df['枠別勝率'] = 84.1
                elif df['枠'] == 3:
                    df['枠別勝率'] = 72.2
                elif df['枠'] == 4:
                    df['枠別勝率'] = 88.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 71.8
                elif df['枠'] == 6:
                    df['枠別勝率'] = 65.3
                elif df['枠'] == 7:
                    df['枠別勝率'] = 56.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 68.7
                    
            if df['course_len'] == 11.5:
                if df['枠'] == 1:
                    df['枠別勝率'] = 89.9
                elif df['枠'] == 2:
                    df['枠別勝率'] = 54.4
                elif df['枠'] == 3:
                    df['枠別勝率'] = 94.6
                elif df['枠'] == 4:
                    df['枠別勝率'] = 73.2
                elif df['枠'] == 5:
                    df['枠別勝率'] = 69.4
                elif df['枠'] == 6:
                    df['枠別勝率'] = 57.9
                elif df['枠'] == 7:
                    df['枠別勝率'] = 50.3
                elif df['枠'] == 8:
                    df['枠別勝率'] = 98.4
                    
            if df['course_len'] == 17.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 65.1
                elif df['枠'] == 2:
                    df['枠別勝率'] = 83.5
                elif df['枠'] == 3:
                    df['枠別勝率'] = 79.9
                elif df['枠'] == 4:
                    df['枠別勝率'] = 65.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 57.9
                elif df['枠'] == 6:
                    df['枠別勝率'] = 86.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 67.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 85.1
                    
            if df['course_len'] == 24.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 76.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 76.6
                elif df['枠'] == 3:
                    df['枠別勝率'] = 70.9
                elif df['枠'] == 4:
                    df['枠別勝率'] = 74.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 53.8
                elif df['枠'] == 6:
                    df['枠別勝率'] = 73.7
                elif df['枠'] == 7:
                    df['枠別勝率'] = 72.3
                elif df['枠'] == 8:
                    df['枠別勝率'] = 57.7
                    
    elif df['開催_04'] == True:             
        if['course_type_芝'] == True:
            if df['course_len'] == 12.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 51.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 84.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 52.4
                elif df['枠'] == 4:
                    df['枠別勝率'] = 66.9
                elif df['枠'] == 5:
                    df['枠別勝率'] = 82.2
                elif df['枠'] == 6:
                    df['枠別勝率'] = 88.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 84.6
                elif df['枠'] == 8:
                    df['枠別勝率'] = 79.8
                    
            if df['course_len'] == 14.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 75.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 74.5
                elif df['枠'] == 3:
                    df['枠別勝率'] = 61.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 70.3
                elif df['枠'] == 5:
                    df['枠別勝率'] = 58.9
                elif df['枠'] == 6:
                    df['枠別勝率'] = 75.7
                elif df['枠'] == 7:
                    df['枠別勝率'] = 66.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 93.5
                    
            if df['course_len'] == 20.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 80.3
                elif df['枠'] == 2:
                    df['枠別勝率'] = 50.4
                elif df['枠'] == 3:
                    df['枠別勝率'] = 67.0
                elif df['枠'] == 4:
                    df['枠別勝率'] = 66.3
                elif df['枠'] == 5:
                    df['枠別勝率'] = 87.4
                elif df['枠'] == 6:
                    df['枠別勝率'] = 70.5
                elif df['枠'] == 7:
                    df['枠別勝率'] = 86.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 75.1
                    
            if df['course_len'] == 22.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 75.3
                elif df['枠'] == 2:
                    df['枠別勝率'] = 70.1
                elif df['枠'] == 3:
                    df['枠別勝率'] = 76.3
                elif df['枠'] == 4:
                    df['枠別勝率'] = 71.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 65.6
                elif df['枠'] == 6:
                    df['枠別勝率'] = 78.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 63.7
                elif df['枠'] == 8:
                    df['枠別勝率'] = 74.5
                    
            if df['course_len'] == 24.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 51.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 61.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 69.2
                elif df['枠'] == 4:
                    df['枠別勝率'] = 94.6
                elif df['枠'] == 5:
                    df['枠別勝率'] = 50.8
                elif df['枠'] == 6:
                    df['枠別勝率'] = 90.3
                elif df['枠'] == 7:
                    df['枠別勝率'] = 69.8
                elif df['枠'] == 8:
                    df['枠別勝率'] = 81.6
                    
            if df['course_len'] == 10.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 50.1
                elif df['枠'] == 2:
                    df['枠別勝率'] = 56.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 50.5
                elif df['枠'] == 4:
                    df['枠別勝率'] = 50.3
                elif df['枠'] == 5:
                    df['枠別勝率'] = 51.9
                elif df['枠'] == 6:
                    df['枠別勝率'] = 96.9
                elif df['枠'] == 7:
                    df['枠別勝率'] = 98.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 100.0
                    
            if df['course_len'] == 16.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 56.3
                elif df['枠'] == 2:
                    df['枠別勝率'] = 73.9
                elif df['枠'] == 3:
                    df['枠別勝率'] = 73.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 63.3
                elif df['枠'] == 5:
                    df['枠別勝率'] = 92.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 60.6
                elif df['枠'] == 7:
                    df['枠別勝率'] = 90.7
                elif df['枠'] == 8:
                    df['枠別勝率'] = 67.0
                    
            if df['course_len'] == 18.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 62.0
                elif df['枠'] == 2:
                    df['枠別勝率'] = 88.5
                elif df['枠'] == 3:
                    df['枠別勝率'] = 80.2
                elif df['枠'] == 4:
                    df['枠別勝率'] = 68.4
                elif df['枠'] == 5:
                    df['枠別勝率'] = 66.7
                elif df['枠'] == 6:
                    df['枠別勝率'] = 62.1
                elif df['枠'] == 7:
                    df['枠別勝率'] = 84.3
                elif df['枠'] == 8:
                    df['枠別勝率'] = 74.5
                    
            if df['course_len'] == 20.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 68.0
                elif df['枠'] == 2:
                    df['枠別勝率'] = 79.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 84.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 66.9
                elif df['枠'] == 5:
                    df['枠別勝率'] = 63.6
                elif df['枠'] == 6:
                    df['枠別勝率'] = 58.6
                elif df['枠'] == 7:
                    df['枠別勝率'] = 62.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 88.1
                    
        elif['course_type_ダ'] == True:
            if df['course_len'] == 12.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 52.5
                elif df['枠'] == 2:
                    df['枠別勝率'] = 61.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 64.4
                elif df['枠'] == 4:
                    df['枠別勝率'] = 92.4
                elif df['枠'] == 5:
                    df['枠別勝率'] = 59.8
                elif df['枠'] == 6:
                    df['枠別勝率'] = 73.7
                elif df['枠'] == 7:
                    df['枠別勝率'] = 97.5
                elif df['枠'] == 8:
                    df['枠別勝率'] = 71.4
                    
            elif df['course_len'] == 18.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 55.4
                elif df['枠'] == 2:
                    df['枠別勝率'] = 57.5
                elif df['枠'] == 3:
                    df['枠別勝率'] = 60.9
                elif df['枠'] == 4:
                    df['枠別勝率'] = 59.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 99.5
                elif df['枠'] == 6:
                    df['枠別勝率'] = 81.6
                elif df['枠'] == 7:
                    df['枠別勝率'] = 75.1
                elif df['枠'] == 8:
                    df['枠別勝率'] = 84.5
                    
            elif df['course_len'] == 25.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 52.7
                elif df['枠'] == 2:
                    df['枠別勝率'] = 52.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 76.6
                elif df['枠'] == 4:
                    df['枠別勝率'] = 50.0
                elif df['枠'] == 5:
                    df['枠別勝率'] = 77.0
                elif df['枠'] == 6:
                    df['枠別勝率'] = 67.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 81.3
                elif df['枠'] == 8:
                    df['枠別勝率'] = 83.1
                    
    elif df['開催_05'] == True:
        if df['course_type_芝'] == True:
            if df['course_len'] == 14.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 52.5
                elif df['枠'] == 2:
                    df['枠別勝率'] = 55.6
                elif df['枠'] == 3:
                    df['枠別勝率'] = 85.3
                elif df['枠'] == 4:
                    df['枠別勝率'] = 78.0
                elif df['枠'] == 5:
                    df['枠別勝率'] = 77.4
                elif df['枠'] == 6:
                    df['枠別勝率'] = 86.9
                elif df['枠'] == 7:
                    df['枠別勝率'] = 69.5
                elif df['枠'] == 8:
                    df['枠別勝率'] = 91.1
                    
            elif df['course_len'] == 16.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 85.9
                elif df['枠'] == 2:
                    df['枠別勝率'] = 68.5
                elif df['枠'] == 3:
                    df['枠別勝率'] = 65.8
                elif df['枠'] == 4:
                    df['枠別勝率'] = 57.0
                elif df['枠'] == 5:
                    df['枠別勝率'] = 59.6
                elif df['枠'] == 6:
                    df['枠別勝率'] = 86.5
                elif df['枠'] == 7:
                    df['枠別勝率'] = 76.6
                elif df['枠'] == 8:
                    df['枠別勝率'] = 81.3
                    
            elif df['course_len'] == 18.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 64.3
                elif df['枠'] == 2:
                    df['枠別勝率'] = 88.3
                elif df['枠'] == 3:
                    df['枠別勝率'] = 66.6
                elif df['枠'] == 4:
                    df['枠別勝率'] = 91.8
                elif df['枠'] == 5:
                    df['枠別勝率'] = 78.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 55.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 82.5
                elif df['枠'] == 8:
                    df['枠別勝率'] = 54.7
                    
            elif df['course_len'] == 20.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 78.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 53.1
                elif df['枠'] == 3:
                    df['枠別勝率'] = 71.6
                elif df['枠'] == 4:
                    df['枠別勝率'] = 74.3
                elif df['枠'] == 5:
                    df['枠別勝率'] = 93.3
                elif df['枠'] == 6:
                    df['枠別勝率'] = 79.4
                elif df['枠'] == 7:
                    df['枠別勝率'] = 69.6
                elif df['枠'] == 8:
                    df['枠別勝率'] = 62.6
                    
            elif df['course_len'] == 23.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 68.8
                elif df['枠'] == 2:
                    df['枠別勝率'] = 81.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 51.3
                elif df['枠'] == 4:
                    df['枠別勝率'] = 61.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 75.3
                elif df['枠'] == 6:
                    df['枠別勝率'] = 80.9
                elif df['枠'] == 7:
                    df['枠別勝率'] = 84.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 51.4
                    
            elif df['course_len'] == 24.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 78.8
                elif df['枠'] == 2:
                    df['枠別勝率'] = 50.5
                elif df['枠'] == 3:
                    df['枠別勝率'] = 78.6
                elif df['枠'] == 4:
                    df['枠別勝率'] = 63.5
                elif df['枠'] == 5:
                    df['枠別勝率'] = 81.5
                elif df['枠'] == 6:
                    df['枠別勝率'] = 88.5
                elif df['枠'] == 7:
                    df['枠別勝率'] = 60.8
                elif df['枠'] == 8:
                    df['枠別勝率'] = 86.2
                    
            elif df['course_len'] == 25.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 69.1
                elif df['枠'] == 2:
                    df['枠別勝率'] = 53.5
                elif df['枠'] == 3:
                    df['枠別勝率'] = 62.4
                elif df['枠'] == 4:
                    df['枠別勝率'] = 84.9
                elif df['枠'] == 5:
                    df['枠別勝率'] = 80.9
                elif df['枠'] == 6:
                    df['枠別勝率'] = 84.0
                elif df['枠'] == 7:
                    df['枠別勝率'] = 52.7
                elif df['枠'] == 8:
                    df['枠別勝率'] = 67.3
                    
            elif df['course_len'] == 34.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 56.0
                elif df['枠'] == 2:
                    df['枠別勝率'] = 76.9
                elif df['枠'] == 3:
                    df['枠別勝率'] = 62.1
                elif df['枠'] == 4:
                    df['枠別勝率'] = 54.7
                elif df['枠'] == 5:
                    df['枠別勝率'] = 54.7
                elif df['枠'] == 6:
                    df['枠別勝率'] = 73.3
                elif df['枠'] == 7:
                    df['枠別勝率'] = 59.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 83.3
            
        elif df['course_type_ダ'] == True:
            if df['course_len'] == 13.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 95.3
                elif df['枠'] == 2:
                    df['枠別勝率'] = 94.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 68.2
                elif df['枠'] == 4:
                    df['枠別勝率'] = 53.7
                elif df['枠'] == 5:
                    df['枠別勝率'] = 78.7
                elif df['枠'] == 6:
                    df['枠別勝率'] = 80.6
                elif df['枠'] == 7:
                    df['枠別勝率'] = 55.7
                elif df['枠'] == 8:
                    df['枠別勝率'] = 62.5
                    
            elif df['course_len'] == 14.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 59.6
                elif df['枠'] == 2:
                    df['枠別勝率'] = 71.9
                elif df['枠'] == 3:
                    df['枠別勝率'] = 63.4
                elif df['枠'] == 4:
                    df['枠別勝率'] = 86.3
                elif df['枠'] == 5:
                    df['枠別勝率'] = 52.4
                elif df['枠'] == 6:
                    df['枠別勝率'] = 96.8
                elif df['枠'] == 7:
                    df['枠別勝率'] = 91.0
                elif df['枠'] == 8:
                    df['枠別勝率'] = 75.6
                    
            elif df['course_len'] == 16.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 51.8
                elif df['枠'] == 2:
                    df['枠別勝率'] = 60.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 53.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 51.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 76.5
                elif df['枠'] == 6:
                    df['枠別勝率'] = 87.2
                elif df['枠'] == 7:
                    df['枠別勝率'] = 96.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 99.4
                    
            elif df['course_len'] == 21.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 52.5
                elif df['枠'] == 2:
                    df['枠別勝率'] = 50.7
                elif df['枠'] == 3:
                    df['枠別勝率'] = 89.6
                elif df['枠'] == 4:
                    df['枠別勝率'] = 80.2
                elif df['枠'] == 5:
                    df['枠別勝率'] = 85.1
                elif df['枠'] == 6:
                    df['枠別勝率'] = 95.6
                elif df['枠'] == 7:
                    df['枠別勝率'] = 70.3
                elif df['枠'] == 8:
                    df['枠別勝率'] = 66.3
                    
            elif df['course_len'] == 24.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 50.0
                elif df['枠'] == 2:
                    df['枠別勝率'] = 50.0
                elif df['枠'] == 3:
                    df['枠別勝率'] = 50.0
                elif df['枠'] == 4:
                    df['枠別勝率'] = 52.6
                elif df['枠'] == 5:
                    df['枠別勝率'] = 69.6
                elif df['枠'] == 6:
                    df['枠別勝率'] = 77.5
                elif df['枠'] == 7:
                    df['枠別勝率'] = 93.2
                elif df['枠'] == 8:
                    df['枠別勝率'] = 84.0
            
    elif df['開催_06'] == True:
        if df['course_type_芝'] == True:
            if df['course_len'] == 16.0:
                if df['枠'] == 1:
                    df['枠別勝率'] = 51.8
                elif df['枠'] == 2:
                    df['枠別勝率'] = 60.2
                elif df['枠'] == 3:
                    df['枠別勝率'] = 53.7
                elif df['枠'] == 4:
                    df['枠別勝率'] = 51.1
                elif df['枠'] == 5:
                    df['枠別勝率'] = 76.5
                elif df['枠'] == 6:
                    df['枠別勝率'] = 87.2
                elif df['枠'] == 7:
                    df['枠別勝率'] = 96.9
                elif df['枠'] == 8:
                    df['枠別勝率'] = 99.4
            
            
            

        
    return df