from stepik_autotests_final_task.pages.base_page import BasePage
from .locators import MainPaigeLocators
import selenium
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)
