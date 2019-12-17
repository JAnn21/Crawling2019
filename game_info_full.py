# 지난순위 다시보기 페이지에서 각 게임의 번호(a태그에 href로 있음.)를 알아와
# 50개 고른 게임들의 정보 파악하기 - 킹 오브 타워는 따로해줌
# 정확하지 않음 확인하고 정제해야 함.
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver

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

def GameList(result, start_month, now_month):
    # 어떤 게임으로 할껀지 이름, url 저장한 파일에서 게임이름 50개 가져오기
    last_data = pd.read_csv('.\\game_info.csv', sep=',', header=0, encoding='euckr')
    last_data_value = last_data.values
    last_data_df = pd.DataFrame(last_data_value, columns=['name', 'url'])
    last_data_df_value = last_data_df.values

    Game_URL = last_data_df_value[0][1]
    #wd = webdriver.Chrome('D:\python_D\\chromedriver.exe')
    wd = webdriver.Chrome('D:\chromedriver_win32\\chromedriver.exe') # 업그레이드댄 버전
    wd.get(Game_URL)

    # 로그인해야함
    wd.execute_script("goMemberNaver()") # 이 스크립트 적용해 들어감
    # 기다림
    x = input()

    result = []
    print(len(last_data_df))
    for i in range(0,len(last_data_df)):
        name_result = last_data_df_value[i][0]
        url_result = last_data_df_value[i][1]
        print(str(i)+"번째 게임 이름 : "+name_result) # 한줄 [0][0] = 이름
        print("게임 url : "+url_result) # 한줄 [0][1] = url
        game_list = last_data_df.name.unique()  # game_list[0] = '리니지M(19)'
        #print(game_list)

        
        # 다시 게임정보 페이지 감
        Game_URL = last_data_df_value[i][1]
        wd.get(Game_URL)
        try:
            div = wd.find_element_by_xpath("/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[3]/div[2]")
        except:
            try:
                div = wd.find_element_by_xpath("/html/body/div[7]/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div[3]") # 무한의계단 ㅠ
            except:
                print("수기로 입력하기")
                result.append([name_result] + [url_result] + ["none"] + ["none"])
                continue
            
        ol = div.find_element_by_css_selector('ol')
        li = ol.find_elements_by_css_selector('li')
        
        # 등록날짜 가져오기
        try: # 위에서 1번째꺼 해보고
            span_date = li[1].find_elements_by_css_selector('span')             # list중에 위에서 1번째꺼
            print("등록날짜 : "+span_date[1].text)
            date = span_date[1].text   # 2019년 11월 27일
            dates = date.split(" ")    # ['2019년', '11월', '27일']
            date_result = dates[0][:-1]+"_"+dates[1][:-1]+"_"+dates[2][:-1] # 2019_11_27

        except: # 안되면 위에서 3번째꺼임.
            try:
                span_date = li[3].find_elements_by_css_selector('span')             # list중에 위에서 1번째꺼
                print("등록날짜 : "+span_date[1].text)
                date = span_date[1].text   # 2019년 11월 27일
                dates = date.split(" ")    # ['2019년', '11월', '27일']
                date_result = dates[0][:-1]+"_"+dates[1][:-1]+"_"+dates[2][:-1] # 2019_11_27
            except:
                date_result = 'none'

        # 다운로드 횟수 가져오기
        try: # 뒤에서 1번째꺼 해보고
            list_num = len(li)
            span_download = li[list_num-2].find_elements_by_css_selector('span') # list중에 밑에서 1번째꺼
            print("다운로드 : "+span_download[1].text)
            down = span_download[1].text    # "500,000 ~ 1,000,000"
            downs = down.split(" ~ ")       # ['500,000', '1,000,000']
            a = int(downs[0].replace(",","")) # 500000
            b = int(downs[1].replace(",","")) # 1000000
            down_result = int((a+b)/2)        # 750000

        except: # 안되면 뒤에서 2번째꺼
            try:
                list_num = len(li)
                span_download = li[list_num-3].find_elements_by_css_selector('span') # list중에 밑에서 1번째꺼
                print("다운로드 : "+span_download[1].text)
                down = span_download[1].text    # "500,000 ~ 1,000,000"
                downs = down.split(" ~ ")       # ['500,000', '1,000,000']
                a = int(downs[0].replace(",","")) # 500000
                b = int(downs[1].replace(",","")) # 1000000
                down_result = int((a+b)/2)        # 750000
            except:
                down_result = 'none'
            
        result.append([name_result] + [url_result] + [date_result] + [down_result])
        print("================================")

    game_table = pd.DataFrame(result, columns=('name', 'url', 'enter_date', 'download'))
    game_table.to_csv(".\\game_info_full.csv", encoding="utf-8-sig", mode='w', index=False)   
        
    
    '''  
    # 다시 지난 순위 들어감
    wd.get(Game_URL)
    #wd.find_element_by_id('schDate').click()
    #wd.find_element_by_xpath("/html/body/div[5]/table/tbody/tr[1]/td[6]").click()

    # 현재 페이지에서 a태그 밑의 href 정보 가져옴
    table = wd.find_element_by_xpath("/html/body/div[2]/div[7]/div/div/table")
    tbody = table.find_element_by_css_selector('tbody')
    tr = tbody.find_elements_by_css_selector('tr')

    game_url = []
    for rank_list in tr:
        item_info = rank_list.find_elements_by_css_selector('td')
        item_name = item_info[1].find_element_by_class_name('rank1')
        item_num = item_name.find_element_by_css_selector('a').get_attribute('href')
        
        if(item_name.text in game_list):
            #print(item_name.text)
            #print(item_num)     # 각 게임 url
            game_url.append([item_name.text] + [item_num])
            #game_url.append([item_name.text])

    game_table = pd.DataFrame(game_url, columns=('name', 'url'))
    game_table.to_csv("./game_info.csv", encoding="utf-8-sig", mode='w', index=True)
    print("지금 가져온 url 개수 : "+ str(len(game_url)))
    '''
    '''
    #for tr_num in range(1,3):  # /html/body/div[5]/table/tbody/tr[1]/td[1]
        #for td_num in range(1,3):
    for tr_num in range(1,6):
        for td_num in range(1,8):
            result = []
            try:
                wd.find_element_by_id('schDate').click()
                now_date = wd.find_element_by_xpath("/html/body/div[5]/table/tbody/tr["+str(tr_num)+"]/td["+str(td_num)+"]")
                now_date_text = now_date.text
                if(now_date_text != " "):    # 달력 표에서 숫자안적혀있으면 " "(공백하나), 아니면 숫자 적혀있음.
                    now_date.click()
                    #print("날짜 : "+now_date_text)
                    date = wd.find_element_by_class_name("schTxt")
                    date_txt = date.find_element_by_css_selector('input').get_attribute("value")
                    #print("현재 년월일 : "+date_txt)

                    # 현재 년월일 뽑기
                    date = wd.find_element_by_class_name("schTxt")
                    date_txt = date.find_element_by_css_selector('input').get_attribute("value")
                    #print("현재 년월일 : "+date_txt)
                    # 년월일 split, 2019_11_28로 변경 후 리턴할 것.
                    date_txt = date_txt.replace("-", "_")
                    
                    # 현재 날짜의 순위 가져오기
                    rank_div = wd.find_element_by_id('imgload')
                    rank_table = rank_div.find_element_by_css_selector("table")
                    rank_body = rank_table.find_element_by_css_selector('tbody')
                    ranks_list = rank_body.find_elements_by_css_selector('tr')
                    #print("가져온 랭크 개수 : ", len(ranks_list))
                    
                    for item in ranks_list:   # item = tr 하나, tr에 대해 td 네개 나옴.
                        item_info = item.find_elements_by_css_selector('td')
                        item_rank = item_info[0].text
                        item_name = item_info[1].find_elements_by_class_name('rank1')[0].text
                        #print("어플 랭킹 : ", item_rank)
                        #print("어플 이름 : ", item_name)
                        result.append([item_rank] + [item_name])
                    print(date_txt+" 랭킹 크롤링 성공")
                    game_table = pd.DataFrame(result, columns=('rank', 'name'))
                    game_table.to_csv("./project/game_"+date_txt+".csv", encoding="utf-8-sig", mode='w', index=True)
    
                else:
                    print("달력에 활성화된곳 아님")
            except:
                print("어디선가 오류가!!")
        
    '''     
    #rank_info = ranks_list[0].find_elements_by_css_selector('td')
    #print("어플 랭킹 : ", rank_info[0].text)
    #print("어플 이름 : ", rank_info[1].text)

    return

    
def game_list():

    result = []

    print('GAME CRAWLING START')

    # 현재 달과 최근 몇달인지 설정
    start_month = 9
    now_month = 11
    
    GameList(result, start_month, now_month)


    print('FINISHED')


if __name__ == '__main__':
     game_list()

