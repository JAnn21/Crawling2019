# 1단계 : 유튜브 검색했을때에 나오는 모든 영상 url 가져오기
# youtube_url_crawling.py : 유튜브 들어가 검색어, 각 영상 url, 조회수, 날짜 크롤링
# 검색어에 따라서 [검색어, url, 조회수, 업로드날짜] 일단 전체적으로 크롤링
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ssl  #추가

#game_name = 'crazy_shopping' #'tatto_tycoon'#'brain_out'
#search_label = ["Crazy Shopping 게임"]

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
game_names = ['1945','궁수의_전설','배틀그라운드','펭귄의_섬','라이즈_오브_킹덤즈','puzzrama'
             ,'rummikub','꿈의_마을','park_of_monster','mr_bullet','킹_오브_파이터_올스타','바이러스_워','염왕이_뿔났다','sandwich'
             ,'계급장_키우기','킹_오브_타워']
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
    #search_label = ["브레인아웃", "브레인+아웃"] # 한국랭킹이므로 한국어 검색을 위
    #search_label = ["Ink Inc. - Tattoo Tycoon", "Tattoo Tycoon game", "tatoo tycoon 타투"]
    
    try:
        game_data = pd.read_csv('./game_info_full.csv', sep=',', header=0, encoding='utf-8-sig')
    except:
        game_data = pd.read_csv('./game_info_full.csv', sep=',', header=0, encoding='cp949')

    game_full_names = game_data['name'].values

    wd = webdriver.Chrome('D:\chromedriver_win32\\chromedriver.exe') # 업그레이드댄 버전
    
    
    count = 34
    for game_name in game_names:
        result = []
        search_label = [game_full_names[count]+" 게임"]
        count += 1
        for search in search_label:
            # CAISBAgFEAE%253D = 동영상, 업로드날짜 클릭했을때 
            Youtube_URL = 'https://www.youtube.com/results?search_query='+search+'&sp=CAISBAgFEAE%253D'
            #wd = webdriver.Chrome('D:\python_D\\chromedriver.exe')
           
            wd.get(Youtube_URL)

            # 페이지 다운 "결과가 더 이상 없습니다." 나올때까지 하기!
            body = wd.find_element_by_tag_name("body")
            for i in range(0, 1000):
                body.send_keys(Keys.PAGE_DOWN)
                #if (i%10==0):
                    #print("페이지다운 : "+str(i))
                try:
                    try:
                        content = wd.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]")
                        message_list = content.find_element_by_css_selector("ytd-message-renderer")
                        is_end = message_list.find_element_by_css_selector("yt-formatted-string").text
                        print(is_end)
                    except: # tatto일 경우
                        content = wd.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[3]/div[3]")
                        message_list = content.find_element_by_css_selector("ytd-message-renderer")
                        is_end = message_list.find_element_by_css_selector("yt-formatted-string").text
                        print(is_end)
                    if(is_end == "결과가 더 이상 없습니다."):
                        print("페이지 다운 끝까지 했습니다.")
                        break;
                except:
                    continue
                
            content = wd.find_elements_by_id('contents')
            content_list = content[0].find_elements_by_css_selector('ytd-video-renderer')
            '''
            content = wd.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]")
            content_list = content.find_elements_by_css_selector("ytd-video-renderer")
            
            if(len(content_list) == 0) : # tatto일 경우
                content = wd.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[3]/div[3]")
                content_list = content.find_elements_by_css_selector("ytd-video-renderer")
                print(len(content_list))
            '''     
        
            for i in range(0, len(content_list)):
                try:
                    content_info = content_list[i].find_element_by_css_selector("ytd-video-meta-block")
                    content_div = content_info.find_element_by_id("metadata-line")
                    content_span = content_div.find_elements_by_css_selector("span")
                    content_viewer = content_span[0].text
                    content_viewer = content_viewer[4:]
                
                    content_day = content_span[1].text
                    #print("viewer : "+content_viewer+", day : "+content_day)
                    a = content_list[i].find_element_by_css_selector("a").get_attribute('href')
                    #print(str(i) + "번째 : " + a)
                except:
                    print("실시간 진행중이라 못함.")
                    continue
                result.append([search] + [a] + [content_viewer] + [content_day])
                
            print(str(count) + " : "+game_name+" 게임 url 크롤링 - "+str(len(result))+"개")
        youtube_table = pd.DataFrame(result, columns=('search', 'youtube_url', 'viewer', 'upload'))
        #youtube_table.to_csv("./youtube_brain_out_url.csv", encoding="utf-8-sig", mode='w', index=False)
        youtube_table.to_csv("./youtube_game_data/youtube_"+game_name+"_url.csv", encoding="utf-8-sig", mode='w', index=False)  
    return

    
def youtube_list():

    print('YOUTUBE CRAWLING START')
    
    YoutubeList()

    print('FINISHED')


if __name__ == '__main__':
     youtube_list()

