# game_rank_data.csv에서 지정한 50개 게임에 대해 각 게임별로 랭킹 뽑아보기
import pandas as pd
import os
from pandas import DataFrame

# 어떤 게임으로 할껀지 가장 최근 파일(11/29)에서 게임이름 50개 가져오기
last_data = pd.read_csv('.\\project3\\game_2019_11_29.csv', sep=',', header=0, encoding='utf-8-sig')
last_data_value = last_data.values
last_data_df = DataFrame(last_data_value[:50])
last_data_df = DataFrame(last_data_value[:50], columns=['rank', 'date', 'name'])
game_list = last_data_df.name.unique()  # game_list[0] = '리니지M(19)'
print(game_list)
#last_data_result = last_data_df['name']

# 원본폴더와 저장될 폴더 설정
folder_path = ".\\project3"

# 원본파일 불러오기(project3 에서 불러오기)
file_list = os.listdir(folder_path)

result = []
# 불러온 파일에서 
for file_name in file_list:   # file_name = game_2019_09_01.csv
    game_data = pd.read_csv(folder_path+"\\"+file_name, sep=',', header=0, encoding='utf-8-sig')
    for game in game_list:
        game_rank = game_data[game_data['name']==game] # 게임이름이 내가 정한 리스트에 있는지 검사
        print(game_rank['rank'].values)
        if(game_rank['rank'].empty):                    # 100위안에 든 랭킹에 없다면
            print("순위없으면 랭킹 999, 날짜, 게임이름으로 만들어 csv파일에 넣기")
            result.append(["999"] + [file_name[5:-4]] + [game])
        else:
            print(file_name[5:-4]+" "+game+" 랭킹 순위 : "+str(game_rank['rank'].values))
            #result.append(game_rank)
            result.append([game_rank['rank'].values[0]] + [game_rank['date'].values[0]] + [game_rank['name'].values[0]])

game_table = pd.DataFrame(result, columns=('rank', 'date', 'name'))
game_table.to_csv(".\\game_rank_data_top50.csv", encoding="utf-8-sig", mode='w', index=False)



print(result)
#result.to_csv(".\\game_rank_data_top50.csv", encoding="utf-8-sig", mode='w', index=False)
#result.to_csv(".\\game_rank_data.csv", encoding="utf-8-sig", mode='w', index=False)
#print("game_rank_data.csv 파일로 저장했습니다.")
