"""
PAGE OBJECT МОДЕЛЬ СТРАНИЦЫ ТОВАРА

Данный модуль содержит класс ProductPage для работы со страницей товара в интернет-магазине.
Это набор инструментов для автоматического тестирования процесса добавления товара в корзину.

ОСНОВНЫЕ ФУНКЦИОНАЛЬНЫЕ ВОЗМОЖНОСТИ:
- Добавление товара в корзину (нажатие кнопки)
- Проверка сообщений об успешном добавлении
- Сравнение данных товара (название, цена) с тем, что показывается в сообщениях
- Работа с всплывающими сообщениями на странице
"""

from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, List, Optional

# Импорты Page Object моделей и локаторов
from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    """
    Класс для работы со страницей товара.

    Содержит методы для взаимодействия с элементами страницы товара и проверки
    правильности работы функционала добавления в корзину.

    Наследует все возможности от BasePage и добавляет специальные методы
    для работы именно со страницей товара.
    """

    def __init__(self, browser, url: str) -> None:
        """
        Инициализация страницы товара.

        Args:
            browser: Веб-браузер, которым управляем для тестирования
            url: Адрес страницы товара, которую будем тестировать
        """
        # Вызываем конструктор родительского класса (BasePage)
        super().__init__(browser, url)
        # Словарь для хранения данных о товаре (название, цена)
        self.product_data: dict = {}

    def open(self) -> None:
        """
        Открывает страницу товара и обновляет данные о товаре.

        При открытии страницы автоматически считывает и сохраняет информацию
        о названии и цене товара для последующих проверок.
        """
        # Открываем страницу (метод из родительского класса)
        super().open()
        # Обновляем информацию о товаре (название и цена)
        self._update_product_data()

    # === ОСНОВНЫЕ МЕТОДЫ ДЛЯ ВЗАИМОДЕЙСТВИЯ СО СТРАНИЦЕЙ ===

    def click_add_to_basket(self) -> None:
        """
        Нажимает кнопку 'Добавить в корзину'.

        Находит кнопку добавления в корзину на странице и имитирует клик пользователя.
        После этого действия товар должен добавиться в корзину.
        """
        # Ищем кнопку "Добавить в корзину" на странице
        add_button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BTN)
        # Нажимаем на кнопку
        add_button.click()

    def should_be_add_to_basket_button(self) -> None:
        """
        Проверяет наличие кнопки 'Добавить в корзину' на странице.

        Убеждается, что элемент кнопки присутствует на странице и доступен для взаимодействия.

        Raises:
            AssertionError: Если кнопка не найдена на странице
        """
        # Проверяем, что кнопка присутствует на странице
        assert self.is_element_present(*ProductPageLocators.ADD_TO_BASKET_BTN), \
            "Add to basket button is not presented"

    def should_be_success_message(self) -> None:
        """
        Проверяет наличие сообщения об успешном добавлении товара в корзину.

        После добавления товара должно появиться сообщение, содержащее название
        добавленного товара. Метод ожидает появления такого сообщения.

        Raises:
            AssertionError: Если сообщение не найдено или не содержит название товара
        """
        # Получаем название товара из сохраненных данных
        product_name = self.product_data['name']

        # Ожидаем появление хотя бы одного элемента сообщения
        # (сообщения могут появляться с задержкой после клика)
        try:
            self.wait_for_element(*ProductPageLocators.MESSAGE_ELEMENT)
        except TimeoutException:
            # Если сообщений вообще нет - это ошибка!
            assert False, (
                f"No success messages found at all. "
                f"Expected message containing: '{product_name}'"
            )

        # Ищем сообщение, которое содержит название нашего товара
        message_element, all_messages = self._find_message_containing_text(
            ProductPageLocators.MESSAGE_ELEMENT,
            product_name,
            expect_multiple=False
        )

        # Проверяем, что нашли нужное сообщение
        assert message_element is not None, (
            f"Success message containing product name '{product_name}' was not found. "
            f"All messages: {[elem.text for elem in self.browser.find_elements(*ProductPageLocators.MESSAGE_ELEMENT)]}"
        )

    def should_show_basket_total_message(self) -> None:
        """
        Проверяет отображение сообщения с общей стоимостью корзины.

        После добавления товара должно появиться сообщение с обновленной
        общей стоимостью корзины, содержащее цену добавленного товара.

        Raises:
            AssertionError: Если сообщение о стоимости корзины не найдено
        """
        # Получаем цену товара
        product_price = self._get_product_price()

        # Ищем сообщение, содержащее цену товара
        message_element, all_messages = self._find_message_containing_text(
            ProductPageLocators.MESSAGE_ELEMENT,
            product_price,
            expect_multiple=False
        )

        # Проверяем, что нашли сообщение с ценой
        assert message_element is not None, (
            f"Basket total message containing '{product_price}' was not found."
        )

    def should_have_correct_product_name_in_message_box(self) -> None:
        """
        Проверяет корректность названия товара в сообщении о добавлении.

        Сравнивает название товара на странице с названием, указанным в сообщении
        об успешном добавлении. Они должны точно совпадать.

        Raises:
            AssertionError: Если названия не совпадают или не найдены
        """
        product_name = self.product_data['name']
        found_text = self._find_matching_text_in_messages(product_name)

        # Проверяем, что название найдено в сообщениях
        assert found_text is not None, f"Product name '{product_name}' not found in messages"

        # Проверяем, что название точно совпадает
        assert product_name == found_text, \
            f"Product name doesn't match. Expected: '{product_name}', Got: '{found_text}'"

    def should_have_correct_price_in_message_box(self) -> None:
        """
        Проверяет корректность цены товара в сообщении о стоимости корзины.

        Сравнивает цену товара на странице с ценой, указанной в сообщении
        об общей стоимости корзины. Они должны точно совпадать.

        Raises:
            AssertionError: Если цены не совпадают или не найдены
        """
        product_price = self.product_data['price']
        found_text = self._find_matching_text_in_messages(product_price)

        # Проверяем, что цена найдена в сообщениях
        assert found_text is not None, f"Price '{product_price}' not found in messages"

        # Проверяем, что цена точно совпадает
        assert product_price == found_text, \
            f"Price doesn't match. Expected: '{product_price}', Got: '{found_text}'"

    def should_not_be_success_message(self) -> None:
        """
        Проверяет отсутствие сообщения об успехе до добавления товара.

        Убеждается, что сообщение об успешном добавлении появляется ТОЛЬКО
        после нажатия кнопки "Добавить в корзину".

        Raises:
            AssertionError: Если сообщение найдено до добавления товара
        """
        product_name = self._get_product_name()
        # Создаем локатор для сообщения с конкретным названием товара
        locator = ProductPageLocators.message_product_is_added_successfully(product_name)

        # Проверяем, что сообщения НЕТ на странице
        assert self.is_not_element_present(*locator), (
            f"Success message for product '{product_name}' was found when it should not be present. "
            "This message should only appear after adding product to basket."
        )

    def success_message_should_disappear(self) -> None:
        """
        Проверяет исчезновение сообщения об успехе через некоторое время.

        Проверяет, что сообщение об успешном добавлении исчезает через
        определенное время, как это обычно происходит в интерфейсах.

        Raises:
            AssertionError: Если сообщение не исчезает в течение заданного времени
        """
        product_name = self._get_product_name()
        # Создаем локатор для сообщения с конкретным названием товара
        locator = ProductPageLocators.message_product_is_added_successfully(product_name)

        # Проверяем, что сообщение исчезает
        assert self.is_disappeared(*locator), (
            f"Success message for product '{product_name}' did not disappear within the expected time. "
            "The message should vanish after being displayed."
        )

    # === ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ДЛЯ РАБОТЫ С ДАННЫМИ ===

    def _update_product_data(self) -> None:
        """Обновляет внутренний словарь с данными о товаре при открытии страницы."""
        self.product_data = {
            'name': self._get_product_name(),   # Сохраняем название товара
            'price': self._get_product_price()  # Сохраняем цену товара
        }

    def _get_product_name(self) -> str:
        """
        Извлекает название товара со страницы.

        Returns:
            str: Текст названия товара
        """
        # Ожидаем появление элемента с названием товара
        element = self.wait_for_element(*ProductPageLocators.PRODUCT_NAME)
        # Возвращаем текст названия
        return element.text

    def _get_product_price(self) -> str:
        """
        Извлекает цену товара со страницы.

        Returns:
            str: Текст цены товара
        """
        # Ожидаем появление элемента с ценой товара
        element = self.wait_for_element(*ProductPageLocators.PRODUCT_PRICE)
        # Возвращаем текст цены
        return element.text

    def _get_strong_texts_from_message_box(self) -> List[str]:
        """
        Извлекает все тексты из элементов <strong> в сообщениях.

        В HTML-разметке важные части сообщений часто выделяются тегом <strong>.

        Returns:
            List[str]: Список текстов из strong элементов
        """
        # Ищем все элементы с тегом <strong> в сообщениях
        strong_elements = self.browser.find_elements(*ProductPageLocators.MESSAGE_ELEMENT_STRONG)
        # Собираем тексты из этих элементов
        return [element.text for element in strong_elements]

    def _find_matching_text_in_messages(self, target_text: str) -> Optional[str]:
        """
        Ищет совпадение текста среди выделенных частей сообщений.

        Args:
            target_text: Текст для поиска совпадений

        Returns:
            Optional[str]: Найденный текст или None если не найден
        """
        # Получаем все выделенные тексты из сообщений
        strong_texts = self._get_strong_texts_from_message_box()

        # Ищем совпадения различными способами
        for text in strong_texts:
            # Проверяем точное совпадение или частичное вхождение
            if text == target_text or target_text in text or text in target_text:
                return text
        return None

    def _find_message_containing_text(self,
                                    element_locator: Tuple[str, str],
                                    search_text: str,
                                    min_length_delta: int = 1,
                                    expect_multiple: bool = False) -> Tuple[Optional[WebElement], List[str]]:
        """
        Универсальный метод для поиска сообщений, содержащих указанный текст.

        Args:
            element_locator: Локатор для поиска элементов сообщений
            search_text: Текст для поиска в сообщениях
            min_length_delta: Минимальная разница длины для фильтрации коротких совпадений
            expect_multiple: Ожидать ли множественные совпадения

        Returns:
            Tuple[Optional[WebElement], List[str]]: Найденный элемент и список всех сообщений
        """
        # Ищем все элементы сообщений на странице
        all_elements = self.browser.find_elements(*element_locator)
        found_elements = []
        found_messages = []

        # Проверяем каждое сообщение
        for element in all_elements:
            full_text = element.text
            # Проверяем содержит ли сообщение нужный текст и не слишком ли оно короткое
            if (search_text in full_text and
                len(full_text) >= len(search_text) + min_length_delta):
                found_elements.append(element)
                found_messages.append(full_text)

        # Обрабатываем результаты поиска
        if not found_elements:
            return None, []
        elif len(found_elements) == 1:
            return found_elements[0], found_messages
        else:
            if expect_multiple:
                return found_elements[0], found_messages
            else:
                # Логируем предупреждение о множественных совпадениях
                print(f"\n[WARNING] Found {len(found_elements)} messages containing '{search_text}': {found_messages}")
                return found_elements[0], found_messages
