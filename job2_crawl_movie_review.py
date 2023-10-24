import os
import re
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

if not os.path.isdir('./crawling_data/'):
    os.mkdir('./crawling_data/')


INITIAL_YEAR = 2020
INITIAL_MONTH = 1
FINAL_YEAR = 2023
FINAL_MONTH = 9

cur_year = INITIAL_YEAR
cur_month = INITIAL_MONTH

title_set = set()
df_title_review = pd.DataFrame(columns=['title', 'review'])

while cur_year != FINAL_YEAR or cur_month != FINAL_MONTH + 1:
    url = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}{:02d}'.format(cur_year, cur_month)
    
    titles = []
    reviews = []
    
    df_temp_title_review = pd.DataFrame()
    
    for ranking_idx in range(1, 31):
        driver.get(url)

        movie_title_element = driver.find_element(
            By.XPATH,
            '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(ranking_idx)
        )
        title = movie_title_element.text
        
        if title in title_set:
            continue
        else:
            title_set.add(title)
        if movie_title_element.get_attribute('href')[-1] == '=':
            continue
        
        movie_title_element.click()
        
        while True:  # Infinite loop for page load
            try:
                driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]/div/div/div')
            except NoSuchElementException:
                continue
            break
        review_tab_element = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a')
        review_tab_element.click()
        
        review_cnt_element = None
        while True:
            try:
                review_cnt_element = driver.find_element(
                    By.XPATH,
                    '//*[@id="mainContent"]/div/div[2]/div[2]/div/strong/span'
                )
            except NoSuchElementException:
                continue
            
            if review_cnt_element.text:
                break
        review_cnt = int(re.compile('[^0-9]').sub('', review_cnt_element.text))
        if review_cnt > 160:
            review_cnt = 160
        
        for click_idx in range((review_cnt + 19) // 30):
            view_more_element = None
            while True:  # Infinite loop for button load
                try:
                    view_more_element = driver.find_element(
                        By.XPATH,
                        '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button'
                    )
                except NoSuchElementException:
                    continue
                
                if not view_more_element.text == '':
                    break
            view_more_element.click()
        
        review_idx = 1
        while review_idx <= review_cnt:
            try:
                review = driver.find_element(
                    By.XPATH,
                    '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]'
                    '/li[{}]/div/p'.format(review_idx)
                ).text
            except NoSuchElementException:
                review_idx += 1
                continue
            refined_review = re.compile('[^가-힣]').sub(' ', review)
            
            titles.append(title)
            reviews.append(refined_review)
            
            review_idx += 1

    df_temp_title_review['title'] = titles
    df_temp_title_review['review'] = reviews
    df_temp_title_review.to_csv(
        './crawling_data/temp_title_review_{}{:02d}.csv'.format(cur_year, cur_month),
        index=False
    )
    df_title_review = pd.concat([df_title_review, df_temp_title_review], axis='rows', ignore_index=True)

    if cur_month == 12:
        cur_year += 1
        cur_month = 1
    else:
        cur_month += 1

df_title_review.to_csv(
    './crawling_data/title_review_{}{:02d}-{}{:02d}.csv'
    .format(INITIAL_YEAR, INITIAL_MONTH, FINAL_YEAR, FINAL_MONTH),
    index=False
)
