from selenium.webdriver.common.by import By

from .base_page import BasePage
from .locators import BasePageLocators


class MainPage(BasePage):

    def go_to_login_page(self):
        login_link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        login_link.click()

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"
