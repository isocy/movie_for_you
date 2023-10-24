import collections

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

from wordcloud import WordCloud


font_path = './fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')
