BASE_URL = "http://selenium1py.pythonanywhere.com"
LOGIN_PAGE_URL = "http://selenium1py.pythonanywhere.com/fi/accounts/login/"
MAIN_PAGE_URL = "http://selenium1py.pythonanywhere.com"
PRODUCT_PAGE_URL = "http://selenium1py.pythonanywhere.com/fi/catalogue/hacking-exposed-wireless_208/"
TEST_PAGE_URL = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209?promo=midsummer"
TEST_PROMO_PRODUCT_PAGE_URL = "http://selenium1py.pythonanywhere.com/catalogue/the-shellcoders-handbook_209/?promo=newYear"


def get_promo_urls(cls, count=10):
    """Returns list of promo URLs"""
    return [f"{cls.BASE_URL}/?promo=offer{no}" for no in range(count)]
