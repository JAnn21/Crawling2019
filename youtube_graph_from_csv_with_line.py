# 날짜별로 3달간 데이터 랭킹 그래프로 그리기
# 여기서 날짜별 조회수 = 위에꺼 plt.plot 주석풀기
# 날짜별 영상개수 = 아래꺼
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime as dt

# 폰트설정
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

def regul(a) :
    y = (a / sum(a)) * 5
    return y

def regul_rank(a):
    y = (a / sum(a)) * 50
    return y

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


for game_name, game_full_name in zip(game_names, game_full_names):
    # 파일 불러오기
    #youtube_data = pd.read_csv('./youtube_brain_out_count_each_date.csv', sep=',', header=0, encoding='utf-8-sig')
    #youtube_data2 = pd.read_csv('./game_rank_data_top3.csv', sep=',', header=0, encoding='utf-8-sig')
    #youtube_data2 = youtube_data2[youtube_data2['name'] == 'Brain Out – 가장 어색한 게임']
    youtube_data = pd.read_csv('./youtube_game_data/count_each_date/youtube_'+game_name+'_count_each_date.csv', sep=',', header=0, encoding='utf-8-sig')
    youtube_data2 = pd.read_csv('./game_rank_data_top50_final.csv', sep=',', header=0, encoding='utf-8-sig')
    youtube_data2 = youtube_data2[youtube_data2['name'] == game_full_name]
    #print(youtube_data.head())


    plot_data = []  # count
    plot_data2 = [] # contents_count
    plot_data3 = [] # rank
    for data in youtube_data.values:
        plot_data.append([data[0], data[1]])
        plot_data2.append([data[0], data[2]])

    for data in youtube_data2.values:
        #ranks.append(100-int(data[2]))
        plot_data3.append([data[1], 100-int(data[2])])
        
    x,y = [], []
    x2,y2 = [], []
    x3,y3 = [], []
    for line in plot_data:
        times = dt.datetime.strptime(str(line[0]),'%Y_%m_%d')
        x.append(times)
        y.append(line[1])

    for line in plot_data2:
        times = dt.datetime.strptime(str(line[0]),'%Y_%m_%d')
        x2.append(times)
        y2.append(line[1])

    for line in plot_data3:
        times = dt.datetime.strptime(str(line[0]),'%Y_%m_%d')
        x3.append(times)
        y3.append(line[1])
        
    y = regul(np.asarray(y))
    y2 = regul(np.asarray(y2))
    y3 = regul_rank(np.asarray(y3))

    fig = plt.figure(figsize=(16,3))

    # 여기서 날짜별 조회수 = 위에꺼 plt.plot 주석풀기
    # 날짜별 영상개수 = 아래꺼
    plt.plot(x,y,linestyle='-', marker='o', markersize=5, label="count")
    plt.plot(x2,y2,linestyle='--', marker='o', markersize=5, label="contents_count")
    plt.plot(x3,y3,linestyle='-', marker='o', markersize=5, label="rank")

    import datetime

    datenow = datetime.datetime.now()
    dstart = datetime.datetime(2019,1,1)
    
    


    firsts = [x3[0],x3[-1]]

    #for i in range(dstart.month, datenow.month+1):
    #    firsts.append(datetime.datetime(2019,i,1))
    xticks = pd.date_range(x[0],x[-1], freq='D') #xticks = pd.date_range('2019-11-20', '2019-11-29', freq='D')
    plt.xticks(xticks, [x.strftime('%Y-%m-%d') for x in xticks])
    plt.xlim(firsts)


    plt.title(game_full_name)
    plt.xlabel('date')
    plt.legend(loc=2)


    fig.autofmt_xdate()
    plt.tight_layout()

    # 그래프 저장
    if(game_name == '밥 먹고 갈래요?'):
        plt.savefig('.\\graph_img_final\\밥 먹고 갈래요.png')
    elif(game_name == '콜 오브 듀티: 모바일'):
        plt.savefig('.\\graph_img_final\\콜 오브 듀티 모바일.png')
    elif(game_name == '마기아 : 카르마 사가'):
        plt.savefig('.\\graph_img_final\\마기아 카르마 사가.png')
    else:
        plt.savefig('.\\graph_img_final\\'+game_name+'.png')
    print(game_name+" 그래프를 저장하였습니다.")

    #plt.show()
