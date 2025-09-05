from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):

    def should_be_basket_empty(self):
        assert self.is_not_element_present(*BasketPageLocators.ITEMS_IN_BASKET), \
            "basket is not empty"

    def should_display_empty_basket_message(self):
        message_element_present = self.is_element_present(*BasketPageLocators.BASKET_BOX)
        message_text = self.browser.find_element(*BasketPageLocators.BASKET_BOX).text
        empty_basket_message_displayed = all([message_element_present, len(message_text) > 1])
        assert empty_basket_message_displayed, \
            "no messages displayed, expected 'empty basket' message"
