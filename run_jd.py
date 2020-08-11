from selenium import webdriver as driver
from bs4 import BeautifulSoup as bs
import shoe_info
import pymysql as my
import time
import urllib.request
#숫자만 골라내는 라이브러리
import re
from DBMg import DBHelper as Db

#사이트마다 다른 사이트의 형식을 가졌기에 사이트마다 따로 크롤러제작
main_url = 'https://www.jdsports.co.kr/main/main.php'
index_url = 'https://www.jdsports.co.kr/'
#db 커넥션
db = Db()
#키워드 저장리스트
keyword_list = db.db_selectKeyword()
#상품정보를 담는 리스트(ShoeInfo 리스트)
shoeinfo_list = []
#이미지 url 정보 리스트
imgs = []
#드라이버 로드
main_dr = driver.Chrome()
# site 접속(get)
main_dr.get (main_url)
#모델명 패턴
pattern = '\d+/d+'

#링크값을 사용할건가? 우리 서버에 업로드 할것인가??(사진은 업로드 방식이 우월
# 처리속도의 문제와 DB의 크기가 너무 방대해져 좋지 않은 스타일이다.)
#스크랩핑 시작시에 테이블 리셋(중복 방지 위한 자동 리셋)
for keyword in keyword_list:
#검색창 찾아가서 검색
        main_dr.find_element_by_id('search').send_keys(keyword)
        time.sleep(3)
        main_dr.find_element_by_xpath('/html/body/header/div/div[2]/div[1]/nav/ul/li[1]/div/form/button').click()
        pagecount = int(main_dr.find_element_by_class_name('pageCount').text[:2])
        if int(main_dr.find_element_by_class_name('pageCount').text[:2])%24 == 0:
                pagecount =  int(main_dr.find_element_by_class_name('pageCount').text[:2])/24
        else:
                pagecount = int(pagecount/24)+1
        
        for n in range(1,int(pagecount)):
                elem = main_dr.find_element_by_class_name('comp-goods')
                lis = elem.find_elements_by_tag_name('li')
                for li in lis:
                        #데이터 모음
                        obj = shoe_info.ShoeInfo(
                                li.find_element_by_class_name('brand').text,
                                li.find_element_by_class_name('title').text,
                                li.find_element_by_class_name('point-color3').text,
                                li.find_element_by_css_selector('a').get_attribute('href'),
                                li.find_element_by_css_selector('img').get_attribute('src')
                        )
                        shoeinfo_list.append( obj )
                n = n+1
                main_dr.get('https://www.jdsports.co.kr/front/productsearch.php?block=0&gotopage='+str(n) 
                +'&listnum=24&brand=&color=&size=&sel_cate_code=&thr=sw&sort=recent&begin_price=0&end_price=0&sale=&sm_search='+keyword)

        for ShoeInfo in shoeinfo_list:
                # ShoeInfo = shoeinfo
                #가격 문자열 숫자로 변형
                numbers = re.findall("\d+",ShoeInfo.price)
                ShoeInfo.price = ''
                for number in numbers:
                         ShoeInfo.price = ShoeInfo.price + number
                #링크 데이터에서 실정보 획득(링크 가공)
                arr = ShoeInfo.link
                link = arr.replace('javascript:prod_detail(','') 
                detail_link = link[1:-3]
                main_dr.get('https://www.jdsports.co.kr/front/productdetail.php?productcode=' + detail_link)
                time.sleep(1)
                var = main_dr
                if(ShoeInfo.brand == 'adidas'):
                 ShoeInfo.model_number = var.find_element_by_css_selector('#contents > main > div > div.detail_area > section.goods-detail-info.tab-list.tab-detail-list02.active > div.cont-info > dl:nth-child(1) > dd').text[0:6]
                 #contents > main > div > div.detail_area > section.goods-detail-info.tab-list.tab-detail-list02.active > div.cont-info > dl:nth-child(1) > dd
                else:
                 ShoeInfo.model_number = var.find_element_by_css_selector('#contents > main > div > div.detail_area > section.goods-detail-info.tab-list.tab-detail-list02.active > div.cont-info > dl:nth-child(1) > dd').text
                

                #DB 입력
                db.db_insert_data_price(
                        ShoeInfo.title,
                        int(ShoeInfo.price),
                        ShoeInfo.model_number,
                        ShoeInfo.brand,
                        'https://www.jdsports.co.kr/front/productdetail.php?productcode=' + detail_link,
                        'JD Sports',
                        ShoeInfo.img)
        n = 1
        shoeinfo_list = []

main_dr.close()
main_dr.quit()
