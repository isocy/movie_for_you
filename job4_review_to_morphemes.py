import pandas as pd

from konlpy.tag import Okt


df_title_review = pd.read_csv('./crawling_data/title_review.csv')
df_title_review = df_title_review.groupby('title')['review'].apply(lambda s: ' '.join(s)).reset_index()

review_series = df_title_review['review']

okt = Okt()
for review_idx in range(len(review_series)):
    review_series[review_idx] = okt.pos(review_series[review_idx], stem=True)

review_series.to_json('./datasets/review_series.json')
