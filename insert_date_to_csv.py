# 여러개의 csv파일(rank, name)을 name,date,rank로 구성해 저장하기
import pandas as pd
import os

# 원본폴더와 저장될 폴더 설정
folder_path = ".\\project2"
restore_folder_path = ".\\project3"

# 원본파일 불러오기(project2 에서 불러오기)
file_list = os.listdir(folder_path)

# project폴더 밑의 모든 파일 불러와서 처리 후 저장 ('.\\project\\game_2019_09_01.csv'형식)
for file_name in file_list:   # file_name = game_2019_09_01.csv
    game_data = pd.read_csv(folder_path+"\\"+file_name, sep=',', header=0, encoding='utf-8-sig')
    
    # name, date, rank로 만들어 저장하기
    game_data.insert(1, column='date', value=file_name[5:-4])
    game_data.to_csv(restore_folder_path+"\\"+file_name, index=False, encoding='utf-8-sig')
    print(file_name +" 파일 다시 저장 성공")
    '''
    game_name = "보스레이브"
    game_data2 = game_data[game_data['name']==game_name] # name을 내가 선택한 게임으로 가져옴
    print(game_data2.values)
    result.append(game_data2.values)
    print(result)
    '''
