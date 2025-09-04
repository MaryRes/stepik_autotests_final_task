import pytest
from .urls import BASE_URL, MAIN_PAGE_URL
from .pages.main_page import MainPage
from .pages.basket_page import BasketPage


@pytest.mark.parametrize('url', [BASE_URL])
def test_guest_can_go_to_login_page(browser, url):
    page = MainPage(browser, url)
    page.open()
    page.go_to_login_page()


@pytest.mark.parametrize('url', [BASE_URL])
def test_should_be_login_link(browser, url):
    page = MainPage(browser, url)
    page.open()
    page.should_be_login_link()


@pytest.mark.parametrize('url', [MAIN_PAGE_URL])
def test_guest_cant_see_product_in_basket_opened_from_main_page(browser, url):

    # Гость открывает главную страницу
    page = MainPage(browser, url)
    page.open()
    # Переходит в корзину по кнопке в шапке сайта
    page.go_to_basket_page()

    # Ожидаем, что в корзине нет товаров
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_basket_empty()
    # Ожидаем, что есть текст о том что корзина пуста
    basket_page.should_display_empty_basket_message()

