import pytest
from .urls import BASE_URL
from .pages.locators import BasePageLocators
print(BASE_URL)

@pytest.mark.parametrize('url', [BASE_URL])
def test_guest_can_go_to_login_page(browser, url):
    browser.get(url)
    login_link = browser.find_element(*BasePageLocators.LOGIN_LINK)
    login_link.click()