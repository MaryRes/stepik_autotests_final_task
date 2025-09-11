"""
МОДУЛЬ ТЕСТИРОВАНИЯ КОРЗИНЫ ПОКУПОК

Данный модуль содержит комплексные тесты функциональности корзины:
- Для гостевых пользователей (неавторизованных)
- Для зарегистрированных пользователей
- На различных типах страниц (обычные товары, промо-акции)

ОСНОВНЫЕ СЦЕНАРИИ ТЕСТИРОВАНИЯ:
1. Сообщения об успешном добавлении товаров
2. Корректность названий и цен в сообщениях
3. Отсутствие сообщений до добавления товаров
4. Поведение корзины из разных состояний пользователя

СПЕЦИАЛЬНЫЕ МАРКЕРЫ:
@need_review - основные тесты для проверки ревьюером
@new - новые тесты в разработке
@xfail - тесты с ожидаемыми падениями (известные баги)
"""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Union

# Импорты Page Object моделей
from .pages.product_page import ProductPage
from .pages.basket_page import BasketPage
from .pages.login_page import LoginPage
from .urls import (TEST_PAGE_URL, PRODUCT_PAGE_URL, get_promo_urls, LOGIN_PAGE_URL)

# Определяем проблемное промо-предложение с известным багом
# Тесты для этого предложения помечаются как ожидаемые падения (xfail)
BUGGED_OFFER: str = "offer7"

# Получаем все промо-ссылки для тестирования
all_urls: List[str] = get_promo_urls()

# Создаем тестовые данные с учетом известных проблем
# Для проблемных URL добавляем маркер xfail
test_data: List[Union[str, pytest.param]] = []
for url in all_urls:
    if BUGGED_OFFER in url:
        # Известный баг в offer7 - тест должен падать, но это ожидаемо
        test_data.append(pytest.param(url, marks=pytest.mark.xfail(reason="Известный баг в offer7")))
    else:
        test_data.append(url)


@pytest.mark.new
@pytest.mark.parametrize('url', [PRODUCT_PAGE_URL])
class TestUserAddToBasketFromProductPage:
    """
    Тесты добавления товаров в корзину для ЗАРЕГИСТРИРОВАННЫХ пользователей.

    Данный класс включает автоматическую регистрацию пользователя перед каждым тестом.
    Содержит как позитивные, так и негативные сценарии тестирования.
    """

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser: WebDriver) -> None:
        """
        Автоматическая настройка перед каждым тестовым методом:
        1. Открывает страницу регистрации
        2. Регистрирует нового пользователя с автоматической генерацией учетных данных
        3. Проверяет успешную авторизацию

        Args:
            browser: Экземпляр Selenium WebDriver
        """
        # Открываем страницу регистрации
        login_page = LoginPage(browser, LOGIN_PAGE_URL)
        login_page.open()

        # Регистрируем нового пользователя (email генерируется автоматически с timestamp)
        login_page.register_new_user()

        # Проверяем, что пользователь успешно авторизован
        # (иконка пользователя должна отображаться в шапке сайта)
        login_page.should_be_authorized_user()

    def test_user_cant_see_success_message(self, browser: WebDriver, url: str) -> None:
        """
        Проверяет, что сообщение об успехе НЕ отображается ДО добавления товара в корзину.

        Это важно для чистоты пользовательского интерфейса - сообщения должны появляться
        только после соответствующих действий пользователя.

        Args:
            browser: Экземпляр Selenium WebDriver
            url: URL страницы товара для тестирования
        """
        # Открываем страницу товара
        page = ProductPage(browser, url)
        page.open()

        # Проверяем, что сообщение об успехе отсутствует до добавления товара
        page.should_not_be_success_message()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser: WebDriver, url: str) -> None:
        """
        ОСНОВНОЙ ТЕСТ: Проверяет полный процесс добавления товара для зарегистрированного пользователя.

        Включает:
        - Проверку доступности кнопки добавления в корзину
        - Добавление товара в корзину
        - Решение капчи (для промо-страниц)
        - Все проверки сообщений об успехе

        Данный тест входит в минимальный набор для ревью.

        Args:
            browser: Экземпляр Selenium WebDriver
            url: URL страницы товара для тестирования
        """
        page = ProductPage(browser, url)
        page.open()

        # Проверяем, что кнопка "Добавить в корзину" доступна пользователю
        page.should_be_add_to_basket_button()

        # Нажимаем кнопку "Добавить в корзину"
        page.click_add_to_basket()

        # Решаем математическую капчу (требуется для некоторых промо-акций)
        page.solve_quiz_and_get_code()

        # --- ПРОВЕРКИ ПОСЛЕ ДОБАВЛЕНИЯ ---

        # Должно появиться сообщение об успешном добавлении товара
        page.should_be_success_message()

        # Название товара в сообщении должно совпадать с добавленным товаром
        page.should_have_correct_product_name_in_message_box()

        # Должно отображаться сообщение с общей стоимостью корзины
        page.should_show_basket_total_message()

        # Общая стоимость корзины должна совпадать с ценой товара
        page.should_have_correct_price_in_message_box()


