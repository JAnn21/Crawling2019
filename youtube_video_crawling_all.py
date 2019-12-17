# 2단계 : 모든영상 url 가져왔다면 "중복제거한 url"에서 각 url 들어가 아래 내용 가져오기
# youtube_video_crawling.py : youtube_brain_out2.csv의 모든 정보에서 중복제거한 후 나머지에 대해 가져오기
# 한것에 대해 각 url에 들어가 제목, 조회수, 날짜, 좋아요, 싫어요, 작성자, 구독자 수, 해당 동영상 url 가져오기

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ssl  #추가
import time

#game_name = 'crazy_shopping' #'tatto_tycoon' #"brain_out"
'''
game_names = ['리니지2M(19)', 'brain_out', '고수_with_NAVER_WEBTOON', '리니지2M(12)', '마기아_카르마_사가','Pocket_World_3D'
             ,'Rusty_Blower_3D','sky_roller','게임빌프로야구_슈퍼스타즈', 'tatto_tycoon', '무한의_계단','워드퍼즐_단어게임'
             ,'애프터라이프','엑소스_히어로즈','무한의_농장','워너비챌린지','진화소녀','밥_먹고_갈래요','꽃피는_달빛'
             ,'브롤스타즈','기적의_검','꿈의_정원','콜_오브_듀티_모바일','꿈의_집','fun_race_3d','cannon_shot'
             ,'stencil_art','tales_rush','supreme_duelist_stickman','clash_of_blocks','클래시_로얄','v4','crazy_shopping'
             ,'왕비의_맛','1945','궁수의_전설','배틀그라운드','펭귄의_섬','라이즈_오브_킹덤즈','puzzrama'
             ,'rummikub','꿈의_마을','park_of_monster','mr_bullet','킹_오브_파이터_올스타','바이러스_워','염왕이_뿔났다','sandwich'
             ,'계급장_키우기','킹_오브_타워']
'''
'''
game_names = ['콜_오브_듀티_모바일','꿈의_집','cannon_shot','clash_of_blocks','v4','1945','배틀그라운드'
             ,'계급장_키우기','킹_오브_타워']
'''
#game_names = ['배틀그라운드', '콜_오브_듀티_모바일','꿈의_집','cannon_shot','clash_of_blocks','v4','1945']
game_names = ['왕비의_맛']
def get_request_url(url, enc='utf-8'):
    
    req = urllib.request.Request(url)

    try:
        ssl._create_default_https_context = ssl._create_unverified_context    #추가
        
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:                  
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')    
            
            return ret
            
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def YoutubeList():
    no_search = ['https://www.youtube.com/watch?v=4PdUcEQxryQ','https://www.youtube.com/watch?v=wIlXXRco3vw', 'https://www.youtube.com/watch?v=AVxwSOzaiQ8'
                 ,'https://www.youtube.com/watch?v=306ZBEGQqRE','https://www.youtube.com/watch?v=Nz2611bKdD8', 'https://www.youtube.com/watch?v=tgsAO1cwni0'
                 ,'https://www.youtube.com/watch?v=ypbmYVePLf8', 'https://www.youtube.com/watch?v=eipX32U2uIk', 'https://www.youtube.com/watch?v=BjbM7cAKz_Y'
                 ,'https://www.youtube.com/watch?v=gM0kpjnDjUI', 'https://www.youtube.com/watch?v=4ZTMlgiQHeI', 'https://www.youtube.com/watch?v=TNjfH1yonM8'
                 ,'https://www.youtube.com/watch?v=9xUqfKfpN9g', 'https://www.youtube.com/watch?v=QyopJEDQFxs', 'https://www.youtube.com/watch?v=1LTwp53ZTkI'
                 ,'https://www.youtube.com/watch?v=RybuOrJOLSs', 'https://www.youtube.com/watch?v=neG8am4HchI', 'https://www.youtube.com/watch?v=OdqX2koS8-o'
                 ,'https://www.youtube.com/watch?v=6WCf1j6a2rE']
    for game_name in game_names:
        # 모든 url(중복제거) 가져옴
        youtube_data = pd.read_csv('./youtube_game_data/youtube_'+game_name+'_url.csv', sep=',', header=0, encoding='utf-8-sig')
        '''
        youtube_2month = youtube_data[youtube_data['upload']=='2개월 전']
        youtube_10000viewer = youtube_2month[youtube_2month['viewer'] > 10000]
        url_list = youtube_10000viewer['youtube_url'].unique()
        '''
        url_list = youtube_data['youtube_url'].unique()
        print("중복제거 전 url 개수 : "+str(len(youtube_data['youtube_url']))+", 중복제거 후 url 개수 : "+str(len(url_list)))
        #wd = webdriver.Chrome('D:\python_D\\chromedriver.exe')
        wd = webdriver.Chrome('D:\chromedriver_win32\\chromedriver.exe') # 업그레이드댄 버전
        
        result = []  
        url_count = 0
        for url in url_list:
            #try:
            if(url in no_search): # 예외할부분...https://www.youtube.com/watch?v=wIlXXRco3vw
                continue
            try:
                Youtube_URL = url

                wd.get(Youtube_URL)

                time.sleep(1) # 로딩으로 인한 지연
                print(str(url_count)+'번째 크롤링')

                #div = wd.find_element_by_css_selector('ytd-video-primary-info-renderer')
                #div = div.find_element_by_id('container')
                div = wd.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[7]/div[2]/ytd-video-primary-info-renderer/div')
                title = div.find_element_by_css_selector('h1').text
                try:
                    print('제목:'+title)
                except:
                    print('제목:'+title.encode('unicode-escape').decode('utf-8'))
                info = div.find_element_by_id('info')
                count = info.find_element_by_id('count').find_elements_by_css_selector('span')[0].text
                print('조회수:'+count)
                date = info.find_element_by_id('date').find_element_by_css_selector('yt-formatted-string').text
                print("날짜:"+date)
                
                button_div = info.find_element_by_id('top-level-buttons')
                buttons = button_div.find_elements_by_css_selector('ytd-toggle-button-renderer')
                good_count = buttons[0].find_element_by_css_selector('yt-formatted-string').text
                print("좋아요 수 : "+good_count)
                bad_count = buttons[1].find_element_by_css_selector('yt-formatted-string').text
                print("싫어요 수 : "+bad_count)

                youtuber_div = wd.find_element_by_css_selector('ytd-video-owner-renderer')
                youtuber_div = youtuber_div.find_element_by_id('upload-info')
                #youtuber_div = wd.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[9]/div[3]/ytd-video-secondary-info-renderer/div/div[2]/ytd-video-owner-renderer/div[1]')
                youtuber_name = youtuber_div.find_element_by_css_selector('ytd-channel-name').text
                try:
                    print('작성자 : '+youtuber_name)
                except:
                    print('작성자 : '+youtuber_name.encode('unicode-escape').decode('utf-8'))
                youtuber_subscriber = youtuber_div.find_element_by_id('owner-sub-count').text
                print('구독자 수 : '+youtuber_subscriber)
                print("===================================")
                result.append([title]+[count]+[date]+[good_count]+[bad_count]+[youtuber_name]+[youtuber_subscriber]+[url])

                url_count += 1
            except:
                continue
            
            if(url_count%50==0):
                youtube_table = pd.DataFrame(result, columns=('title', 'count', 'date', 'good_count', 'bad_count', 'youtuber', 'subscriber', 'url'))
                youtube_table.to_csv("./youtube_game_data/video/youtube_"+game_name+"_video.csv", encoding="utf-8-sig", mode='w', index=False)
            #except:
            #    print("작성자가 없앤 동영상입니다.")
            
        youtube_table = pd.DataFrame(result, columns=('title', 'count', 'date', 'good_count', 'bad_count', 'youtuber', 'subscriber', 'url'))
        youtube_table = youtube_table.sort_values(by=['date'], axis=0)
        youtube_table.to_csv("./youtube_game_data/video/youtube_"+game_name+"_video.csv", encoding="utf-8-sig", mode='w', index=False)
        
    return

    
def youtube_list():

    print('Youtube CRAWLING START')
    
    YoutubeList()

    print('FINISHED')


if __name__ == '__main__':
     youtube_list()


    
