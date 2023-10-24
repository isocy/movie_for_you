import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_review.csv')
df.dropna(inplace=True)
df.info()
print(df.head(10))

one_sentences = []
for title in df['title'].unique():  # 영화제목이 중복되지 않는 리스트
    temp = df[df['title']== title]  # title 값이 같은 review 를 인덱싱
    one_sentence = ' '.join(temp['cleaned_sentences'])
    one_sentences.append(one_sentence)
df_one = pd.DataFrame({'title': df['title'].unique(), 'review': one_sentences})
print(df_one.head())
df_one.info()
df_one.to_csv('./crawling_data/cleaned_one_review.csv', index=False)