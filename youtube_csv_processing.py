# 3단계 : youtube_video_crawling.py에서 가져온 데이터 일반화시키기
# youtube_video_csv_processing의 정보에서 조회수, 날짜, 좋아요, 싫어요, 구독자
# 형태 일반화시키기

import pandas as pd
import os
from pandas import DataFrame

game_name = 'crazy_shopping'#'tatto_tycoon' #'brain_out'
def count_processing(count):
    if("없음" in count):
        count = 0
    else:
        count = count[4:-1]  # 조회수 15회 -> 15
    #print(count)   
    return str(count)

def date_processing(date):
    num = date.replace(' ', '') # 2019. 12. 3. -> 2019.12.3.
    num = num.split('.') # 2019.12.3. -> ['2019', '12', '2', '']
    if(("실시간" in num[0]) or ("최초" in num[0])):
        num[0]=num[0][-4:]
    if(int(num[1]) < 10):
        num[1] = '0'+num[1] # 9 -> 09
    if(int(num[2]) < 10):
        num[2] = '0'+num[2]  # 2 -> 02
    #print("date : "+num[0]+num[1]+num[2])
    return str(num[0]+"_"+num[1]+"_"+num[2]) # 2019_12_03

def good_count_processing(good_count): # 좋아요 없애기, 3.7천 -> 3.7*1000=3700으로 반환하기
    if(good_count == '좋아요'):
        good_count = 0
    elif("천" in good_count):
        good_count = good_count.replace('천', '')
        good_count = int(float(good_count)*1000)
    elif("만" in good_count):
        good_count = good_count.replace('만', '')
        good_count = int(float(good_count)*10000)
    #print("good : "+str(good_count))
    return str(good_count)

def bad_count_processing(bad_count): # 싫어요 없애기, 3.7천 -> 3.7*1000=3700으로 반환하기
    if(bad_count == '싫어요'):
        bad_count = 0
    elif("천" in bad_count):
        bad_count = bad_count.replace('천', '')
        bad_count = int(float(bad_count)*1000)
    elif("만" in bad_count):
        bad_count = bad_count.replace('만', '')
        bad_count = int(float(bad_count)*10000)
    #print("bad : "+str(bad_count))
    return str(bad_count)

def subscriber_processing(subscriber): # 구독자 36만명 -> 360000으로 반환
    if(str(subscriber)=='nan'):             # 아무것도없으면 0으로
        subscriber=0
    else:
        subscriber = subscriber[4:-1] # 구독자 36만명 -> 36만
        if("천" in subscriber):
            subscriber = subscriber.replace('천', '')
            subscriber = int(float(subscriber)*1000)
        elif("만" in subscriber):
            subscriber = subscriber.replace('만', '')
            subscriber = int(float(subscriber)*10000)
            
    return str(subscriber)
    
# 유튜브 정보 가져옴

result = []
try:
    youtube_data = pd.read_csv('./youtube_'+game_name+'_video.csv', sep=',', header=0, encoding='utf-8-sig')
except:
    youtube_data = pd.read_csv('./youtube_'+game_name+'_video.csv', sep=',', header=0, encoding='cp949')

youtube_values = youtube_data.values
for item in youtube_values:
    count = item[1]
    date = item[2]
    good_count = item[3]
    bad_count = item[4]
    subscriber = item[6]
    print(str(count)+"\t"+ str(date)+"\t"+ str(good_count)+"\t"+ str(bad_count)+"\t"+ str(subscriber))
    
    count = count_processing(count)
    date = date_processing(date)
    good_count = good_count_processing(good_count)
    bad_count = bad_count_processing(bad_count)
    subscriber = subscriber_processing(subscriber)
    print(count+"\t\t"+ date+"\t"+ good_count+"\t"+ bad_count+"\t"+ subscriber)
    print("=========================================")
    result.append([item[0]]+[count]+[date]+[good_count]+[bad_count]+[item[5]]+[subscriber]+[item[7]])
    
youtube_table = pd.DataFrame(result, columns=('title', 'count', 'date', 'good_count', 'bad_count', 'youtuber', 'subscriber', 'url'))
youtube_table = youtube_table.sort_values(by=['date'], axis=0)
youtube_table.to_csv("./youtube_"+game_name+"_video_regul.csv", encoding="utf-8-sig", mode='w', index=False)
