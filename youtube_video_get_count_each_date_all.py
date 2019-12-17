# 4단계 : 각 영상 정보 일반화시킨 후에 날짜별로 가장 큰 조회수 가진 것으로 구성.
# youtube_brain_out_video_regul.csv의 정보에서 날짜별로 가장 큰 값만 표시 - date, count 만 표시.
#
import pandas as pd
import os
from pandas import DataFrame

#game_name = 'crazy_shopping' #'tatto_tycoon' #'brain_out'
#game_full_name = 'Crazy Shopping'#'Ink Inc. - Tattoo Tycoon' #'Brain Out – 가장 어색한 게임'

game_names = ['리니지2M(19)', 'brain_out', '고수_with_NAVER_WEBTOON', '리니지2M(12)', '마기아_카르마_사가','Pocket_World_3D'
             ,'Rusty_Blower_3D','sky_roller','게임빌프로야구_슈퍼스타즈', 'tatto_tycoon', '무한의_계단','워드퍼즐_단어게임'
             ,'애프터라이프','엑소스_히어로즈','무한의_농장','워너비챌린지','진화소녀','밥_먹고_갈래요','꽃피는_달빛'
             ,'브롤스타즈','기적의_검','꿈의_정원','콜_오브_듀티_모바일','꿈의_집','fun_race_3d','cannon_shot'
             ,'stencil_art','tales_rush','supreme_duelist_stickman','clash_of_blocks','클래시_로얄','v4','crazy_shopping'
             ,'왕비의_맛','1945','궁수의_전설','배틀그라운드','펭귄의_섬','라이즈_오브_킹덤즈','puzzrama'
             ,'rummikub','꿈의_마을','park_of_monster','mr_bullet','킹_오브_파이터_올스타','바이러스_워'
             ,'염왕이_뿔났다','sandwich','계급장_키우기','킹_오브_타워']

game_full_names = ['리니지2M(19)','Brain Out - 가장 어색한 게임','고수 with NAVER WEBTOON','리니지2M(12)','마기아 : 카르마 사가','Pocket World 3D'
                  ,'Rusty Blower 3D','Sky Roller','게임빌프로야구 슈퍼스타즈','Ink Inc. - Tattoo Tycoon','무한의 계단','워드퍼즐 - 단어 게임'
                  ,'애프터라이프','엑소스 히어로즈','무한의 농장','워너비챌린지','진화소녀','밥 먹고 갈래요?','꽃피는 달빛'
                  ,'브롤스타즈','기적의 검','꿈의 정원 (Gardenscapes)','콜 오브 듀티: 모바일','꿈의 집 (Homescapes)','Fun Race 3D','Cannon Shot!'
                  ,'Stencil Art - Spray Masters','Tales Rush!','Supreme Duelist Stickman','Clash of Blocks','클래시 로얄','V4','Crazy Shopping'
                  ,'왕비의 맛','1945','궁수의 전설','배틀그라운드','펭귄의 섬','라이즈 오브 킹덤즈','Puzzrama (퍼즈라마)'
                  ,'Rummikub','꿈의 마을 (Township)','Park of Monster','Mr Bullet - 스파이 퍼즐','킹 오브 파이터 올스타','바이러스 워 - 우주 슈팅 게임'
                  ,'염왕이 뿔났다','Sandwich!','계급장 키우기','킹 오브 타워']


for (game_name, game_full_name) in zip(game_names, game_full_names):
    result = []
    try:
        youtube_data = pd.read_csv('./youtube_game_data/regul/youtube_'+game_name+'_video_regul.csv', sep=',', header=0, encoding='utf-8-sig')
    except:
        youtube_data = pd.read_csv('./youtube_game_data/regul/youtube_'+game_name+'_video_regul.csv', sep=',', header=0, encoding='cp949')

    # youtube 데이터에는 영상이 없는날은 date가 없기 때문에 game data에서 date 가져오자
    try:
        day_data = pd.read_csv('./game_rank_data_top50.csv', sep=',', header=0, encoding='utf-8-sig')
    except:
        day_data = pd.read_csv('./game_rank_data_top50.csv', sep=',', header=0, encoding='cp949')

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
                now_count = int(str(info[1]).replace(',',''))
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
    youtube_table.to_csv("./youtube_game_data/count_each_date/youtube_"+game_name+"_count_each_date.csv", encoding="utf-8-sig", mode='w', index=False)
