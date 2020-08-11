import pymysql as my

class DBHelper:
    '''
    커넥션
    '''
    conn = None
    '''
    생성자
    '''
    def __init__(self):
        self.db_init()
        '''
        멤버 함수
        '''
    def db_init(self):
        self.conn = my.connect(
                host = 'localhost',
                user = 'root',
                password = '1234',
                db = 'shoes_site_db',
                charset = 'utf8',
                cursorclass = my.cursors.DictCursor)

    def db_free(self):
         if self.conn:
            self.conn.close()

    #검색어 가져오기 
    rows = None
    def db_selectKeyword(self):
        with self.conn.cursor() as cursor:
                k_list = []
                sql = "select keyword from tbl_keyword;"
                cursor.execute(sql)
                #fetch = one / fetchall = all(tuples or list)
                rows = cursor.fetchall()
                for row in rows:
                    k_list.append(row['keyword'])
        return k_list

    #신발정보 등록
    def db_insert_data_price(self,title,price,model_name,brand,link,search_site,model_image):
        with self.conn.cursor() as cursor:
                    sql = '''
                        insert into shoes_site_shoe_info
                        (title,price,model_name,brand,link,search_site,model_image)
                        values(%s,%s,%s,%s,%s,%s,%s)
                        '''
                    cursor.execute(sql,(title,price,model_name,brand,link,search_site,model_image))
                    self.conn.commit()
    #발매 정보 등록
    def db_insert_data_datecom(self,title,price,model_name,brand,link,search_site,model_image,date):
        with self.conn.cursor() as cursor:
                    sql = '''
                        insert into shoes_site_datecom_shoe
                        (title,price,model_number,brand,link,search_site,model_image,date)
                        values(%s,%s,%s,%s,%s,%s,%s,%s)
                        '''
                    cursor.execute(sql,(title,price,model_name,brand,link,search_site,model_image,date))
                    self.conn.commit()

    #출시정보 데이터 리셋                
    def db_delete(self):
        with self.conn.cursor() as cursor:
            sql = " DELETE FROM shoes_site_datecom_shoe;"
            cursor.execute(sql)
            self.conn.commit()

    #가격 정보 리셋
    def db_truncate(self,table_name):
        with self.conn.cursor() as cursor:
            sql = 'TRUNCATE TABLE '+ table_name +';'
            cursor.execute(sql)

if __name__ == '__main__':
    db = DBHelper()
    db.db_free()
