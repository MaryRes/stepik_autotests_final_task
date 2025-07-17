from selenium.common import InvalidSelectorException, NoSuchElementException

from .base_page import BasePage
from .locators import LoginPageLocators
import selenium


class LoginPage(BasePage):
    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()

    def should_be_login_url(self):
        # реализуйте проверку на корректный url адрес
        current_url = self.browser.current_url
        login = "login"
        assert login in current_url.lower(), "absence of login word in url"

    def should_be_login_form(self):
        # проверка, что есть форма логина
        try:
            login_form = BasePage.is_element_present(self, *LoginPageLocators.LOGIN_FORM)
            message = "Login form is not present"  # <- message должен быть всегда
        except InvalidSelectorException as e:
            login_form = False
            message = f"Invalid selector: {LoginPageLocators.LOGIN_FORM}"
        except NoSuchElementException as e:
            login_form = False
            message = "Login form not found"

        assert login_form, message

    def should_be_register_form(self):
        # реализуйте проверку, что есть форма регистрации на странице
        register_form = BasePage.is_element_present(self, *LoginPageLocators.REGISTRATION_FORM)
        assert register_form, "absence of registration form"