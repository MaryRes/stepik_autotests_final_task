"""
МОДУЛЬ ТЕСТИРОВАНИЯ ГЛАВНОЙ СТРАНИЦЫ

Данный модуль содержит тесты для главной страницы:
- Тесты перехода на страницу логина
- Тесты наличия элементов интерфейса
- Тесты перехода в с главной страницы в корзину

ОСНОВНЫЕ СЦЕНАРИИ ТЕСТИРОВАНИЯ:
1. Доступность и работоспособность ссылки на страницу логина
2. Наличие элементов интерфейса на главной странице
3. Поведение пустой корзины при переходе с главной страницы
"""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

# Импорты Page Object моделей
from .urls import BASE_URL, MAIN_PAGE_URL
from .pages.main_page import MainPage
from .pages.basket_page import BasketPage


@pytest.mark.login_guest
@pytest.mark.parametrize('url', [MAIN_PAGE_URL])
class TestLoginFromMainPage:
    """
    Тесты функциональности логина для гостевых пользователей с главной страницы.

    Класс содержит тесты проверки перехода на страницу авторизации
    и наличия соответствующих элементов интерфейса.
    """

    def test_guest_can_go_to_login_page(self, browser: WebDriver, url: str) -> None:
        """
        Проверяет возможность перехода на страницу логина с главной страницы.

        Тестирует работоспособность ссылки/кнопки перехода к авторизации.

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

    def test_guest_should_see_login_link(self, browser: WebDriver, url: str) -> None:
        """
        Проверяет наличие и видимость ссылки на страницу логина на главной странице.

        Убеждается, что элемент для перехода к авторизации присутствует в DOM
        и видим для пользователя.

        Args:
            browser: Экземпляр Selenium WebDriver
            url: URL главной страницы для тестирования
        """
        # Создаем объект главной страницы
        page = MainPage(browser, url)

        # Открываем главную страницу
        page.open()

        # Проверяем наличие и видимость ссылки на страницу логина
        page.should_be_login_link()


@pytest.mark.parametrize('url', [MAIN_PAGE_URL])
def test_guest_cant_see_product_in_basket_opened_from_main_page(browser: WebDriver, url: str) -> None:
    """
    Проверяет состояние пустой корзины при переходе с главной страницы.

    Тестирует сценарий, когда гость переходит в корзину без добавления товаров
    и проверяет корректное отображение пустой корзины.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL главной страницы для тестирования
    """
    # Создаем объект главной страницы и открываем ее
    page = MainPage(browser, url)
    page.open()

    # Переходим в корзину через кнопку в шапке сайта
    # (обычно это иконка корзины в верхней части страницы)
    page.go_to_basket_page()

    # Создаем объект страницы корзины для текущего URL
    basket_page = BasketPage(browser, browser.current_url)

    # Проверяем, что корзина пуста (отсутствуют товары)
    # Это включает проверку отсутствия элементов товаров в DOM
    basket_page.should_be_basket_empty()

    # Проверяем наличие информационного сообщения о пустой корзине
    # Сообщение должно пояснять пользователю, что корзина пуста
    basket_page.should_display_empty_basket_message()
