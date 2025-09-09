from .base_page import BasePage
from .locators import LoginPageLocators
import time


#
class LoginPage(BasePage):

    def go_to_login_page(self):
        """
        Находит ссылну на страницу логина и кликает на нее
        :return: None
        """
        link = self.browser.find_element(*LoginPageLocators.LOGIN_LINK)
        link.click()

    def register_new_user(self, email="", password=""):
        if email == "":
            email = str(time.time()) + "@mail.org"
        if password == "":
            password = "1234kkfdkg!"

        if self.is_element_present(*LoginPageLocators.REGISTRATION_FORM):
            email_field = self.browser.find_element(*LoginPageLocators.REGISTRATION_EMAIL)
            email_field.clear()
            email_field.send_keys(email)

            password_field_1 = self.browser.find_element(*LoginPageLocators.REGISTRATION_PASSWORD1)
            password_field_1.clear()
            password_field_1.send_keys(password)

            password_field_2 = self.browser.find_element(*LoginPageLocators.REGISTRATION_PASSWORD2)
            password_field_2.clear()
            password_field_2.send_keys(password)

            submit_button = self.browser.find_element(*LoginPageLocators.REGISTRATION_BUTTON)
            submit_button.click()

    def should_be_login_url(self):
        """
        Проверяет, что подстрока "login" есть в текущем url браузера.
        :return: None
        """

        current_url = self.browser.current_url.lower()
        assert "login" in current_url, f"Current URL {current_url} is probably not login page"

    def should_be_login_form(self):
        """
        Проверяет, что форма для входа в кабинет присутствует на странице
        :return: None
        """
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), \
            "Login form is not present in the page"

    def should_be_register_form(self):
        """
        Проверяет, что форма для регистрации нового пользователя присутствует на странице
        :return: None
        """
        assert self.is_element_present(*LoginPageLocators.REGISTRATION_FORM), \
            "Registration form is not present in the page"
