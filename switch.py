from DBMg import DBHelper as Db
db = Db()
#데이터베이스 초기화
db.db_delete()
db.db_truncate('shoes_site_shoe_info')
#웹크롤러 리스트
import run_atmos
import run_jd
import run_kasina
import run_svd
import run_nike
import run_sns
import run_end