"""
PAGE OBJECT МОДЕЛЬ СТРАНИЦЫ КОРЗИНЫ ПОКУПОК

Данный модуль содержит класс BasketPage для работы со страницей корзины интернет-магазина.
Класс наследует от BasePage и добавляет специфичные методы для проверки состояния корзины
и отображения соответствующих сообщений.

ОСНОВНЫЕ ФУНКЦИОНАЛЬНЫЕ ВОЗМОЖНОСТИ:
- Проверка пустого состояния корзины покупок
- Валидация отображения сообщения о пустой корзине
- Проверка отсутствия товаров в корзине
- Анализ текстовых сообщений о состоянии корзины
"""


# Импорты Page Object моделей и локаторов
from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):
    """
    Класс для работы со страницей корзины покупок интернет-магазина.

    Наследует все методы от BasePage и добавляет специфичные методы для:
    - Проверки пустого состояния корзины
    - Валидации сообщений о пустой корзине
    - Анализа наличия товаров в корзине

    Атрибуты:
        browser: Экземпляр веб-браузера для управления страницей
        url: URL-адрес страницы корзины
    """

    def should_be_basket_empty(self) -> None:
        """
        Проверяет, что корзина покупок пуста.

        Убеждается, что в корзине отсутствуют товары, проверяя отсутствие
        элементов, представляющих товары в корзине.

        Пример использования:
            basket_page = BasketPage(browser, "https://shop.com/basket")
            basket_page.should_be_basket_empty()  # Пройдет если корзина пуста

        Raises:
            AssertionError: Если в корзине найдены товары (корзина не пуста)
        """
        # Проверяем отсутствие элементов товаров в корзине
        assert self.is_not_element_present(*BasketPageLocators.ITEMS_IN_BASKET), \
            "Basket is not empty - items found when expected empty basket"

    def should_display_empty_basket_message(self) -> None:
        """
        Проверяет отображение сообщения о пустой корзине.

        Убеждается, что на странице присутствует и отображается информационное
        сообщение о том, что корзина пуста. Проверяет как наличие элемента,
        так и наличие текстового содержимого.

        Проверяет:
        - Наличие элемента сообщения на странице
        - Наличие текстового содержимого в сообщении
        - Видимость сообщения для пользователя

        Пример использования:
            basket_page = BasketPage(browser, "https://shop.com/basket")
            basket_page.should_display_empty_basket_message()  # Пройдет если сообщение отображается

        Raises:
            AssertionError: Если сообщение отсутствует, не видимо или не содержит текст
        """
        # Проверяем наличие элемента сообщения на странице
        message_element_present = self.is_element_present(*BasketPageLocators.BASKET_BOX)

        # Получаем текст сообщения, если элемент присутствует
        message_text = self.browser.find_element(*BasketPageLocators.BASKET_BOX).text

        # Проверяем, что сообщение содержит текст (длина больше 1 символа)
        message_has_text = len(message_text) > 1

        # Комплексная проверка: элемент присутствует И содержит текст
        empty_basket_message_displayed = all([message_element_present, message_has_text])

        # Проверяем, что сообщение о пустой корзине отображается корректно
        assert empty_basket_message_displayed, \
            "No empty basket message displayed or message is empty. Expected informative 'empty basket' message"
