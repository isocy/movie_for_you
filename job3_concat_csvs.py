import pandas as pd


df_title_review = pd.concat([
    pd.read_csv('./crawling_data/title_review_201310-201612.csv'),
    pd.read_csv('./crawling_data/title_review_201701-201912.csv'),
    pd.read_csv('./crawling_data/title_review_202001-202309.csv')
], axis='rows', ignore_index=True).drop_duplicates().dropna()

df_title_review.to_csv('./crawling_data/title_review.csv', index=False)
