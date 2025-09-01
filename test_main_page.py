import pytest
from .urls import BASE_URL
from .pages.locators import BasePageLocators
from .pages.main_page import MainPaige
from .pages.base_page import BasePage
print(BASE_URL)

@pytest.mark.parametrize('url', [BASE_URL])
def test_guest_can_go_to_login_page(browser, url):
    page = MainPaige(browser, url)
    page.open()
    page.go_to_login_page()


