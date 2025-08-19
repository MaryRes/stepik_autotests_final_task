
class Urls:

    """A class to manage a list of URLs."""

    BASE_URL = "http://selenium1py.pythonanywhere.com"
    PROMO_BASE_URL = f"{BASE_URL}/catalogue/coders-at-work_207"

    # Генерация promo URLs лениво (при обращении)
    @classmethod
    def get_promo_urls(cls, count=10):
        """Returns list of promo URLs"""
        return [f"{cls.PROMO_BASE_URL}/?promo=offer{no}" for no in range(count)]


    def __init__(self):
        self.urls = []

    def add_url(self, url):
        self.urls.append(url)

    def get_urls(self):
        return self.urls

    @staticmethod
    def get_localized_url(language: str = "en-gb") -> str:
        """
        Returns the localized URL based on the provided language.
        :param language: Language code (e.g., 'en', 'fi', etc.)
        :return: Localized URL
        """
        # Преобразуем формат языка (например, 'en-gb' -> 'en')
        locale = language.split('-')[0] if '-' in language else language

        # Для английского часто нет префикса /en/
        if locale == "en":
            return f"{Urls.BASE_URL}/"
        else:
            return f"{Urls.BASE_URL}/{locale}/"


    @staticmethod
    def main_page_url(language: str = "en-gb") -> str:
        """
        Returns the main page URL for the specified language.
        :param language: Language code (default is 'en')
        :return: Main page URL
        """
        return f"{Urls.get_localized_url(language)}"

    @staticmethod
    def login_page_url(language: str = "en-gb") -> str:
        """
        Returns the login page URL for the specified language.
        :param language: Language code (default is 'en')
        :return: Login page URL
        """
        return f"{Urls.get_localized_url(language)}accounts/login/"


    @staticmethod
    def product_page_url(product_slug: str, language: str = "en-gb") -> str:
        """
        Returns the product page URL for the specified product slug and language.
        :param product_slug: Slug of the product
        :param language: Language code (default is 'en')
        :return: Product page URL
        """
        return f"{Urls.get_localized_url(language)}catalogue/{product_slug}/"


    @staticmethod
    def basket_page_url(language: str = "en-gb") -> str:
        """
        Returns the basket page URL for the specified language.
        :param language: Language code (default is 'en')
        :return: Basket page URL
        """
        return f"{Urls.get_localized_url(language)}basket/"

    @staticmethod
    def catalogue_page_url(language: str = "en-gb") -> str:
        """
        Returns the catalogue page URL for the specified language.
        :param language: Language code (default is 'en-gb')
        :return: Catalogue page URL
        """
        return f"{Urls.get_localized_url(language)}catalogue/"