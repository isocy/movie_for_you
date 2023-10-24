from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time
import datetime

options = Options()
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 '
              'Safari/537.36')
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('--no-sandbox')

# with open('./chrome_driver_path.txt', 'r') as f:
#     service = Service(executable_path=f.read())

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

year = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

# 중복된 제목을 저장하기 위한 집합(set)을 생성
previous_titles = []

# df_title = pd.DataFrame()
df_title = pd.DataFrame(columns=['title', 'review'])

# 년도 지정
for i in range(4, 7):
    url_segment = 'https://movie.daum.net/ranking/boxoffice/monthly?date={}'.format(year[i])

    # 월 지정
    for j in range(0, 12):
        refined_titles = []
        url = url_segment + '{}'.format(month[j])
        driver.get(url)

        for k in range(1, 31):
            refined_reviews = []
            address = None
            # 제목 수집
            while True:  # infinite loop for 'StaleElementReferenceException'
                try:
                    title = driver.find_element('xpath',
                                                '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(
                                                    k)).text
                except StaleElementReferenceException:
                    continue
                except NoSuchElementException:
                    # print(category_idx, page, ul_idx, li_idx)
                    try:
                        title = driver.find_element('xpath',
                                                    '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(
                                                        k)).text
                    except NoSuchElementException:
                        break
                refined_title = re.compile('[^가-힣]').sub(' ', title)
                # 만약 제목이 이미 존재한다면 크롤링을 건너뛴다
                # if refined_title in unique_titles:
                #     continue
                refined_titles.append(refined_title)
                # 집합에 제목을 추가
                # unique_titles.add(refined_title)
                print(refined_titles)
                break

            # 제목 클릭
            element_title = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(k))
            address = element_title.get_attribute('href')
            if address[-1] == '=':
                continue
            element_title.click()

            # 평점 클릭
            while (1):
                try:
                    driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]/div/div/div')
                    break
                except:
                    continue
            element_review = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')
            element_review.click()
            time.sleep(1)

            review_num = None


            # 평점 더보기 5번 클릭
            for l in range(5):
                try:
                    element_review_more = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button')))
                    element_review_more.click()
                    time.sleep(0.5)  # 클릭 후 몇 초 동안 기다릴지 조절 가능
                except TimeoutException:
                    break  # 더보기 버튼이 더 이상 활성화되지 않으면 반복문 종료

            while (1):
                try:
                    review_num = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[2]/div/strong/span').text
                    break
                except:
                    continue
            review_num = review_num[1:-2]
            review_num = int(review_num)
            print(review_num)

            # 리뷰 크롤링
            if review_num > 161:
                for m in range(1, 161):
                    while True:  # infinite loop for 'StaleElementReferenceException'
                        try:
                            review = driver.find_element('xpath',
                                                        '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(
                                                        m)).text
                        except StaleElementReferenceException:
                            continue
                        except NoSuchElementException:
                            try:
                                review = driver.find_element('xpath',
                                                            '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(
                                                            m)).text
                            except NoSuchElementException:
                                break
                        refined_review = re.compile('[^가-힣]').sub(' ', review)
                        # if review.strip(' ') == '':
                        #     continue
                        refined_reviews.append(refined_review)
                        # print(refined_reviews)
                        break
            else:
                for m in range(1, review_num+1):
                    while True:  # infinite loop for 'StaleElementReferenceException'
                        try:
                            review = driver.find_element('xpath',
                                                         '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(
                                                             m)).text
                        except StaleElementReferenceException:
                            continue
                        except NoSuchElementException:
                            try:
                                review = driver.find_element('xpath',
                                                             '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(
                                                                 m)).text
                            except NoSuchElementException:
                                break
                        refined_review = re.compile('[^가-힣]').sub(' ', review)
                        refined_reviews.append(refined_review)
                        # print(refined_reviews)
                        break
            # 이전 페이지로 이동
            driver.back()
            driver.back()

            df_review = pd.DataFrame(refined_reviews, columns=['review'])
            df_review['title'] = refined_titles[k-1]
            df_title = pd.concat([df_title, df_review], axis='rows', ignore_index=True)

            # titles.append(title)
            # reviews.append(review)
            # df= pd.DataFrame({'title':titles, 'review':reviews})

        df_title.to_csv('./crawling_data/Movie_crawling_data_{}_{}.csv'.format(year[i], month[j]), index=False)