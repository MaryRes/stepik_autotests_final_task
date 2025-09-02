import pytest
from .pages.login_page import LoginPage
from .pages.locators import LoginPageLocators
from .urls import LOGIN_PAGE_URL, BASE_URL



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