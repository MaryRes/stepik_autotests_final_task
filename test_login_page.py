import pytest
from selenium.webdriver.common.by import By

from .pages.login_page import LoginPage
from .pages.main_page import MainPage

from .pages.locators import MainPaigeLocators, LoginPageLocators

login_link_element = MainPaigeLocators.LOGIN_LINK
login_form_element = LoginPageLocators.LOGIN_FORM
registration_form_element = LoginPageLocators.REGISTRATION_FORM

# pytest -v --tb=line test_login_page.py

login_page_link = "http://selenium1py.pythonanywhere.com/fi/accounts/login/"
link = "http://selenium1py.pythonanywhere.com"

def test_should_be_login_page(browser):
    # НЕ ПОНЯТНО
    page = LoginPage(browser, link)
    page.open()
    page.should_be_login_page()


def test_guest_should_go_to_login_page(browser):
    page = MainPage(browser, link)
    page.open()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.should_be_login_page()
