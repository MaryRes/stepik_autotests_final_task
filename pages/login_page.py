from .base_page import BasePage
from .locators import LoginPageLocators
#

#
class LoginPage(BasePage):

    def go_to_login_page(self):
        """
        Находит ссылну на страницу логина и кликает на нее
        :return: None
        """
        link = self.browser.find_element(*LoginPageLocators.LOGIN_LINK)
        link.click()

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
