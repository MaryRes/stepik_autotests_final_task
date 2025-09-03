import pytest
from .pages.login_page import LoginPage
from .pages.main_page import MainPage
from .urls import LOGIN_PAGE_URL, BASE_URL, MAIN_PAGE_URL, PRODUCT_PAGE_URL


@pytest.mark.parametrize('url', [LOGIN_PAGE_URL])
def test_should_be_login_url(browser, url):
    page = LoginPage(browser, url)
    page.open()

    page.should_be_login_url()


@pytest.mark.parametrize('url', [LOGIN_PAGE_URL])
def test_should_be_register_form(browser, url):
    page = LoginPage(browser, url)
    page.open()

    page.should_be_register_form()


@pytest.mark.parametrize('url', [LOGIN_PAGE_URL])
def test_should_be_login_form(browser, url):
    page = LoginPage(browser, url)
    page.open()

    page.should_be_login_form()


@pytest.mark.parametrize('url', [MAIN_PAGE_URL])
def test_guest_can_go_to_login_page(browser, url):
    page = MainPage(browser, url)
    page.open()
    page.go_to_login_page()
    login_page = LoginPage(browser, browser.current_url)
    login_page.go_to_login_page()
    login_page.should_be_login_url()
