import pandas as pd
import glob

data_path = glob.glob('./crawling_data/*')

df = pd.DataFrame()

for path in data_path:
    df_temp = pd.read_csv(path)
    # nan 값 제거
    df_temp.dropna(inplace=True)
    # 중복 제거
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)

# 중복 제거
df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./crawling_data/reviews_2017~2019.csv', index=False)