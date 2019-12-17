# 4단계 : 각 영상 정보 일반화시킨 후에 날짜별로 가장 큰 조회수 가진 것으로 구성.
# youtube_brain_out_video_regul.csv의 정보에서 날짜별로 가장 큰 값만 표시 - date, count 만 표시.
#
import pandas as pd
import os
from pandas import DataFrame
import datetime as dt
#game_name = 'brain_out'#'crazy_shopping' #'tatto_tycoon' #'brain_out'
#game_full_name = 'Brain Out – 가장 어색한 게임'#'Crazy Shopping'#'Ink Inc. - Tattoo Tycoon' #'Brain Out – 가장 어색한 게임'

game_names = ['리니지2M(19)', 'brain_out', '고수_with_NAVER_WEBTOON', '리니지2M(12)', '마기아_카르마_사가','Pocket_World_3D'
             ,'Rusty_Blower_3D','sky_roller','게임빌프로야구_슈퍼스타즈', 'tatto_tycoon', '무한의_계단','워드퍼즐_단어게임'
             ,'애프터라이프','엑소스_히어로즈','무한의_농장','워너비챌린지','진화소녀','밥_먹고_갈래요','꽃피는_달빛'
             ,'브롤스타즈','기적의_검','꿈의_정원','콜_오브_듀티_모바일','꿈의_집','fun_race_3d','cannon_shot'
             ,'stencil_art','tales_rush','supreme_duelist_stickman','clash_of_blocks','클래시_로얄','v4','crazy_shopping'
             ,'왕비의_맛','1945','궁수의_전설','배틀그라운드','펭귄의_섬','라이즈_오브_킹덤즈','puzzrama'
             ,'rummikub','꿈의_마을','park_of_monster','mr_bullet','킹_오브_파이터_올스타','바이러스_워'
             ,'염왕이_뿔났다','sandwich','계급장_키우기','킹_오브_타워']

game_full_names = ['리니지2M(19)','Brain Out – 가장 어색한 게임','고수 with NAVER WEBTOON','리니지2M(12)','마기아 : 카르마 사가','Pocket World 3D'
                  ,'Rusty Blower 3D','Sky Roller','게임빌프로야구 슈퍼스타즈','Ink Inc. - Tattoo Tycoon','무한의 계단','워드퍼즐 - 단어 게임'
                  ,'애프터라이프','엑소스 히어로즈','무한의 농장','워너비챌린지','진화소녀','밥 먹고 갈래요?','꽃피는 달빛'
                  ,'브롤스타즈','기적의 검','꿈의 정원 (Gardenscapes)','콜 오브 듀티: 모바일','꿈의 집 (Homescapes)','Fun Race 3D','Cannon Shot!'
                  ,'Stencil Art - Spray Masters','Tales Rush!','Supreme Duelist Stickman','Clash of Blocks','클래시 로얄','V4','Crazy Shopping'
                  ,'왕비의 맛','1945','궁수의 전설','배틀그라운드','펭귄의 섬','라이즈 오브 킹덤즈','Puzzrama (퍼즈라마)'
                  ,'Rummikub','꿈의 마을 (Township)','Park of Monster','Mr Bullet - 스파이 퍼즐','킹 오브 파이터 올스타','바이러스 워 - 우주 슈팅 게임'
                  ,'염왕이 뿔났다','Sandwich!','계급장 키우기','킹 오브 타워']

game_enter = [['리니지2M(19)', '2019_11_27'], ['Brain Out – 가장 어색한 게임', '2019_09_17'], ['고수 with NAVER WEBTOON', '2019_11_26']
              , ['리니지2M(12)', '2019_11_27'], ['마기아 : 카르마 사가', '2019_08_08'], ['Pocket World 3D', '2019_10_22']
              , ['Rusty Blower 3D', '2019_11_18'], ['Sky Roller', '2019_10_24'], ['게임빌프로야구 슈퍼스타즈', '2019_11_24']
              , ['Ink Inc. - Tattoo Tycoon', '2019_10_27'], ['무한의 계단', '2015_01_16'], ['워드퍼즐 - 단어 게임', '2019_07_20']
              , ['애프터라이프', '2019_11_20'], ['엑소스 히어로즈', '2019_11_20'], ['무한의 농장', '2019_07_31']
              , ['워너비챌린지', '2019_11_26'], ['진화소녀', '2019_11_26'], ['밥 먹고 갈래요?', '2019_07_31']
              , ['꽃피는 달빛', '2019_10_12'], ['브롤스타즈', '2018_06_26'], ['기적의 검', '2019_09_09']
              , ['꿈의 정원 (Gardenscapes)', '2016_08_22'], ['콜 오브 듀티: 모바일', '2019_09_30'], ['꿈의 집 (Homescapes)', '2017_08_15']
              , ['Fun Race 3D', '2019_05_23'], ['Cannon Shot!', '2019_11_07'], ['Stencil Art - Spray Masters', '2019_11_17']
              , ['Tales Rush!', '2019_09_09'], ['Supreme Duelist Stickman', '2019_04_09'], ['Clash of Blocks', '2019_11_01']
              , ['클래시 로얄', '2016_03_02'], ['V4', '2019_09_25'], ['Crazy Shopping', '2019_10_19']
              , ['왕비의 맛', '2019_09_25'], ['1945', '2019_03_06'], ['궁수의 전설', '2019_04_11']
              , ['배틀그라운드', '2018_05_15'], ['펭귄의 섬', '2019_08_28'], ['라이즈 오브 킹덤즈', '2019_09_02']
              , ['Puzzrama (퍼즈라마)', '2019_10_13'], ['Rummikub', '2017_10_10'], ['꿈의 마을 (Township)', '2013_10_23']
              , ['Park of Monster', '2019_03_09'], ['Mr Bullet - 스파이 퍼즐', '2019_01_16'], ['킹 오브 파이터 올스타', '2019_05_08']
              , ['바이러스 워 - 우주 슈팅 게임', '2019_06_04'], ['염왕이 뿔났다', '2019_11_19'], ['Sandwich!', '2019_08_09']
              , ['계급장 키우기', '2018_02_20'], ['킹 오브 타워', '2019_10_14']]

