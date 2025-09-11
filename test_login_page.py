"""
МОДУЛЬ ТЕСТИРОВАНИЯ СТРАНИЦЫ ЛОГИНА И РЕГИСТРАЦИИ

Данный модуль содержит тесты для страницы авторизации и регистрации:
- Тесты URL страницы логина
- Тесты наличия форм логина и регистрации
- Тесты перехода на страницу логина с других страниц

ОСНОВНЫЕ СЦЕНАРИИ ТЕСТИРОВАНИЯ:
1. Корректность URL страницы авторизации
2. Наличие и доступность форм логина и регистрации
3. Корректность переходов на страницу логина с других страниц
"""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

# Импорты Page Object моделей
from .pages.login_page import LoginPage
from .pages.main_page import MainPage
from .urls import LOGIN_PAGE_URL, MAIN_PAGE_URL


@pytest.mark.parametrize('url', [LOGIN_PAGE_URL])
def test_should_be_login_url(browser: WebDriver, url: str) -> None:
    """
    Проверяет корректность URL страницы логина.

    Убеждается, что текущий URL соответствует ожидаемому URL страницы авторизации.
    Это важно для безопасности и правильной маршрутизации пользователей.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы логина для тестирования
    """
    # Создаем объект страницы логина
    page = LoginPage(browser, url)

    # Открываем страницу логина
    page.open()

    # Проверяем корректность URL
    page.should_be_login_url()


@pytest.mark.parametrize('url', [LOGIN_PAGE_URL])
def test_should_be_login_form(browser: WebDriver, url: str) -> None:
    """
    Проверяет наличие и доступность формы логина на странице.

    Убеждается, что форма для ввода учетных данных существующих пользователей
    присутствует на странице и доступна для взаимодействия.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы логина для тестирования
    """
    # Создаем объект страницы логина
    page = LoginPage(browser, url)

    # Открываем страницу логина
    page.open()

    # Проверяем наличие формы логина
    page.should_be_login_form()


@pytest.mark.parametrize('url', [LOGIN_PAGE_URL])
def test_should_be_register_form(browser: WebDriver, url: str) -> None:
    """
    Проверяет наличие и доступность формы регистрации на странице.

    Убеждается, что форма для регистрации новых пользователей
    присутствует на странице и доступна для взаимодействия.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы логина для тестирования
    """
    # Создаем объект страницы логина
    page = LoginPage(browser, url)

    # Открываем страницу логина
    page.open()

    # Проверяем наличие формы регистрации
    page.should_be_register_form()


@pytest.mark.parametrize('url', [MAIN_PAGE_URL])
def test_guest_can_go_to_login_page(browser: WebDriver, url: str) -> None:
    """
    Проверяет корректность перехода на страницу логина с главной страницы.

    Тестирует полный сценарий: переход с главной страницы на страницу логина
    и последующую проверку корректности URL целевой страницы.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL главной страницы для тестирования
    """
    # Создаем объект главной страницы
    page = MainPage(browser, url)

    # Открываем главную страницу
    page.open()

    # Переходим на страницу логина через соответствующий элемент
    page.go_to_login_page()

    # Создаем объект страницы логина для текущего URL
    login_page = LoginPage(browser, browser.current_url)

    # Дополнительно переходим на страницу логина (для двойной проверки)
    login_page.go_to_login_page()

    # Проверяем корректность URL страницы логина после перехода
    login_page.should_be_login_url()
