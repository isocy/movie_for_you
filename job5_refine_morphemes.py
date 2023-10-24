import pandas as pd

import gdown


review_series = pd.read_json('./datasets/review_series.json', typ='series')
review_series.name = 'review'

gdown.download('https://drive.google.com/uc?id=1TBefeqPHFT_lxObF_WOmzrv891Lik6-U', './datasets/stopwords.csv')
df_stopword = pd.read_csv('./datasets/stopwords.csv', index_col=0)

for review_idx in range(len(review_series)):
    df_morpheme_class = pd.DataFrame(review_series[review_idx], columns=['morpheme', 'class'])
    df_morpheme_class = df_morpheme_class[(df_morpheme_class['class'] == 'Noun') |
                                          (df_morpheme_class['class'] == 'Verb') |
                                          (df_morpheme_class['class'] == 'Adjective')]
    
    morphemes = []
    for morpheme in df_morpheme_class['morpheme']:
        if len(morpheme) > 1 and morpheme not in df_stopword['stopword']:
            morphemes.append(morpheme)
    
    review_series[review_idx] = ' '.join(morphemes)

review_series.dropna().to_csv('./datasets/refined_review_series.csv', index=False)
