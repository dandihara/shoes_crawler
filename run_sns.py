from selenium import webdriver as driver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import change_price
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
main_url_datecom = 'https://www.sneakersnstuff.com/en/472/upcoming-releases'#발매 정보
main_url ='https://www.sneakersnstuff.com/en' # + data-src = 이미지 링크
#db 커넥션
db = Db()
#상품정보를 담는 리스트(ShoeInfo 리스트)
shoeinfo_list = []
#이미지 url 정보 리스트
imgs = []
keyword_list = db.db_selectKeyword()
#드라이버 로드
main_dr = driver.Chrome()
# site 접속(get)
count = 1
main_dr.get (main_url_datecom)
dallar = change_price.dallar
#신발 출시 정보
elem = main_dr.find_element_by_css_selector(".filter-products")
lis = elem.find_elements_by_class_name('card.product')
count = 1
for li in lis:
    try:
        card_banner = li.find_element_by_css_selector('.card__banner')
        temp = card_banner.find_element_by_css_selector('.countdown.card__countdown')
        year = temp.get_attribute('data-date-year')
        month = temp.get_attribute('data-date-month')
        day = temp.get_attribute('data-date-day')
        date = year+'-'+month+'-'+day
        convert_date = datetime.datetime.strptime(date,"%Y-%m-%d").date()
        price = float(li.find_element_by_class_name('price__current').text[1:])
        exchange_price = dallar * price
        time.sleep(3)
        db.db_insert_data_datecom(
                li.find_element_by_class_name('card__name').text,#모델명
                round(exchange_price),#가격
                None,#모델 넘버
                li.find_element_by_class_name('card__brand').text,#브랜드
                li.find_element_by_css_selector('a').get_attribute('href'),#링크
                'Sneakersnstuff/SNS',#사이트명
                main_url + li.find_element_by_css_selector('img').get_attribute('data-src'),#모델이미지
                convert_date#발매일
                )

    except:
        price = float(li.find_element_by_class_name('price__current').text[1:])
        exchange_price = dallar * price
        time.sleep(3)
        db.db_insert_data_datecom(
                li.find_element_by_class_name('card__name').text,#모델명
                round(exchange_price),#가격
                None,#모델 넘버
                li.find_element_by_class_name('card__brand').text,#브랜드
                li.find_element_by_css_selector('a').get_attribute('href'),#링크
                'Sneakersnstuff/SNS',#사이트명
                main_url + li.find_element_by_css_selector('img').get_attribute('data-src'),#모델이미지
                None#발매일
                )

#신발 가격 정보
main_dr.get(main_url)
for keyword in keyword_list:
    main_dr.find_element_by_class_name('navbar__link.instant-search-toggle').click()
    time.sleep(3)
    main_dr.find_element_by_id('instant-search-input').send_keys(keyword)
    main_dr.find_element_by_id('instant-search-input').send_keys(Keys.ENTER)
    item_number = main_dr.find_element_by_css_selector('#container > div > main > section > div.search-definition__head > h2 > span').text
    split_list = item_number.split(' ')
    pagecount = int(split_list[0])
    if pagecount % 60 == 0:
        pagecount = int(pagecount/60)
    else:
        pagecount = int(pagecount/60)+1

    for count in range(1,pagecount):
        elem = main_dr.find_element_by_class_name("filter-products")
        lis = elem.find_elements_by_class_name('card.product')
        time.sleep(3)
        for li in lis:
            price = float(li.find_element_by_class_name('price__current').text[1:])
            exchange_price = dallar * price
            brand = li.find_element_by_class_name('card__brand').text
            title = li.find_element_by_class_name('card__name').text
            price = round(exchange_price)
            link = li.find_element_by_css_selector('a').get_attribute('href')
            thumbnail = main_url + li.find_element_by_css_selector('img').get_attribute('data-src')
            #데이터 삽입
            db.db_insert_data_price(
                        title,
                        price,
                        None,
                        brand,
                        link,
                        'Sneakersnstuff/SNS',
                        thumbnail)

        count = count + 1
        main_dr.find_element_by_class_name('pagination__next').click()
        time.sleep(3)

main_dr.close()
main_dr.quit()