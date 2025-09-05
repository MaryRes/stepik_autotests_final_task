from selenium.webdriver.common.by import By

from .base_page import BasePage
from .locators import BasePageLocators


class MainPage(BasePage):

    def go_to_basket_page(self):
        """
        Находит в шапке сайта ссылну на страницу корзины и кликает на нее
        :return: None
        """
        link = self.browser.find_element(*BasePageLocators.BASKET_LINK_IN_HEADER)
        link.click()

    def should_be_login_link(self):
        self.browser.find_element(*BasePageLocators.LOGIN_LINK)
