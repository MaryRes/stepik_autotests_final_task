from .base_page import BasePage
from .locators import ProductPageLocators

add_to_basket_btn_element = ProductPageLocators.ADD_TO_BASKET_BTN
product_price_element = ProductPageLocators.PRODUCT_PRICE
product_name_element = ProductPageLocators.PRODUCT_NAME
basket_message_box_element = ProductPageLocators.BASKET_MESSAGE_BOX
basket_message_text_elements = ProductPageLocators.MESSAGE_ELEMENT


class ProductPage(BasePage):
    def __init__(self, browser, link):
        super().__init__(browser, link)
        self.data = dict()

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data[key]

    def set_product_name(self):
        product_name = self.browser.find_element(*product_name_element).text
        self.data['product_name'] = product_name

    def set_product_price(self):
        product_price = self.browser.find_element(*product_price_element).text
        self.data['product_price'] = product_price

    def get_message_box_texts(self):
        message_box = self.browser.find_element(*basket_message_box_element)
        text_in_box = message_box.find_elements(*basket_message_text_elements)
        return [element.text for element in text_in_box]

    def click_add_to_basket(self):
        basket = self.browser.find_element(*add_to_basket_btn_element)
        basket.click()
        self.solve_quiz_and_get_code()

    def should_be_add_to_basket_button(self):
        basket_btn = self.is_element_present(*add_to_basket_btn_element)
        assert basket_btn, "Absence of add to basket button"

    def should_be_added_to_basket_message(self):
        texts_in_box = self.get_message_box_texts()
        assert texts_in_box, "No texts found in the message box."

        expected_message = "has been added to your basket"
        result = any(expected_message.lower() in text.lower() for text in texts_in_box)

        assert result, f"Message '{expected_message}' not found. Found texts: {texts_in_box}"

    def should_match_product_name_in_basket(self):
        texts_in_box = self.get_message_box_texts()
        assert texts_in_box, "No texts found in the message box."

        expected_product_name = self.get_data('product_name')
        result = any(expected_product_name.lower() in text.lower() for text in texts_in_box)

        assert result, f"Expected product name '{expected_product_name}' not found. Found texts: {texts_in_box}"

    def should_match_product_price_in_basket(self):
        texts_in_box = self.get_message_box_texts()
        assert texts_in_box, "No texts found in the message box."

        expected_price = self.get_data('product_price')
        result = any(expected_price.lower() in text.lower() for text in texts_in_box)

        assert result, f"Expected price '{expected_price}' not found. Found texts: {texts_in_box}"

    def guest_can_add_product_to_basket(self):
        self.should_be_added_to_basket_message()
        self.should_match_product_name_in_basket()
        self.should_match_product_price_in_basket()
