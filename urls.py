BASE_URL = "http://selenium1py.pythonanywhere.com"
LOGIN_PAGE_URL = ""
MAIN_PAGE_URL = ""
PRODUCT_PAGE_URL = ""


def get_promo_urls(cls, count=10):
    """Returns list of promo URLs"""
    return [f"{cls.BASE_URL}/?promo=offer{no}" for no in range(count)]

