from selenium import webdriver as driver
from bs4 import BeautifulSoup as bs
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
main_url_datecom = 'https://www.kasina.co.kr/main/html.php?htmid=proc/datedrop.html'#발매 정보
main_url_price = 'https://www.kasina.co.kr/goods/goods_list.php?cateCd=013'
index_url = ''
#db 커넥션
db = Db()
#상품정보를 담는 리스트(ShoeInfo 리스트)
shoeinfo_list = []
#이미지 url 정보 리스트
imgs = []
#드라이버 로드
main_dr = driver.Chrome()
# site 접속(get)
main_dr.get (main_url_datecom)
page_count = 1
#링크값을 사용할건가? 우리 서버에 업로드 할것인가??(사진은 업로드 방식이 우월
# 처리속도의 문제와 DB의 크기가 너무 방대해져 좋지 않은 스타일이다.)
#신발 출시 정보
elem = main_dr.find_element_by_css_selector(".dropdate.datecom")
lis = elem.find_elements_by_tag_name('li')
count = 1
soldout_token = 1
for li in lis:
    uls = li.find_elements_by_css_selector('p')
    date = li.find_element_by_css_selector('li > b').text
    nonspace_date = date.replace(" ","")
    replace_date = nonspace_date.replace(".","-")
    convert_date = datetime.datetime.strptime(replace_date,"%Y-%m-%d").date()
    db.db_insert_data_datecom(
                    li.find_element_by_css_selector('p > b').text,
                    uls[-1].text,
                    uls[-2].text,
                    li.find_element_by_css_selector('p').text,
                    main_url_datecom,
                    'Kasina',
                    li.find_element_by_css_selector('img').get_attribute('src'),
                    convert_date
                    )

#신발 가격 정보
main_dr.get(main_url_price)
#전체 페이지 수 구하기
temp = main_dr.find_element_by_class_name('pagination.pagination-sm')
page_count_max = int(len(temp.find_elements_by_css_selector('li')))
#신발 정보 스크랩핑
#숫자 범위  = for 단위 in range(시작,끝) / 리스트 = for 소단위 in 대단위
for page_count in range(1,page_count_max):
    elem = main_dr.find_element_by_class_name('list')
    lis = elem.find_elements_by_css_selector('li')
    count = 0
    for li in lis:
        price = li.find_element_by_class_name('cost').text
        replace_price = price[1:].replace(",","")
        obj = shoe_info.ShoeInfo(
                            li.find_element_by_class_name('brand').text,
                            li.find_element_by_id('gonm').text,
                            replace_price,
                            li.find_element_by_css_selector('a').get_attribute('href'),
                            li.find_element_by_css_selector('img').get_attribute('src')
                    )
        shoeinfo_list.append( obj )
        count = count + 1
        if li.find_element_by_class_name('cost').text == 'soldout':
            soldout_token = 0
            break
        if count == 40:
            page_count = page_count + 1
            main_dr.get('https://www.kasina.co.kr/goods/goods_list.php?page='+str(page_count)+'&cateCd=013')
            #진행 솔드아웃 나오면 종료
    if soldout_token == 0:
        break  

for ShoeInfo in shoeinfo_list[:-1]:
    main_dr.get(ShoeInfo.link)
    model_number = main_dr.find_element_by_xpath('//*[@id="quickbuy"]/div[1]/div/div[2]').text
    replace_model_number = model_number.split(' ')
    db.db_insert_data_price(
                    ShoeInfo.title,
                    int(ShoeInfo.price),
                    replace_model_number[2],
                    ShoeInfo.brand,
                    ShoeInfo.link,
                    'Kasina',
                    ShoeInfo.img)
    
main_dr.close()
main_dr.quit()