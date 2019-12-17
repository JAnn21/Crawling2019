# Crawling2019

# 1. 게임랭킹 크롤링
## 1) game6.py : 게임랭킹 9/1~11/29 크롤링
  - output : project/csv파일들
## 2) remove_index_from_csv.py : project/csv파일에서 index 삭제
  - output : project2/csv파일들
## 3) insert_date_to_csv.py : project2/csv파일에 date 추가
  - output : project3/csv파일들
## 4) processing_info_from_csv.py : project3/csv파일에서 50개 게임 랭킹 합침
  - output : game_rank_data_top50.csv
  
# 2. 게임정보 크롤링
##1) game_info_full.csv.py : 게임정보 50개 게임대해 크롤링
  - output : game_info_full.csv
  
# 3. youtube 크롤링(한개 게임 대해)
## 1) youtube_url_crawling.py : 한개게임 검색 결과 대해 영상 url 크롤링
  - output : youtube_게임이름_url.csv (youtube_brain_out_url.csv)
## 2) youtube_video_crawling.py : 위에서 크롤링한 영상 url대해 구체적인 영상 정보 크롤링
  - output : youtube_게임이름_video.csv (youtube_brain_out_video.csv)
## 3) youtube_csv_processing.py : 크롤링한 csv파일 정제
  - output : youtube_게임이름_video_regul.csv (youtube_brain_out_video_regul.csv)
## 4) youtube_video_get_count_each_date.py
  - output : youtube_게임이름_count_each_date.csv (youtube_brain_out_count_each_date.csv)
  
# 4. youtube 크롤링(전체 게임 대해)
## 1) youtube_url_crawling_all.py : 전체 게임 검색 결과 대해 영상 url 크롤링
  - output : youtube_game_data/youtube_게임이름_url.csv
## 2) youtube_video_crawling_all.py : 위에서 크롤링한 영상 url대해 구체적인 영상 정보 크롤링
  - output : youtube_game_data/video/youtube_게임이름_video.csv
## 3) youtube_csv_processing_all.py : 크롤링한 csv파일 정제
  - output : youtube_game_data/regul/youtube_게임이름_video_regul.csv
## 4) youtube_video_get_count_each_date_all.py
  - output : youtube_game_data/count_each_date/youtube_게임이름_count_each_date.csv

# 5. 게임, 유튜브 데이터 시각화 파일
## 1) youtube_url_crawling_50games_count.py : 게임당 영상 개수 정리본
  - output : youtube_url_crawling_50games_count.csv
## 2) youtube_graph_from_csv_with_line.py : 전체 게임에 대해 날짜별 랭킹, 조회수, 영상 수 그래프 그림
  - output : graph_img_final/게임이름.png

# 6. 가설 결과 및 시각화 파일
## 1) youtube_video_get_hypothesis_result.py : 한개 게임 대해 가설에 따른 결과 계산
  - output : 콘솔창에서 출력
## 2) youtube_video_get_hypothesis_result_all.py : 여러 게임 대해 가설에 따른 결과 계산
  - output : youtube_hypothesis_result.csv, youtube_hypothesis_result2.csv
## 3) youtube_video_get_hypothesis_graph.py : 위에서 나온 가설 결과에 따른 그래프 그림
  - output : hypothesis_result.png, hypothesis_result2_1.png, hypothesis_result2_1.png
