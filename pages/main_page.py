from .base_page import BasePage
from .locators import MainPaigeLocators
import selenium
from selenium.webdriver.common.by import By


class MainPage(BasePage):

    def go_to_login_page(self):
        login_link = self.browser.find_element(*MainPaigeLocators.LOGIN_LINK)
        login_link.click()
        alert = self.browser.switch_to.alert
        alert.accept()

    def should_be_login_link(self):
        assert self.is_element_present(*MainPaigeLocators.LOGIN_LINK), "Login link is not presented"
