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

    game_names = game_data['name'].values

#game_name = 'crazy_shopping' #'tatto_tycoon'#'brain_out'
    
    wd = webdriver.Chrome('D:\chromedriver_win32\\chromedriver.exe') # 업그레이드댄 버전
     
    result = []
    for game_name in game_names:
        url_count = 0
        search_label = [game_name+" 게임"] #["Crazy Shopping 게임"]
        #if(game_name == '엑소스 히어로즈'):
        #    continue
        
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
                #   print("페이지다운 : "+str(i))
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
                        print(is_end)
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
                try:
                    content = wd.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[3]/div[3]")
                    content_list = content.find_elements_by_css_selector("ytd-video-renderer")
                    print(len(content_list))
                except:
                    print("content못찾네")
            if(len(content_list) == 0) : # 엑소스 히어로즈 일 경우
                content = wd.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]")
                content_list = content.find_elements_by_css_selector("ytd-video-renderer")
                print(len(content_list))
            '''
            url_count += len(content_list)
        print(game_name +" 게임 : "+str(url_count)+"개")       
        result.append([game_name] + [len(content_list)])
        '''
            for i in range(0, len(content_list)):
                content_info = content_list[i].find_element_by_css_selector("ytd-video-meta-block")
                content_div = content_info.find_element_by_id("metadata-line")
                content_span = content_div.find_elements_by_css_selector("span")
                content_viewer = content_span[0].text
                content_viewer = content_viewer[4:]
                content_day = content_span[1].text
                print("viewer : "+content_viewer+", day : "+content_day)
                a = content_list[i].find_element_by_css_selector("a").get_attribute('href')
                print(str(i) + "번째 : " + a)
                result.append([search] + [a] + [content_viewer] + [content_day])
    youtube_table = pd.DataFrame(result, columns=('search', 'youtube_url', 'viewer', 'upload'))
        '''
    youtube_table = pd.DataFrame(result, columns=('name', 'contents_count'))
    #youtube_table.to_csv("./youtube_brain_out_url.csv", encoding="utf-8-sig", mode='w', index=False)
    youtube_table.to_csv("./youtube_url_50games_count.csv", encoding="utf-8-sig", mode='w', index=False)  
    return

    
def youtube_list():

    print('YOUTUBE CRAWLING START')
    
    YoutubeList()

    print('FINISHED')


if __name__ == '__main__':
     youtube_list()

