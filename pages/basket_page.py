from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
import logging

from stepik_autotests_final_task.pages.base_page import BasePage
from stepik_autotests_final_task.pages.locators import BasketPageLocators

class BasketPage(BasePage):
    def __init__(self, *args, **kwargs):
        super(BasketPage, self).__init__(*args, **kwargs)
        self.wait = WebDriverWait(self.browser, timeout=10, poll_frequency=1)

    def get_basket_items(self):
        pass

    def get_total_price(self):
        pass

    def is_basket_empty(self, expected_message: str):
        """
        Проверяет, что корзина пуста.
        :return: True если корзина пуста, иначе False
        """
        basket_empty_message_present = self.wait_for_basket_empty_message_present(expected_message)
        basket_item_form_not_present = self.wait_for_basket_item_form_present() is None
        if basket_empty_message_present and basket_item_form_not_present:
            print("Корзина пуста")
            return True
        print("Корзина не пуста")
        return False

    def wait_for_basket_item_form_present(self):
        """ Ждёт появления элемента с описанием содержимого корзины."""
        basket_element = None
        try:
            # Ждём появления элемента (с проверкой видимости)
            basket_element = self.wait.until(EC.visibility_of_element_located(BasketPageLocators.ITEMS_IN_BASKET))
            print("Элемент найден и видим!")
        except TimeoutException:
            print("❌ Элемент с описанием содержимого корзины не появился в течение заданного времени")
        except NoSuchElementException:
            print("❌ Элемент не найден в DOM")
        except StaleElementReferenceException:
            print("❌ Элемент был найден, но 'устарел' (DOM изменился)")
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {type(e).__name__} - {str(e)}")
        return basket_element


    def wait_for_basket_empty_message_present(self, expected_message: str):
        """ Ждёт появления элемента с сообщением о пустой корзине."""
        empty_basket_element = None
        try:
            # Ждём появления элемента (с проверкой видимости)
            empty_basket_element = self.wait.until(EC.visibility_of_element_located(BasketPageLocators.BASKET_BOX))
            print("Элемент с сообщением о пустой корзине найден и видим!")
        except TimeoutException:
            print("❌ Элемент с сообщением о пустой корзине не появился в течение заданного времени")
        except NoSuchElementException:
            print("❌ Элемент не найден в DOM")
        except StaleElementReferenceException:
            print("❌ Элемент был найден, но 'устарел' (DOM изменился)")
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {type(e).__name__} - {str(e)}")
        if empty_basket_element:
            # Проверяем, что текст элемента соответствует ожидаемому сообщению
            actual_message = empty_basket_element.text.strip()
            if expected_message not in actual_message:
                logging.error(f"Ожидалось сообщение '{expected_message}', но получено '{actual_message}'")
                return False
        return True

    def should_be_basket_page(self):
        """
        Проверяет, что текущая страница является страницей корзины.
        :return: None
        """
        assert self.is_element_present(*BasketPageLocators.BASKET_BOX), "Basket box is not present on the page"
        assert self.browser.current_url.endswith("/basket/"), "Current URL does not end with '/basket/'"
