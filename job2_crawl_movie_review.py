import os
import re
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *


if not os.path.isfile('./chrome_driver_path.txt'):
    with open('./job1_install_Chrome_driver.py', 'r') as file:
        exec(file.read())

with open('./chrome_driver_path.txt', 'r') as file:
    service = Service(file.read())

options = Options()
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
              '118.0.0.0 Safari/537.36')
options.add_argument('user_agent=' + user_agent)

driver = webdriver.Chrome(service=service, options=options)


INITIAL_YEAR = 2020
INITIAL_MONTH = 1
FINAL_YEAR = 2023
FINAL_MONTH = 9

cur_year = INITIAL_YEAR
cur_month = INITIAL_MONTH

df_title_review = pd.DataFrame(columns=['title', 'review'])

while cur_year != FINAL_YEAR or cur_month != FINAL_MONTH + 1:
    url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(cur_year, cur_month)
    
    titles = []
    reviews = []
    
    df_temp_title_review = pd.DataFrame()
    
    for ranking_idx in range(1, 31):
        driver.get(url)

        try:
            movie_title_element = driver.find_element(
                By.XPATH, '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(ranking_idx))
        except NoSuchElementException:
            print(cur_year, cur_month, ranking_idx)
            break
        title = movie_title_element.text
        movie_title_element.click()
        
        review_tab_element = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')
        review_tab_element.click()
        
        while True:  # Infinite loop for loading all reviews
            try:
                view_more_element = driver.find_element(
                    By.XPATH, '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button')
                view_more_element.click()
            except NoSuchElementException:
                break
        
        review_idx = 1
        while True:
            try:
                review = driver.find_element(
                    By.XPATH, '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]'
                              '/li[{}]/div/p'.format(review_idx))
            except NoSuchElementException:
                break
            refined_review = re.compile('[^가-힣]').sub(' ', review)
            
            titles.append(title)
            reviews.append(refined_review)
            
            review_idx += 1

    df_temp_title_review['title'] = titles
    df_temp_title_review['review'] = reviews
    df_title_review = pd.concat([df_title_review, df_temp_title_review], axis='rows', ignore_index=True)

    if cur_month == 12:
        cur_year += 1
        cur_month = 1
    else:
        cur_month += 1

if not os.path.isdir('./crawling_data/'):
    os.mkdir('./crawling_data/')

df_title_review.to_csv('./crawling_data/title_review_{}{:02d}-{}{:02d}.csv'
                       .format(INITIAL_YEAR, INITIAL_MONTH, FINAL_YEAR, FINAL_MONTH))
