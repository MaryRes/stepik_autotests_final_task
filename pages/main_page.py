from .base_page import BasePage
from .locators import BasePageLocators


class MainPaige(BasePage):

    def go_to_login_page(self):
        login_link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        login_link.click()
