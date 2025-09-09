"""
PAGE OBJECT МОДЕЛЬ СТРАНИЦЫ ЛОГИНА И РЕГИСТРАЦИИ

Данный модуль содержит класс LoginPage для работы со страницей авторизации и регистрации.
Класс предоставляет методы для взаимодействия с формами входа, регистрации новых пользователей
и проверки корректности отображения элементов страницы.

ОСНОВНЫЕ ФУНКЦИОНАЛЬНЫЕ ВОЗМОЖНОСТИ:
- Навигация на страницу логина через клик по ссылке
- Регистрация новых пользователей с автоматической генерацией данных
- Проверка URL страницы логина на корректность
- Валидация наличия форм входа и регистрации на странице
- Заполнение и отправка форм авторизации
"""

import time
from typing import

None

# Импорты Page Object моделей и локаторов
from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    """
    Класс для работы со страницей авторизации и регистрации пользователей.

    Наследует от BasePage и добавляет специфичные методы для:
    - Перехода на страницу логина
    - Регистрации новых пользователей
    - Проверки наличия форм входа и регистрации
    - Валидации URL страницы логина

    Атрибуты:
        browser: Экземпляр веб-браузера для управления страницей
        url: URL-адрес страницы логина
    """

    def go_to_login_page(self) -> None:
        """
        Переходит на страницу логина через клик по ссылке.

        Метод находит ссылку на страницу логина на текущей странице
        и выполняет клик для перехода. Используется когда страница логина
        доступна через ссылку в навигации.

        Пример использования:
            login_page = LoginPage(browser, current_url)
            login_page.go_to_login_page()

        Raises:
            NoSuchElementException: Если ссылка на страницу логина не найдена
        """
        # Ищем элемент ссылки на страницу логина с помощью локатора
        link = self.browser.find_element(*LoginPageLocators.LOGIN_LINK)
        # Выполняем клик по ссылке для перехода
        link.click()

    def register_new_user(self, email: str = "", password: str = "") -> None:
        """
        Регистрирует нового пользователя через форму регистрации.

        Заполняет форму регистрации данными пользователя и отправляет ее.
        Если email не указан, генерирует уникальный email на основе timestamp.
        Если пароль не указан, использует пароль по умолчанию.

        Args:
            email: Email адрес для регистрации. Если не указан, генерируется автоматически
            password: Пароль для регистрации. Если не указан, используется пароль по умолчанию

        Шаги выполнения:
        1. Проверка наличия формы регистрации на странице
        2. Заполнение поля email (генерация уникального если не указан)
        3. Заполнение полей пароля (одинаковое значение в оба поля)
        4. Клик по кнопке отправки формы

        Пример использования:
            login_page.register_new_user()  # Автоматическая генерация данных
            login_page.register_new_user("user@example.com", "secure_password")

        Raises:
            NoSuchElementException: Если элементы формы регистрации не найдены
            AssertionError: Если форма регистрации отсутствует на странице
        """
        # Генерация уникального email на основе текущего времени, если не указан
        if email == "":
            email = str(time.time()) + "@mail.org"

        # Использование пароля по умолчанию, если не указан
        if password == "":
            password = "1234kkfdkg!"

        # Проверяем, что форма регистрации присутствует на странице
        if self.is_element_present(*LoginPageLocators.REGISTRATION_FORM):
            # Заполняем поле email
            email_field = self.browser.find_element(*LoginPageLocators.REGISTRATION_EMAIL)
            email_field.clear()  # Очищаем поле на случай остаточных данных
            email_field.send_keys(email)  # Вводим email

            # Заполняем первое поле пароля
            password_field_1 = self.browser.find_element(*LoginPageLocators.REGISTRATION_PASSWORD1)
            password_field_1.clear()
            password_field_1.send_keys(password)

            # Заполняем второе поле пароля (подтверждение)
            password_field_2 = self.browser.find_element(*LoginPageLocators.REGISTRATION_PASSWORD2)
            password_field_2.clear()
            password_field_2.send_keys(password)

            # Находим и нажимаем кнопку отправки формы регистрации
            submit_button = self.browser.find_element(*LoginPageLocators.REGISTRATION_BUTTON)
            submit_button.click()

    def should_be_login_url(self) -> None:
        """
        Проверяет, что текущий URL содержит подстроку 'login'.

        Метод используется для подтверждения, что браузер находится
        на корректной странице логина/регистрации.

        Пример использования:
            login_page.should_be_login_url()  # Пройдет если URL содержит 'login'

        Raises:
            AssertionError: Если текущий URL не содержит подстроку 'login'
        """
        # Получаем текущий URL и приводим к нижнему регистру для регистронезависимого поиска
        current_url = self.browser.current_url.lower()

        # Проверяем наличие подстроки 'login' в URL
        assert "login" in current_url, \
            f"Current URL '{current_url}' is probably not login page. Expected 'login' in URL"

    def should_be_login_form(self) -> None:
        """
        Проверяет наличие формы входа на странице.

        Убеждается, что форма для авторизации существующих пользователей
        присутствует и доступна для взаимодействия.

        Пример использования:
            login_page.should_be_login_form()  # Пройдет если форма входа найдена

        Raises:
            AssertionError: Если форма входа не найдена на странице
        """
        # Проверяем наличие формы входа с помощью локатора
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), \
            "Login form is not present on the page"

    def should_be_register_form(self) -> None:
        """
        Проверяет наличие формы регистрации на странице.

        Убеждается, что форма для регистрации новых пользователей
        присутствует и доступна для взаимодействия.

        Пример использования:
            login_page.should_be_register_form()  # Пройдет если форма регистрации найдена

        Raises:
            AssertionError: Если форма регистрации не найдена на странице
        """
        # Проверяем наличие формы регистрации с помощью локатора
        assert self.is_element_present(*LoginPageLocators.REGISTRATION_FORM), \
            "Registration form is not present on the page"