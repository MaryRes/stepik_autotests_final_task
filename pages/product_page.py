from .base_page import BasePage
from .locators import ProductPageLocators
from ..decorators import Decorators
#from locators import ProductPageLocators


@Decorators.print_function_name
@Decorators.screenshot_on_error
class ProductPage(BasePage):
    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def __init__(self, browser, url: str = None):
        """
        Инициализация страницы продукта.
        :return: None
        """
        super().__init__(browser, url)
        self.product_name = None
        self.product_price = None

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def guest_can_add_product_to_basket(self, added_to_basket_message: str):
        """
        Проверяет возможность добавления товара в корзину.
        :return: None
        """
        self.set_product_name()
        self.set_product_price()

        self.should_be_add_to_basket_button()
        self.click_add_to_basket()

        try:
            self.solve_quiz_and_get_code()
        except Exception:
            pass
        self.should_be_added_to_basket_message(added_to_basket_message)
        self.should_match_product_name_in_basket()

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def set_product_name(self):
        """
        Сохраняет название продукта на странице.
        :return: None
        """
        self.product_name = self.get_text_from_element(ProductPageLocators.PRODUCT_NAME)

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def set_product_price(self):
        """
        Сохраняет цену продукта на странице.
        :return: None
        """
        self.product_price = self.get_text_from_element(ProductPageLocators.PRODUCT_PRICE)

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def click_add_to_basket(self):
        """
        Нажимает кнопку "Добавить в корзину".
        :return: None
        """
        add_to_basket_button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BTN)
        add_to_basket_button.click()

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def should_be_add_to_basket_button(self):
        """
        Проверяет наличие кнопки "Добавить в корзину".
        :return: None
        """
        assert self.is_element_present(*ProductPageLocators.ADD_TO_BASKET_BTN), "Add to basket button is not present on the page"

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def should_be_added_to_basket_message(self, expected_message: str):
        """
        Проверяет, что есть сообщение о добавлении товара в корзину.
        :param expected_message: ожидаемое сообщение
        :return: None
        """
        all_messages_after_click_add_to_basket = (
            self.get_texts_from_elements(ProductPageLocators.BASKET_MESSAGE_BOX))
        added_to_basket_message_present = False
        for message in all_messages_after_click_add_to_basket:
            if self.product_name in message and expected_message in message:
                added_to_basket_message_present = True
                break

        assert added_to_basket_message_present, f"Expected product name '{self.product_name}' and message '{expected_message}' not found in messagebox: '{all_messages_after_click_add_to_basket}'"

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def should_match_product_name_in_basket(self):
        """
        Проверяет, что название продукта в корзине совпадает с названием на странице.
        :return: None
        """

        product_name_is_same = False
        all_strong_elements_in_message_box = (
            self.get_texts_from_elements(ProductPageLocators.MESSAGE_ELEMENT_STRONG))
        error_message = (f"Product name '{self.product_name}' "
                                      f"does not match any in message box: {all_strong_elements_in_message_box}")
        for element in all_strong_elements_in_message_box:
            if self.product_name in element:
                if self.product_name == element:
                    product_name_is_same = True

                else:
                    product_name_is_same = False
                    error_message = f"Product name '{self.product_name}' does not match product in basket '{element}' "
                break
        assert product_name_is_same, error_message

    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    def should_match_product_price_in_basket(self):
        """
        Проверяет, что цена продукта в корзине совпадает с ценой на странице.
        :return: None
        """
        result, error_message = self.assert_exact_match(ProductPageLocators.PRODUCT_PRICE, ProductPageLocators.BASKET_TOTAL_IN_NAVBAR)
        if not result:
            error_message = f"Product price '{self.product_price}' does not match basket total: {error_message}"
        assert result, error_message
