# 4단계 : 각 영상 정보 일반화시킨 후에 날짜별로 가장 큰 조회수 가진 것으로 구성.
# youtube_brain_out_video_regul.csv의 정보에서 날짜별로 가장 큰 값만 표시 - date, count 만 표시.
#
import pandas as pd
import os
from pandas import DataFrame

game_name = 'crazy_shopping' #'tatto_tycoon' #'brain_out'
game_full_name = 'Crazy Shopping'#'Ink Inc. - Tattoo Tycoon' #'Brain Out – 가장 어색한 게임'
result = []
try:
    youtube_data = pd.read_csv('./youtube_'+game_name+'_video_regul.csv', sep=',', header=0, encoding='utf-8-sig')
except:
    youtube_data = pd.read_csv('./youtube_'+game_name+'_video_regul.csv', sep=',', header=0, encoding='cp949')

# youtube 데이터에는 영상이 없는날은 date가 없기 때문에 game data에서 date 가져오자
try:
    day_data = pd.read_csv('./game_rank_data_top3.csv', sep=',', header=0, encoding='utf-8-sig')
except:
    day_data = pd.read_csv('./game_rank_data_top3.csv', sep=',', header=0, encoding='cp949')

brain_out_data = day_data[day_data['name']==game_full_name]
date_uni = brain_out_data['date'].unique()

for day in date_uni:                                # 각 date에서
    data = youtube_data[youtube_data['date']==day] # 같은날짜의 데이터 가져옴
    if( len(data.values) == 0 ):
        max_count = 0
        day_count = 0
    else :
        max_count = 0
        day_count = 0
        now_youtuber = []
        for info in data.values: # 같은날짜 데이터에서 가장 큰 값 출력
            now_count = int(info[1].replace(',',''))
            if(max_count < now_count):
                max_count = now_count
                print(max_count)
            if info[5] in now_youtuber: # 그날올린 영상을 같은사람이 했으면 day_count안함
                #print("얘는 day_count에서 빼보자, 오늘 영상수:"+str(day_count))
                continue
            day_count += 1
            now_youtuber.append(info[5])
        print(max_count)
        print("================")
        
    result.append([day] + [max_count] + [day_count])
youtube_table = pd.DataFrame(result, columns=('date', 'count', 'content_count'))
youtube_table = youtube_table.sort_values(by=['date'], axis=0)
youtube_table.to_csv("./youtube_"+game_name+"_count_each_date.csv", encoding="utf-8-sig", mode='w', index=False)
