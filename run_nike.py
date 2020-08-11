from selenium import webdriver as driver
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
main_url_datecom = 'https://www.nike.com/kr/launch/?type=upcoming&activeDate=date-filter:AFTER' #발매 정보
main_url_price = 'https://www.kasina.co.kr/goods/goods_list.php?cateCd=013'
index_url = ''
#requests를 통한 헤더 변경 > 사람처럼 보이기
session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'\
    'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
    'Accept':'text/html,application/xhtml+xml,applications/xml;'\
        'q=0.9,image/webp,*/*;q=0.8'}
url = 'https://www.whatismybrowser.com/'\
    'developers/what-http-headers-is-my-browser-sending'
req = session.get(url, headers=headers)
#db 커넥션
db = Db()
#상품정보를 담는 리스트(ShoeInfo 리스트)
shoeinfo_list = []
#드라이버 로드
main_dr = driver.Chrome()
# site 접속(get)
main_dr.get (main_url_datecom)
page_count = 1
#링크값을 사용할건가? 우리 서버에 업로드 할것인가??(사진은 업로드 방식이 우월
# 처리속도의 문제와 DB의 크기가 너무 방대해져 좋지 않은 스타일이다.)
time.sleep(3)
#신발 출시 정보
elem = main_dr.find_element_by_class_name("uk-grid.item-list-wrap.gallery")
lis = elem.find_elements_by_class_name('launch-list-item.upcomingItem')
count = 1
for li in lis:
    date = li.get_attribute('data-active-date').split(' ')
    thumnail = li.find_element_by_css_selector('img').get_attribute('src')
    title = li.find_element_by_class_name('txt-description').text
    convert_date = datetime.datetime.strptime(date[0],"%Y-%m-%d").date()

    db.db_insert_data_datecom(
                    title,
                    0,
                    None,
                    'Nike',
                    li.find_element_by_css_selector('a').get_attribute('href'),
                    'nike.com',
                    thumnail,
                    convert_date
                    )
    time.sleep(3)                   

main_dr.close()
main_dr.quit()