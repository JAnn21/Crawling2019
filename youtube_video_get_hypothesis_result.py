# 4단계 : 각 영상 정보 일반화시킨 후에 날짜별로 가장 큰 조회수 가진 것으로 구성.
# youtube_brain_out_video_regul.csv의 정보에서 날짜별로 가장 큰 값만 표시 - date, count 만 표시.
#
import pandas as pd
import os
from pandas import DataFrame
import datetime as dt
game_name = 'brain_out'#'crazy_shopping' #'tatto_tycoon' #'brain_out'
game_full_name = 'Brain Out – 가장 어색한 게임'#'Crazy Shopping'#'Ink Inc. - Tattoo Tycoon' #'Brain Out – 가장 어색한 게임'

result = []

# date, count, content_count 있음.
try:
    youtube_data = pd.read_csv('./youtube_'+game_name+'_count_each_date.csv', sep=',', header=0, encoding='utf-8-sig')
except:
    youtube_data = pd.read_csv('./youtube_'+game_name+'_count_each_date.csv', sep=',', header=0, encoding='cp949')

# name, date, rank, diff 있음.
try:
    rank_data = pd.read_csv('./game_rank_data_top3.csv', sep=',', header=0, encoding='utf-8-sig')
except:
    rank_data = pd.read_csv('./game_rank_data_top3.csv', sep=',', header=0, encoding='cp949')

rank_data = rank_data[rank_data['name'] == game_full_name]



# count(조회수) 가장 높은 5개 시점 조사, high_count, high_count_date, high_count_rank 가져오기.
high_count_data = youtube_data.sort_values(by=['count'], axis=0, ascending=False)
high_count_data = high_count_data.values[:5]

'''
array([['2019_10_20', 668476, 6],
       ['2019_10_04', 566125, 5],
       ['2019_11_24', 346565, 11],
       ['2019_10_03', 320225, 2],
       ['2019_10_29', 238827, 3]], dtype=object)
'''
high_counts = [x[1] for x in high_count_data]      # [668476, 566125, 346565, 320225, 238827]
high_count_dates = [x[0] for x in high_count_data] # ['2019_10_20', '2019_10_04', '2019_11_24', '2019_10_03', '2019_10_29']

high_count_ranks = []                              # [1, 3, 2, 3, 3]
for h_date in high_count_dates:
    high_count_rank = rank_data[rank_data['date']==h_date].values
    high_count_ranks.append(high_count_rank[0][2])
print(high_count_ranks)


# 다 가져온 뒤 high_count_date 다음날 랭크 조사
next_ranks = []
for date in high_count_dates:
    next_date = dt.datetime.strptime(str(date),'%Y_%m_%d')
    next_date = next_date + dt.timedelta(days=1)

    next_date_tuple = next_date.timetuple()
    next_date = str(next_date_tuple[0])+"_"+'%02d'%next_date_tuple[1]+"_"+'%02d'%next_date_tuple[2] # 2019_10_21

    next_rank = rank_data[rank_data['date']==next_date]
    next_rank = next_rank.values[0][2]
    next_ranks.append(next_rank) 

print(next_ranks) # [1, 3, 1, 3, 2]

# high_count_rank <= next_rank = true

# 순위별로 정렬, 순위 높은 3개(1위 2개, 2위 3개, 3위 1개 -> 6개) 그날의 contents 개수 파악, 평균값 계산.
rank_data_sort = rank_data.sort_values(by=['rank'], axis=0) # 오름차순
rank_uni = rank_data_sort['rank'].unique()
rank_list = rank_uni[:3]
unrank_list = rank_uni[3:]

high_rank_contents = []
for rank in rank_list: 
    high_rank_data = rank_data[rank_data['rank']==rank] # 1위인것 가져오고,
    for date in high_rank_data.values:
        contents = youtube_data[youtube_data['date']==date[1]].values # 1위인것 날짜에 따른 컨텐츠개수 파악
        contents = contents[0][2]
        high_rank_contents.append(contents)

print(high_rank_contents) # 4, 2, 0, 4, 8, 11, ...

low_rank_contents = []
for rank in unrank_list: 
    high_rank_data = rank_data[rank_data['rank']==rank] # 1위인것 가져오고,
    for date in high_rank_data.values:
        contents = youtube_data[youtube_data['date']==date[1]].values # 1위인것 날짜에 따른 컨텐츠개수 파악
        contents = contents[0][2]
        low_rank_contents.append(contents)   
print(low_rank_contents) # 4, 2, 0, 4, 8, 11, ...

high_rank_contents_count = sum(high_rank_contents) / len(high_rank_contents)
low_rank_contents_count = sum(low_rank_contents) / len(low_rank_contents)

print(high_rank_contents_count)
print(low_rank_contents_count)


# 결과
# 각 게임 순위 높을때 contents 수 많은가
if(high_rank_contents_count > low_rank_contents_count):
    hypothesis = True
else:
    hypothesis = False

# 유튜브 조회수가 많을때 다음날에 게임 순위가 올랐는가
h2_result = []
t = 0
f = 0
for i in range(0, 5):
    h_rank = high_count_ranks[i]
    n_rank = next_ranks[i]
    if(h_rank >= n_rank):
        h2_result.append(True)
        t += 1
    else:
        h2_result.append(False)
        f += 1

print(h2_result)
if(t >= f):
    hypothesis2 = True
else:
    hypothesis2 = False

h_c_r = str(high_count_ranks)
n_r = str(next_ranks)

result.append([game_full_name] + ["%.2f"%high_rank_contents_count] + ["%.2f"%low_rank_contents_count] + [high_counts[0]] + [high_count_dates[0]] + [h_c_r] + [n_r] + [hypothesis] + [hypothesis2])

print(result)
'''
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
'''
