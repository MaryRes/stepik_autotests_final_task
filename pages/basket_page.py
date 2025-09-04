from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):

    def should_be_basket_empty(self):
        assert self.is_not_element_present(*BasketPageLocators.ITEMS_IN_BASKET), \
            "basket is not empty"

    def should_display_empty_basket_message(self):
        assert self.is_element_present(*BasketPageLocators.BASKET_BOX), \
            "no messages displayed, expected 'empty basket' message"
