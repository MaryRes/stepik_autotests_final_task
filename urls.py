BASE_URL = "http://selenium1py.pythonanywhere.com"
LOGIN_PAGE_URL = "http://selenium1py.pythonanywhere.com/fi/accounts/login/"
MAIN_PAGE_URL = ""
PRODUCT_PAGE_URL = ""
TEST_PAGE_URL = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209?promo=midsummer"

def get_promo_urls(cls, count=10):
    """Returns list of promo URLs"""
    return [f"{cls.BASE_URL}/?promo=offer{no}" for no in range(count)]

