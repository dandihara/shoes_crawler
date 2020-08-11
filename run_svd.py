from selenium import webdriver as driver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import change_price
import requests
import shoe_info
import pymysql as my
import time
import datetime
import urllib.request
#숫자만 골라내는 라이브러리
import re
import sys
from DBMg import DBHelper as Db
#사이트마다 다른 사이트의 형식을 가졌기에 사이트마다 따로 크롤러제작
main_url_price = 'https://www.sivasdescalzo.com/en/lifestyle/sneakers'
index_url = ''
#db 커넥션
db = Db()
#상품정보를 담는 리스트(ShoeInfo 리스트)
shoeinfo_list = []
#이미지 url 정보 리스트
imgs = []
#드라이버 로드
main_dr = driver.Chrome('chromedriver')
#requests를 통한 헤더 변경 > 사람처럼 보이기
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'\
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,applications/xml;'\
        'q=0.9,image/webp,*/*;q=0.8'}
url = 'https://www.whatismybrowser.com/'\
    'developers/what-http-headers-is-my-browser-sending'
req = session.get(url, headers=headers)
number = 1
page_count = 1
#환율 정보 (유로화)
euro = change_price.euro
#신발 가격 정보
main_dr.get(main_url_price)
for page_count in range(1,40):
    time.sleep(2)
    body = main_dr.find_element_by_class_name('products-list.medium-block-grid-3.large-block-grid-4')#전체페이지
    #신발 정보 리스트 수집
    lis = body.find_elements_by_tag_name('li')
    #신발 정보 스크랩핑
    for li in lis:
        thumbnail = li.find_element_by_css_selector('body > main > div:nth-child(3) > div > div.row.product-list-row > ul > li:nth-child('+ str(number) +') > div > a > img').get_attribute('src')
        link = li.find_element_by_css_selector('body > main > div:nth-child(3) > div > div.row.product-list-row > ul > li:nth-child('+ str(number)  +') > div > a').get_attribute('href')
        brand = li.find_element_by_class_name('brand').text
        title = li.find_element_by_class_name('model').text
        price = int(li.find_element_by_tag_name('b').text) * euro
        number = number + 1
        #db에 저장
        db.db_insert_data_price(
                                title,
                                price,
                                None,
                                brand,
                                link,
                                'SVD',
                                thumbnail)
        #페이지 로딩을 위해 스크롤을 내림
        main_dr.execute_script("window.scrollBy(0, 60)")
    time.sleep(3)
    #다음페이지
    main_dr.find_element_by_xpath('//*[@title="Next page"]').click()
    page_count = page_count + 1
    number = 1

main_dr.close()
main_dr.quit()