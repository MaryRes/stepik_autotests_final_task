import pytest
from .urls import BASE_URL
from .pages.main_page import MainPage


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
