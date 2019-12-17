import pandas as pd
import matplotlib.pyplot as plt




youtube_data = pd.read_csv('./youtube_hypothesis_result.csv', sep=',', header=0, encoding='utf-8-sig')
result = []
t_count = 0
f_count = 0

for data in youtube_data.values:
    if(data[7] == True):
        t_count += 1
    else:
        f_count += 1

result.append(['TRUE', t_count])
result.append(['FALSE', f_count])

youtube_df = pd.DataFrame(result, columns=('hypothesis1', 'result'))
youtube_df.set_index(["hypothesis1"],inplace=True)
youtube_df.plot(kind='bar', figsize=(3, 7), alpha=0.75, rot=0)
plt.savefig('.\\hypothesis_result.png')


result = []
t_count = 0
f_count = 0

for data in youtube_data.values:
    if(data[8] == True):
        t_count += 1
    else:
        f_count += 1

result.append(['TRUE', t_count])
result.append(['FALSE', f_count])

youtube_df = pd.DataFrame(result, columns=('hypothesis2', 'result'))
youtube_df.set_index(["hypothesis2"],inplace=True)
youtube_df.plot(kind='bar', figsize=(3, 7), alpha=0.75, rot=0)
#plt.show()
plt.savefig('.\\hypothesis_result2_1.png')