@pytest.mark.need_review
@pytest.mark.parametrize('url', test_data)
def test_guest_can_add_product_to_basket(browser: WebDriver, url: str) -> None:
    """
    ОСНОВНОЙ ТЕСТ: Проверяет добавление товара в корзину ГОСТЕВЫМ пользователем.

    Тестирует все промо-предложения, включая проблемные (с ожидаемым падением).
    Автоматически обрабатывает математические капчи на промо-страницах.

    Данный тест входит в минимальный набор для ревью.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()

    # Проверяем наличие кнопки добавления в корзину
    page.should_be_add_to_basket_button()

    # Добавляем товар в корзину
    page.click_add_to_basket()

    # Решаем математическую капчу для промо-страниц
    page.solve_quiz_and_get_code()

    # --- ПРОВЕРКИ ПОСЛЕ ДОБАВЛЕНИЯ ---

    # Сообщение о успешном добавлении товара
    page.should_be_success_message()

    # Корректность названия товара в сообщении
    page.should_have_correct_product_name_in_message_box()

    # Сообщение с общей стоимостью корзины
    page.should_show_basket_total_message()

    # Корректность цены в сообщении о стоимости корзины
    page.should_have_correct_price_in_message_box()


@pytest.mark.xfail(reason="Сообщение об успехе ДОЛЖНО появляться после добавления товара, этот тест проверяет обратное поведение")
@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_should_be_and_not_to_be_success_message(browser: WebDriver, url: str) -> None:
    """
    Комплексный тест проверки появления и исчезновения сообщений об успехе.

    Проверяет, что сообщение отсутствует до добавления, появляется после добавления
    и затем исчезает через некоторое время.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    page = ProductPage(browser, url)
    page.open()

    # Проверяем отсутствие сообщения до добавления товара
    page.should_not_be_success_message()

    # Добавляем товар в корзину
    page.click_add_to_basket()

    # Решаем математическую капчу
    page.solve_quiz_and_get_code()

    # Проверяем появление сообщения после добавления
    page.should_be_success_message()

    # Проверяем, что сообщение исчезает через некоторое время
    page.success_message_should_disappear()


@pytest.mark.xfail(reason="Сообщение об успехе ДОЛЖНО появляться после добавления товара, этот тест проверяет обратное поведение")
@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser: WebDriver, url: str) -> None:
    """
    НЕГАТИВНЫЙ ТЕСТ: Проверяет, что сообщение об успехе не отображается сразу после добавления.

    Этот тест ДОЛЖЕН падать, так как сообщение должно появляться после добавления товара.
    Проверяет некорректное поведение, поэтому помечен как xfail.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()

    # Добавляем товар в корзину
    page.click_add_to_basket()

    # Проверяем отсутствие сообщения об успехе (это неправильное поведение)
    page.should_not_be_success_message()


@pytest.mark.need_review
@pytest.mark.parametrize('url', [PRODUCT_PAGE_URL])
def test_guest_can_go_to_login_page_from_product_page(browser: WebDriver, url: str) -> None:
    """
    ОСНОВНОЙ ТЕСТ: Проверяет переход на страницу логина со страницы товара.

    Проверяет доступность и работоспособность ссылки на страницу авторизации.

    Данный тест входит в минимальный набор для ревью.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    page = ProductPage(browser, url)
    page.open()

    # Переходим на страницу логина
    page.go_to_login_page()


@pytest.mark.parametrize('url', [TEST_PAGE_URL, PRODUCT_PAGE_URL])
def test_guest_should_see_login_link_on_product_page(browser: WebDriver, url: str) -> None:
    """
    Проверяет наличие ссылки на страницу логина на странице товара.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    page = ProductPage(browser, url)
    page.open()

    # Проверяем наличие ссылки на страницу логина
    page.should_be_login_link()


@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_guest_cant_see_success_message(browser: WebDriver, url: str) -> None:
    """
    Проверяет, что сообщение об успехе не отображается до добавления товара.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()

    # Проверяем отсутствие сообщения об успехе до добавления товара
    page.should_not_be_success_message()


@pytest.mark.xfail(reason="Сообщение об успехе НЕ ДОЛЖНО исчезать сразу после добавления товара")
@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_message_disappeared_after_adding_product_to_basket(browser: WebDriver, url: str) -> None:
    """
    НЕГАТИВНЫЙ ТЕСТ: Проверяет немедленное исчезновение сообщения после добавления.

    Этот тест ДОЛЖЕН падать, так как сообщение не должно исчезать сразу.
    Проверяет некорректное поведение, поэтому помечен как xfail.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()

    # Добавляем товар в корзину
    page.click_add_to_basket()

    # Проверяем немедленное исчезновение сообщения (это неправильное поведение)
    page.success_message_should_disappear()


@pytest.mark.need_review
@pytest.mark.parametrize('url', [PRODUCT_PAGE_URL])
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser: WebDriver, url: str) -> None:
    """
    ОСНОВНОЙ ТЕСТ: Проверяет пустую корзину при переходе со страницы товара.

    Проверяет, что в корзине нет товаров и отображается соответствующее сообщение.

    Данный тест входит в минимальный набор для ревью.

    Args:
        browser: Экземпляр Selenium WebDriver
        url: URL страницы товара для тестирования
    """
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()

    # Переходим в корзину через кнопку в шапке сайта
    page.go_to_basket_page()

    # Создаем объект страницы корзины
    basket_page = BasketPage(browser, browser.current_url)

    # Проверяем, что корзина пуста
    basket_page.should_be_basket_empty()

    # Проверяем наличие сообщения о пустой корзине
    basket_page.should_display_empty_basket_message()
