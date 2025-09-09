"""
МОДУЛЬ ЛОКАТОРОВ ДЛЯ PAGE OBJECT МОДЕЛЕЙ

Данный модуль содержит все локаторы (селекторы) для элементов веб-страниц,
используемые в автоматизированном тестировании. Локаторы организованы по классам,
соответствующим различным страницам приложения.

ОСНОВНЫЕ КАТЕГОРИИ ЛОКАТОРОВ:
- Базовые локаторы для общих элементов всех страниц
- Локаторы для страницы корзины покупок
- Локаторы для главной страницы
- Локаторы для страницы логина и регистрации
- Локаторы для страницы товара с динамическими селекторами
"""

from selenium.webdriver.common.by import By


class BasePageLocators:
    """
    Локаторы для общих элементов, присутствующих на всех страницах сайта.

    Содержит селекторы для элементов навигации, пользовательского интерфейса
    и общих компонентов, которые доступны с любой страницы.
    """

    # Ссылка для входа в систему
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")

    # Ссылка для регистрации нового пользователя
    REGISTRATION_LINK = (By.CSS_SELECTOR, '#registration_link')

    # Невалидная ссылка логина (для негативного тестирования)
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")

    # Иконка пользователя (отображается после авторизации)
    USER_ICON = (By.CSS_SELECTOR, ".icon-user")

    # Ссылка на корзину в шапке сайта
    BASKET_LINK_IN_HEADER = (By.CSS_SELECTOR, 'div[class*="basket-mini"] > span.btn-group > a[href*="basket"]')


class BasketPageLocators:
    """
    Локаторы для страницы корзины покупок.

    Содержит селекторы для элементов, специфичных для страницы корзины:
    - Контейнер содержимого корзины
    - Элементы товаров в корзине
    - Сообщения о состоянии корзины
    """

    # Основной контейнер содержимого корзины
    BASKET_BOX = (By.CSS_SELECTOR, 'div[id="content_inner"]')

    # Элементы товаров, присутствующих в корзине
    ITEMS_IN_BASKET = (By.CSS_SELECTOR, 'div[id="content_inner"] form')


class MainPageLocators:
    """
    Локаторы для главной страницы сайта.

    Содержит селекторы для элементов, специфичных для главной страницы.
    Наследует общие локаторы от BasePageLocators.
    """

    # Ссылка на корзину в шапке сайта (дублируется для специфичности главной страницы)
    BASKET_LINK_IN_HEADER = (By.CSS_SELECTOR, 'div[class*="basket-mini"] > span.btn-group > a[href*="basket"]')


class LoginPageLocators:
    """
    Локаторы для страницы логина и регистрации.

    Содержит селекторы для всех элементов форм авторизации и регистрации:
    - Ссылки на формы
    - Поля ввода данных
    - Кнопки отправки форм
    """

    # Ссылка на страницу логина
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")

    # Форма для входа в систему
    LOGIN_FORM = (By.CSS_SELECTOR, 'form[id*="login"]')

    # Форма для регистрации нового пользователя
    REGISTRATION_FORM = (By.CSS_SELECTOR, 'form[id*="register"]')

    # Поле ввода email для регистрации
    REGISTRATION_EMAIL = (By.CSS_SELECTOR, "[id='register_form'] input[id*='registration-email']")

    # Первое поле ввода пароля для регистрации
    REGISTRATION_PASSWORD1 = (By.CSS_SELECTOR, "[id='register_form'] input[id*='password1']")

    # Второе поле ввода пароля (подтверждение) для регистрации
    REGISTRATION_PASSWORD2 = (By.CSS_SELECTOR, "[id='register_form'] input[id*='password2']")

    # Кнопка отправки формы регистрации
    REGISTRATION_BUTTON = (By.CSS_SELECTOR, "[id='register_form'] button[type='submit']")


class ProductPageLocators:
    """
    Локаторы для страницы товара.

    Содержит селекторы для элементов страницы товара, включая:
    - Кнопки добавления в корзину
    - Информацию о товаре (название, цена)
    - Сообщения о действиях с корзиной
    - Элементы навигации и отображения цен
    """

    # Кнопка добавления товара в корзину
    ADD_TO_BASKET_BTN = (By.CSS_SELECTOR, '[class*="btn-add-to-basket"]')

    # Название товара на странице (до и после добавления в корзину)
    PRODUCT_NAME = (By.CSS_SELECTOR, '[class*=product_main] h1')

    # Цена товара на странице
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[class*="product_main"] [class*="price_color"]')

    # Контейнер сообщений о действиях с корзиной
    BASKET_MESSAGE_BOX = (By.CSS_SELECTOR, '[id="messages"]')

    # Элементы навигационной цепочки (хлебные крошки)
    BREADCRUMB_BOX = (By.XPATH, '//ul[@class="breadcrumb"]//li[last()]')

    # Элементы с выделенным текстом в сообщениях (обычно содержат названия и цены)
    MESSAGE_ELEMENT_STRONG = (By.CSS_SELECTOR, '[class*="alertinner"] strong')

    # Элементы сообщений о действиях с корзиной
    MESSAGE_ELEMENT = (By.CSS_SELECTOR, '[class*="alertinner"]')

    # Строка с ценой товара включая налоги
    PRODUCT_PRICE_INCLUDED_TAX_ROW = (By.XPATH, "//th[text()='Price (incl. tax)']/..//td")

    # Общая стоимость корзины в навигационной панели
    BASKET_TOTAL_IN_NAVBAR = (By.CSS_SELECTOR, '[class*="basket-mini pull-right"]')

    # Выделенная общая стоимость корзины в навигационной панели
    BASKET_TOTAL_IN_NAVBAR_STRONG = (By.CSS_SELECTOR, '[class*="basket-mini pull-right"] strong')

    # Текстовая часть общей стоимости корзины в навигационной панели
    BASKET_TOTAL_IN_NAVBAR_ONLY_TEXT = (By.CSS_SELECTOR, '[class*="basket-mini pull-right"] span[class*="total"]')

    # Общая стоимость корзины в сообщениях
    BASKET_TOTAL_IN_MESSAGE_BOX = (By.XPATH, "//div[@id='messages']//p[contains(., 'basket total')]//strong")

    # Список локаторов, содержащих название продукта
    list_of_product_titles = [PRODUCT_NAME, MESSAGE_ELEMENT_STRONG, BREADCRUMB_BOX]

    # Список локаторов, содержащих цену товара
    list_of_item_prices = [PRODUCT_PRICE, PRODUCT_PRICE_INCLUDED_TAX_ROW]

    # Список локаторов, содержащих общую стоимость корзины
    list_of_basket_total = [BASKET_TOTAL_IN_NAVBAR, BASKET_TOTAL_IN_MESSAGE_BOX]

    @staticmethod
    def message_product_is_added_successfully(product_name: str) -> tuple:
        """
        Динамический локатор для сообщения об успешном добавлении товара.

        Генерирует XPath выражение для поиска сообщения, содержащего указанное
        название товара. Используется для проверки корректности сообщений.

        Args:
            product_name: Название товара для поиска в сообщении

        Returns:
            tuple: Локатор в формате (By.XPATH, xpath_expression)
        """
        return (By.XPATH,
                f'//div[contains(@class, "alertinner") and contains(., "{product_name}")]')