result = []
for game_name, game_full_name in zip(game_names, game_full_names):
    try:
        print(game_name+", "+game_full_name+" 가설 추측")
        # date, count, content_count 있음.
        try:
            youtube_data = pd.read_csv('./youtube_game_data/count_each_date/youtube_'+game_name+'_count_each_date.csv', sep=',', header=0, encoding='utf-8-sig')
        except:
            youtube_data = pd.read_csv('./youtube_game_data/count_each_date/youtube_'+game_name+'_count_each_date.csv', sep=',', header=0, encoding='cp949')

        # name, date, rank, diff 있음.
        try:
            rank_data = pd.read_csv('./game_rank_data_top50_final.csv', sep=',', header=0, encoding='utf-8-sig')
        except:
            rank_data = pd.read_csv('./game_rank_data_top50_final.csv', sep=',', header=0, encoding='cp949')
     
        rank_data = rank_data[rank_data['name'] == game_full_name]

        # count(조회수) 가장 높은 5개 시점 조사, high_count, high_count_date, high_count_rank 가져오기.
        high_count_data = youtube_data.sort_values(by=['count'], axis=0, ascending=False)
        #print(high_count_data)
        high_count_datas = []
        high_count_data_num = 0
        for data in high_count_data.values:
            if(high_count_data_num == 5):
                break
            date = data[0] # 2019_09_08
            date = date.replace('_','') # 20190908

            print(rank_data.values[0][1].replace('_',''))
            if(int(date) < int(rank_data.values[0][1].replace('_',''))): # 영상의 날짜가 해당게임 등록일보다 작다면 건너뛰기
                continue
            elif(int(date) >= 20191129):
                break
            else:
                high_count_datas.append([data[0], data[1], data[2]])
                high_count_data_num += 1
            
        #high_count_data = high_count_data.values[:5]
        high_count_data = high_count_datas
        print('high_count_data')
        print(high_count_data)
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
            try:
                high_count_rank = rank_data[rank_data['date']==h_date].values
                high_count_ranks.append(high_count_rank[0][2])
            except:
                print(h_date+" 영상은 게임 등록일보다 이전")
        print('high_count_ranks')
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
        print('next_ranks')
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

        print('high_rank_contents')
        print(high_rank_contents) # 4, 2, 0, 4, 8, 11, ...


        low_rank_contents = []
        for rank in unrank_list: 
            high_rank_data = rank_data[rank_data['rank']==rank] # 1위인것 빼고 가져오고,
            for date in high_rank_data.values:
                contents = youtube_data[youtube_data['date']==date[1]].values # 1위인것 날짜에 따른 컨텐츠개수 파악
                contents = contents[0][2]
                low_rank_contents.append(contents)
                
        print('low_rank_contents')
        print(low_rank_contents) # 4, 2, 0, 4, 8, 11, ...


        if(len(high_rank_contents) == 0):
            high_rank_contents_count = 0
        else:
            high_rank_contents_count = sum(high_rank_contents) / len(high_rank_contents)

        if(len(low_rank_contents) == 0):
            low_rank_contents_count = 0
        else:
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
        for i in range(0, len(high_count_ranks)):
            h_rank = high_count_ranks[i]
            n_rank = next_ranks[i]
            if(h_rank > n_rank):
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

        #print('result')
        #print(result)
        print('=================================================')
    except:
        print(game_name+"은 데이터가 너무 적어요 ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ")
youtube_table = pd.DataFrame(result, columns=('name','high_rank_contents_count','low_rank_contents_count','high_count','high_count_day','high_count_rank','next_count_rank','hypothesis1','hypothesis2'))
youtube_table.to_csv("./youtube_hypothesis_result2.csv", encoding="utf-8-sig", mode='w', index=False)

