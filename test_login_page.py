import pytest
from selenium.webdriver.common.by import By

from .pages.login_page import LoginPage

from .pages.locators import MainPaigeLocators, LoginPageLocators

login_link_element = MainPaigeLocators.LOGIN_LINK
login_form_element = LoginPageLocators.LOGIN_FORM
registration_form_element = LoginPageLocators.REGISTRATION_FORM

# pytest -v --tb=line test_login_page.py

link = "http://selenium1py.pythonanywhere.com/fi/accounts/login/"
def test_should_be_login_page(browser):
    # НЕ ПОНЯТНО
    page = LoginPage(browser, link)
    page.open()
    page.should_be_login_page()