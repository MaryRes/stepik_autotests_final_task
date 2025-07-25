import pytest
import selenium
from selenium.webdriver.common.by import By

from .pages.main_page import MainPage
from .pages.login_page import LoginPage

from .pages.locators import MainPaigeLocators, LoginPageLocators

link = "http://selenium1py.pythonanywhere.com/"


def go_to_login_page(browser):
    login_link = browser.find_element(By.CSS_SELECTOR, "#login_link")
    login_link.click()


def test_guest_can_go_to_login_page(browser):
    page = MainPage(browser=browser, url=link)  # инициализируем Page Object, п
    # передаем в конструктор экземпляр драйвера и url адрес

    page.open()  # открываем страницу
    page.go_to_login_page()  # выполняем метод страницы — переходим на страницу логина


def test_guest_should_see_login_link(browser):
    page = MainPage(browser, link)  # инициализируем Page Object, п
    # передаем в конструктор экземпляр драйвера и url адрес
    page.open()  # открываем страницу
    page.should_be_login_link()  # выполняем метод страницы — переходим на страницу логина
