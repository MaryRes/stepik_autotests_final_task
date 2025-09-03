from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):

    def __init__(self, browser, url):
        super().__init__(browser, url)
        self.product_data = {}

    def open(self):
        """Открывает страницу и обновляет данные товара"""
        super().open()
        self._update_product_data()

    # === ПУБЛИЧНЫЕ МЕТОДЫ (ИНТЕРФЕЙС ДЛЯ ТЕСТОВ) ===

    def click_add_to_basket(self):
        """Нажимает кнопку 'Добавить в корзину'"""
        add_button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BTN)
        add_button.click()

    def should_be_add_to_basket_button(self):
        """Проверяет, что кнопка добавления в корзину присутствует"""
        assert self.is_element_present(*ProductPageLocators.ADD_TO_BASKET_BTN), \
            "Add to basket button is not presented"

    def should_be_success_message(self):
        """Проверяет сообщение об успешном добавлении в корзину"""
        product_name = self._get_product_name()
        message_element, all_messages = self._find_message_containing_text(
            ProductPageLocators.MESSAGE_ELEMENT,
            product_name,
            expect_multiple=False
        )
        assert message_element is not None, (
            f"Success message containing product name '{product_name}' was not found. "
            f"All messages: {[elem.text for elem in self.browser.find_elements(*ProductPageLocators.MESSAGE_ELEMENT)]}"
        )

    def should_show_basket_total_message(self):
        """Проверяет сообщение со стоимостью корзины"""
        product_price = self._get_product_price()
        message_element, all_messages = self._find_message_containing_text(
            ProductPageLocators.MESSAGE_ELEMENT,
            product_price,
            expect_multiple=False
        )
        assert message_element is not None, (
            f"Basket total message containing '{product_price}' was not found."
        )

    def should_have_correct_product_name_in_message_box(self):
        """Проверяет совпадение названия товара в сообщении"""
        product_name = self.product_data['name']
        found_text = self._find_matching_text_in_messages(product_name)
        assert found_text is not None, f"Product name '{product_name}' not found in messages"
        assert product_name == found_text, \
            f"Product name doesn't match. Expected: '{product_name}', Got: '{found_text}'"

    def should_have_correct_price_in_message_box(self):
        """Проверяет совпадение цены в сообщении"""
        product_price = self.product_data['price']
        found_text = self._find_matching_text_in_messages(product_price)
        assert found_text is not None, f"Price '{product_price}' not found in messages"
        assert product_price == found_text, \
            f"Price doesn't match. Expected: '{product_price}', Got: '{found_text}'"

    def should_not_be_success_message(self):
        """
        Проверяет отсутствие сообщения об успешном добавлении в корзину.
        """
        product_name = self._get_product_name()
        locator = ProductPageLocators.message_product_is_added_successfully(product_name)

        assert self.is_not_element_present(*locator), (
            f"Success message for product '{product_name}' was found when it should not be present. "
            "This message should only appear after adding product to basket."
        )

    def success_message_should_disappear(self):
        """
        Проверяет исчезновение сообщения об успешном добавлении в корзину.
        """
        product_name = self._get_product_name()
        locator = ProductPageLocators.message_product_is_added_successfully(product_name)

        assert self.is_disappeared(*locator), (
            f"Success message for product '{product_name}' did not disappear within the expected time. "
            "The message should vanish after being displayed."
        )

    # === ПРИВАТНЫЕ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ===

    def _update_product_data(self):
        """Обновляет данные товара при открытии страницы"""
        self.product_data = {
            'name': self._get_product_name(),
            'price': self._get_product_price()
        }

    def _get_product_name(self):
        """Возвращает название товара на странице"""
        element = self.wait_for_element(*ProductPageLocators.PRODUCT_NAME)
        return element.text

    def _get_product_price(self):
        """Возвращает цену товара на странице"""
        element = self.wait_for_element(*ProductPageLocators.PRODUCT_PRICE)
        return element.text

    def _get_strong_texts_from_message_box(self):
        """Возвращает список текстов из strong элементов в сообщениях"""
        strong_elements = self.browser.find_elements(*ProductPageLocators.MESSAGE_ELEMENT_STRONG)
        return [element.text for element in strong_elements]

    def _find_matching_text_in_messages(self, target_text):
        """Ищет совпадение текста среди strong элементов"""
        strong_texts = self._get_strong_texts_from_message_box()
        for text in strong_texts:
            if text == target_text or target_text in text or text in target_text:
                return text
        return None

    def _find_message_containing_text(self, element_locator, search_text, min_length_delta=1, expect_multiple=False):
        """Универсальная функция для поиска сообщений"""
        all_elements = self.browser.find_elements(*element_locator)
        found_elements = []
        found_messages = []

        for element in all_elements:
            full_text = element.text
            if search_text in full_text and len(full_text) >= len(search_text) + min_length_delta:
                found_elements.append(element)
                found_messages.append(full_text)

        if not found_elements:
            return None, []
        elif len(found_elements) == 1:
            return found_elements[0], found_messages
        else:
            if expect_multiple:
                return found_elements[0], found_messages
            else:
                print(f"\n[WARNING] Found {len(found_elements)} messages containing '{search_text}': {found_messages}")
                return found_elements[0], found_messages
