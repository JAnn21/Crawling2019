# csv파일 불러와 인덱스 없애고 저장하기
import pandas as pd
import os

# 원본폴더와 저장될 폴더 설정
folder_path = ".\\project"
restore_folder_path = ".\\project2"

# 원본파일 불러오기(project 에서 불러오기)
file_list = os.listdir(folder_path)

# project폴더 밑의 모든 파일 불러와서 처리 후 저장 ('.\\project\\game_2019_09_01.csv'형식)
for file_name in file_list:   # file_name = game_2019_09_01.csv
    game_data = pd.read_csv(folder_path+"\\"+file_name, sep=',', header=0, encoding='utf-8-sig')
    
    # 인덱스, rank, name으로 이루어진 파일에서 인덱스 뺀 나머지 정보로 구성
    game_data2 = game_data[['rank','name']]
    
    # 인덱스를 없애고(index=False) project2폴더에 다시 저장하기 ('.\\project2\\game_2019_09_01.csv')
    game_data2.to_csv(restore_folder_path+"\\"+file_name, index=False, encoding='utf-8-sig')
    print(file_name +" 파일 다시 저장 성공")
