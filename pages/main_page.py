from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from stepik_autotests_final_task.pages.base_page import BasePage
from .locators import MainPaigeLocators
import selenium
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)
        self.wait = WebDriverWait(self.browser, timeout=4, poll_frequency=1)

    def should_be_basket_link_in_header(self):
        """
        Проверяет наличие ссылки на корзину в шапке сайта.
        """
        assert self.is_element_present(*MainPaigeLocators.BASKET_LINK_IN_HEADER), "Basket link is not present in header"

    def go_to_basket_from_header(self):
        """
        Переходит в корзину по ссылке в шапке сайта.
        """
        basket_link_locator = MainPaigeLocators.BASKET_LINK_IN_HEADER
        # Используем явное ожидание, чтобы дождаться кликабельности ссылки
        basket_link = self.wait.until(EC.element_to_be_clickable(basket_link_locator))
        basket_link.click()
        # Явное ожидание, чтобы дождаться загрузки страницы корзины
        self.wait.until(lambda driver: driver.current_url.endswith("/basket/"))

    def should_be_in_basket_page(self):
        """
        Проверяет, что текущая страница является страницей корзины.
        """
        assert self.browser.current_url.endswith("/basket/"), "Not on the basket page"
