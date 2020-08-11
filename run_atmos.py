from selenium import webdriver as driver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
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
main_url_price = 'http://atmos-seoul.com/shop/shopbrand.html?xcode=003&type=N&mcode=003&gf_ref=Yz00OGhxaHI='
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
# site 접속(get)
page_count = 1
#신발 가격 정보
main_dr.get(main_url_price)
#전체 아이템 수
page = main_dr.find_element_by_css_selector('#productClass > div.page-body.prd-page > div.prd-list-wrap > div.item-wrap.prd-parts > div.paging > a.last').get_attribute('href')
temp = page.split('=')
pagecount = int(temp[-1])
i = 1
for i in range(1,pagecount):
    time.sleep(2)
    body = main_dr.find_element_by_class_name('item-wrap.prd-parts')#전체페이지
    #신발 정보 리스트 수집
    lis = body.find_elements_by_class_name('item-list')
    #신발 정보 스크랩핑
    for li in lis:
        brand = li.find_element_by_class_name('list-brand-name').text
        title = li.find_element_by_class_name('prd-name').text
        price = li.find_element_by_class_name('prd-price').text
        if price == 'Sold Out':
            price = 'soldout'
        else:
            price = price.replace(',','')
            price = price[:-1]
            replace_price = int(price)
        thumb = li.find_element_by_css_selector('img').get_attribute('src')
        href = li.find_element_by_css_selector('a').get_attribute('href')
        if price == 'soldout':
            continue
        #데이터 삽입
        db.db_insert_data_price(
            title,
            int(replace_price),
            None,
            brand,
            li.find_element_by_css_selector('a').get_attribute('href'),
            'Atmos',
            li.find_element_by_css_selector('img').get_attribute('src'))
        time.sleep(0.5)
    i = i + 1
    main_dr.get('http://atmos-seoul.com/shop/shopbrand.html?type=Y&xcode=003&mcode=003&sort=&page=' + str(i))

main_dr.close()
main_dr.quit()