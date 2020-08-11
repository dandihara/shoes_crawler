from selenium import webdriver as driver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import shoe_info
import requests
import pymysql as my
import time
import datetime
import urllib.request
#숫자만 골라내는 라이브러리
import re
import sys
from DBMg import DBHelper as Db

#사이트마다 다른 사이트의 형식을 가졌기에 사이트마다 따로 크롤러제작
main_url_price = 'https://www.endclothing.com/kr/footwear/sneakers'
index_url = ''
#db 커넥션
db = Db()
#상품정보를 담는 리스트(ShoeInfo 리스트)
shoeinfo_list = []
#드라이버 로드
#requests를 통한 헤더 변경 > 사람처럼 보이기
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'\
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,applications/xml;'\
        'q=0.9,image/webp,*/*;q=0.8'}
url = 'https://www.whatismybrowser.com/'\
    'developers/what-http-headers-is-my-browser-sending'
req = session.get(url, headers=headers)
main_dr = driver.Chrome('chromedriver')
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
# site 접속(get)
page_count = 1
#신발 가격 정보
try:
    main_dr.get(main_url_price)
    body = main_dr.find_element_by_css_selector('body')
    #전체 아이템 수
    item_number = int(main_dr.find_element_by_css_selector('#app-container > div.StyledWrapper-sc-1ca44sh-0.nFVci > div > div.ToolbarBody-sc-1ot6ogf-0.fmUIfv > div:nth-child(1) > div > span:nth-child(2)').text)
    pagecount = int(item_number/120) + 1
    i = 1
    for i in range(1,pagecount):
        #신발 정보 리스트 수집
        temp = main_dr.find_element_by_class_name('PlpGrid-sc-25l6fi-5.hhdQwU')
        lis = temp.find_elements_by_class_name('InnerLink-sc-1koxpgo-0.htTaev.ProductCardSC-sc-5sgtnq-3.gJgQuy')
        #신발 정보 스크랩핑
        for li in lis:
            model_number = li.get_attribute('id')
            price = li.find_element_by_css_selector("span[data-test='ProductCard__ProductFinalPrice']").text
            replace_price = int(price[1:].replace(",","")) # 가격만 남기기
            model_and_brand = li.find_element_by_css_selector("span[data-test='ProductCard__PlpName']").text
            temp_li = model_and_brand.split(' ')
            if temp_li[0] == 'New': # New Balance
                brand = temp_li[0] + ' ' +temp_li[1]
                model = ' '.join(temp_li[2:])#split 반대 join
            elif temp_li[0] == 'Polo': # Polo Ralph Lauren
                brand = temp_li[0] + temp_li[1] + temp_li[2]
                model = ' '.join(temp_li[3:])
            elif temp_li[0] == 'Paul': # Paul Smith
                brand = temp_li[0] + temp_li[1]
                model = ' '.join(temp_li[2:])
            elif temp_li[0] == 'Shoes': # Shoes Like Pottery
                brand = temp_li[0] + temp_li[1] + temp_li[2]
                model = ' '.join(temp_li[3:])
            elif temp_li[0] == 'Air':#air jordan
                brand = 'Nike'
                model = ' '.join(temp_li[0:])
            elif temp_li[0] == 'Jordan':
                brand = 'Nike'
                model = ' '.join(temp_li[0:])
            elif temp_li[0] == 'Fred':
                brand = temp_li[0] + temp_li[1]
                model = ' '.join(temp_li[2:])
            elif temp_li[1] == 'North':
                brand = temp_li[0] + temp_li[1] + temp_li[2]
                model = ' '.join(temp_li[3:])       
            else:
                brand = temp_li[0]
                model = ' '.join(temp_li[0:])
            #데이터 삽입
            db.db_insert_data_price(
                model,
                int(replace_price),
                model_number,
                brand,
                li.get_attribute('href'),
                'EndClothing',
                li.find_element_by_css_selector('img').get_attribute('src'))
            main_dr.execute_script("window.scrollBy(0, 100)")
            time.sleep(0.5)
        i = i + 1
        main_dr.get(main_url_price + '?page=' + str(i))
except:#캡차발생시 종료
    main_dr.close()
    main_dr.quit()

main_dr.close()
main_dr.quit()