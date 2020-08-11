# 상품정보를 담는 클래스
class ShoeInfo:
    #멤버변수 (실제 컬럼보다는 작게 세팅)
    title = ''
    brand = ''
    price = ''
    link = ''
    img = ''
    model_name = ''
    search_site = ''
    #생성자
    def __init__(self, brand, title, price, link, img, model_number = None,searching_site = None):
        self.brand = brand
        self.title = title
        self.price = price
        self.link = link
        self.img = img
        self.model_number = model_number
        self.searching_site = searching_site