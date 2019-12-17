# 게임순위 들어가서 현재 년월일, 어플랭킹, 어플이름 뽑아서 저장
# 달 바꿔서 검색하고, 100개 리스트 저장하는 함수 만듦
# 최근 3달간(9,10,11월)의 모바일게임랭킹 정보 크롤링해 각 날짜별로 game_2019_11_29.csv로 저장.
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
    Game_URL = 'http://www.gevolution.co.kr/rank/history'    
    wd = webdriver.Chrome('D:\chromedriver_win32\\chromedriver.exe')
    wd.get(Game_URL)

    # 로그인해야함
    wd.execute_script("goMemberNaver()") # 이 스크립트 적용해 들어감
    # 기다림
    x = input()

    
    # 다시 지난 순위 들어가서 달력누르기
    wd.get(Game_URL)
    #wd.find_element_by_id('schDate').click()
    #wd.find_element_by_xpath("/html/body/div[5]/table/tbody/tr[1]/td[6]").click()

    

    for month in range(start_month-1, now_month): # 9~11 몇월부터 몇월까지 검색할건지
        # 이번달꺼 다 하면 다음달로 넘어감(9월부터 시작)
        print("============================")
        wd.find_element_by_id('schDate').click()
        month_list = wd.find_element_by_class_name("ui-datepicker-month")
        month_list.click()
        option_list = month_list.find_elements_by_css_selector("option")
        print("달 선택 : "+option_list[month].get_attribute("value"))  # option_list[0]~option_list[10] 누를 수 있음.   
        option_list[month].click()

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

