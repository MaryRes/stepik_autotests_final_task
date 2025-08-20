import pytest
import selenium
from selenium.webdriver.common.by import By
import locale

from stepik_autotests_final_task.pages.main_page import MainPage
from stepik_autotests_final_task.pages.login_page import LoginPage
from stepik_autotests_final_task.pages.basket_page import BasketPage

from stepik_autotests_final_task.pages.locators import MainPaigeLocators, LoginPageLocators
from stepik_autotests_final_task.conftest import translation_fixture
from stepik_autotests_final_task.urls import Urls

link = "http://selenium1py.pythonanywhere.com/"

main_page_url = Urls.main_page_url("en-gb")


def go_to_login_page(browser):
    login_link = browser.find_element(By.CSS_SELECTOR, "#login_link")
    login_link.click()


@pytest.mark.ui
@pytest.mark.headed
def test_guest_cant_see_product_in_basket_opened_from_main_page(browser, translation_fixture):
    # Гость открывает главную страницу
    page = MainPage(browser, link)  # инициализируем Page Object, п
    page.open()

    # Проверяем, что есть ссылка на корзину в шапке сайта
    page.should_be_basket_link_in_header()  # выполняем метод страницы — проверяем наличие ссылки на корзину в шапке сайта
    # Переходит в корзину по кнопке в шапке сайта
    page.go_to_basket_from_header()  # выполняем метод страницы — переходим в корзину по ссылке в шапке сайта
    # Проверяем, что мы на странице корзины
    page.should_be_in_basket_page()  # выполняем метод страницы — проверяем, что мы на странице корзины
    basket_page = BasketPage(browser, browser.current_url)  # инициализируем Page Object для страницы корзины
    # сообщение о том, что корзина пуста
    basket_empty_message = translation_fixture["basket_is_empty"]
    # Ожидаем, что в корзине нет товаров и есть сообщение о том, что корзина пуста
    assert basket_page.is_basket_empty(basket_empty_message), "Basket is not empty, but should be empty"


@pytest.mark.login_guest
class TestLoginFromMainPage:
    """ Class for testing login functionality from the main page."""

    @pytest.mark.parametrize("link", [main_page_url])
    def test_guest_can_go_to_login_page(self, browser, link):
        """
        Checks that the guest can go to the login page from the main page.
        :param browser:
        :param link:
        :return:
        """
        page = MainPage(browser, link)  # инициализируем Page Object, п
        # передаем в конструктор экземпляр драйвера и url адрес
        page.open()  # открываем страницу
        page.go_to_login_page()  # выполняем метод страницы — переходим на страницу логина

    @pytest.mark.parametrize("link", [main_page_url])
    def test_guest_should_see_login_link(self, browser, link):
        """
        Checks that the login link is present on the main page.
        :param browser:
        :param link:
        :return:
        """
        page = MainPage(browser, link)  # инициализируем Page Object, п
        # передаем в конструктор экземпляр драйвера и url адрес
        page.open()  # открываем страницу
        page.should_be_login_link()  # выполняем метод страницы — проверяем наличие ссылки на логин
