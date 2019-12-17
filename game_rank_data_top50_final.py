# game_rank_data_top50.csv에서 지정한 50개 게임에 대해
# 등록된 날짜부터의 brain out, tatto tycoon, crazy shopping 정보만 가져오기
import pandas as pd

'''
game_enter = [['Brain Out – 가장 어색한 게임', '2019_09_17'], ['Ink Inc. - Tattoo Tycoon','2019_10_27']
              , ['Crazy Shopping','2019_10_19']]
'''

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



game_data = pd.read_csv('.\\game_rank_data_top50.csv', sep=',', header=0, encoding='utf-8-sig')
#brain = game_data[game_data['name']=='Brain Out – 가장 어색한 게임']
#brain_values = brain.values
'''
array([[999, '2019_09_17', 'Brain Out – 가장 어색한 게임'],
       [999, '2019_09_18', 'Brain Out – 가장 어색한 게임'],
       [999, '2019_09_19', 'Brain Out – 가장 어색한 게임'],
       [999, '2019_09_20', 'Brain Out – 가장 어색한 게임'],
       [999, '2019_09_21', 'Brain Out – 가장 어색한 게임']])
'''

result = []
for game in range(0, len(game_enter)):
    sub_game = game_data[game_data['name']==game_enter[game][0]]
    sub_game_values = sub_game.values
    # 게임 등록 날짜가 2019년9월1일 이전에 등록된 것은 전부 9월 1일로 바꾼다. -> 랭킹을 9월 1일부터 가져왔음.
    game_enter_date = game_enter[game][1].replace('_','') # 2019_11_27 -> 20191127
    if(int(game_enter_date) < 20190901):
        game_enter_date = '2019_09_01'
        #print(str(game_enter[game][0])+' : '+str(game_enter[game][1])+' -> '+'2019_09_01')
    else:
        game_enter_date = game_enter[game][1]
        #print(str(game_enter[game][0])+' : '+str(game_enter[game][1]))
    
    for i in range(0,len(sub_game_values)-1):
        if(int(game_enter_date.replace('_','')) <= int(sub_game_values[i][1].replace('_',''))): # 게임 등록일보다 큰것에 한해서 
            a = sub_game_values[i][0]
            b = sub_game_values[i+1][0]
            if(a == 999):
                a = 101
            if(b == 999):
                b = 101
            #print("첫번째("+brain_values[i][1]+") : "+ str(a))
            #print("두번째("+brain_values[i+1][1]+") : "+ str(b))
            print("앞, 뒤 차 : "+str(abs(int(a)-int(b))))

            result.append([sub_game_values[i][2]] + [sub_game_values[i][1]] + [a] + [str(abs(int(a)-int(b)))])
        if( i == len(sub_game_values)-2):
            print("끝입니당 : "+str(i))
            result.append([sub_game_values[i+1][2]] + [sub_game_values[i+1][1]] + [b] + [0])
            
print(result)
game_table = pd.DataFrame(result, columns=('name', 'date', 'rank', 'diff'))
#game_table.to_csv(".\\game_rank_data_top3.csv", encoding="utf-8-sig", mode='w', index=False)
game_table.to_csv(".\\game_rank_data_top50_final.csv", encoding="utf-8-sig", mode='w', index=False)
