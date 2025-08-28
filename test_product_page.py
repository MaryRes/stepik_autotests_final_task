import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Any
from stepik_autotests_final_task.pages.product_page import ProductPage
from stepik_autotests_final_task.decorators import Decorators
from stepik_autotests_final_task.urls import Urls
from stepik_autotests_final_task.pages.basket_page import BasketPage
from stepik_autotests_final_task.pages.login_page import LoginPage
import random

# ================================================
# Test run commands:
# pytest -s test_product_page.py
# --browser_name=chrome --language=en --headed
# --headed - run browser in normal (non-headless) mode
# pytest -s -m ui test_product_page.py
# pytest -s -v -m ui
# ================================================

product_base_link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
product_page_link = "http://selenium1py.pythonanywhere.com/en-gb/catalogue/the-city-and-the-stars_95/"
link_list = [f"{product_base_link}/?promo=offer{no}" for no in range(10)]
bugged_link = f"{product_base_link}/?promo=offer7"
link_list.remove(bugged_link)  # Remove the buggy link from the main list

product_page_link = Urls.product_page_url("the-city-and-the-stars_95", "en-gb")

class TestProductPage:
    """
    A set of tests for the product page on the site.

    Tests cover:
    - adding a product to the basket,
    - checking the presence and disappearance of success messages,
    - verifying product name and price in the success message and basket.
    """
    @pytest.mark.new
    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    @pytest.mark.parametrize(
        "link",
        [*link_list, pytest.param(bugged_link, marks=pytest.mark.xfail)]
    )
    def test_guest_can_add_product_to_basket(
        self,
        browser: WebDriver,
        link: str,
        translation_fixture: dict[str, str]
    ) -> None:
        """
        Checks that a guest can add a product to the basket.

        Steps:
        1. Save the product's name and price.
        2. Verify that the "Add to basket" button is present.
        3. Click the "Add to basket" button and handle the quiz alert if it appears.
        4. Verify the success message.
        5. Verify that the product name in the message matches the product.
        6. Verify that the product price in the message matches the product.

        :param browser: WebDriver instance
        :param link: URL of the product page
        :param translation_fixture: dictionary with message texts in the selected language
        """
        page = ProductPage(browser, link)
        page.open()
        page.wait_for_page_load()

        added_to_basket_message = translation_fixture["added_to_basket"]
        print(f"Testing link: {link}")

        # 1️⃣ Save product name and price
        page.set_product_name()
        page.set_product_price()

        # 2️⃣ Verify "Add to basket" button exists
        page.should_be_add_to_basket_button()

        # 3️⃣ Click "Add to basket"
        page.click_add_to_basket()

        # 3.1️⃣ Handle quiz alert if present
        try:
            page.solve_quiz_and_get_code()
        except Exception:
            pass  # alert may not appear

        # 4️⃣ Check success message
        page.should_be_added_to_basket_message(added_to_basket_message)

        # 5️⃣ Check product name in the message
        page.should_match_product_name_in_basket()

        # 6️⃣ Check product price in the message
        page.should_match_product_price_in_basket()

    @pytest.mark.ui
    @pytest.mark.parametrize("link", [product_base_link])
    @Decorators.no_implicit_wait
    def test_guest_cant_see_success_message_after_adding_product_to_basket(
        self,
        browser: WebDriver,
        link: str,
        translation_fixture: dict[str, str]
    ) -> None:
        """
        Verifies that the success message does NOT appear after clicking,
        when the page is first opened. Implicit wait is disabled.

        :param browser: WebDriver instance
        :param link: URL of the product page
        :param translation_fixture: dictionary with message texts in the selected language
        """
        page = ProductPage(browser, link)
        page.open()

        added_to_basket_message = translation_fixture["added_to_basket"]

        page.click_add_to_basket()

        page.should_not_be_success_message(added_to_basket_message)

    @pytest.mark.ui
    @pytest.mark.parametrize("link", [product_base_link])
    @Decorators.no_implicit_wait
    def test_guest_cant_see_success_message(
        self,
        browser: WebDriver,
        link: str,
        translation_fixture: dict[str, str]
    ) -> None:
        """
        Verifies that the success message does not appear
        on the product page when it is opened normally.
        Implicit wait is disabled.

        :param browser: WebDriver instance
        :param link: URL of the product page
        :param translation_fixture: dictionary with message texts in the selected language
        """
        page = ProductPage(browser, link)
        page.open()

        added_to_basket_message = translation_fixture["added_to_basket"]

        page.should_not_be_success_message(added_to_basket_message)

    @pytest.mark.ui
    @pytest.mark.parametrize("link", [product_base_link])
    @Decorators.no_implicit_wait
    def test_message_disappeared_after_adding_product_to_basket(
        self,
        browser: WebDriver,
        link: str,
        translation_fixture: dict[str, str]
    ) -> None:
        """
        Verifies that the success message disappears after adding a product
        to the basket. Implicit wait is disabled.

        :param browser: WebDriver instance
        :param link: URL of the product page
        :param translation_fixture: dictionary with message texts in the selected language
        """
        page = ProductPage(browser, link)
        page.open()

        added_to_basket_message = translation_fixture["added_to_basket"]

        page.click_add_to_basket()

        page.should_success_message_disappeared(added_to_basket_message)

    @pytest.mark.ui
    @pytest.mark.parametrize("link", [product_page_link])
    def test_guest_should_see_login_link_on_product_page(self, browser, link: str) -> None:

        page = ProductPage(browser, link)
        page.open()
        page.should_be_login_link()

    @pytest.mark.headed
    @pytest.mark.parametrize("link", [product_page_link])
    @Decorators.no_implicit_wait
    def test_guest_can_go_to_login_page_from_product_page(self, browser, link: str) -> None:
        """
        Checks that a guest can navigate to the login page from the product page.

        :param browser: WebDriver instance
        :param link: URL of the product page
        """
        page = ProductPage(browser, link)
        page.open()
        page.go_to_login_page()


        # Verify that we are on the login page
        print(f"started from link: {link}")
        print(f"Current URL: {browser.current_url}")
        print(f"Expected URL to contain 'login': {link}")
        assert "login" in browser.current_url, "Not on the login page"

    @pytest.mark.ui
    @pytest.mark.headed
    @pytest.mark.parametrize("link", [product_page_link])
    def test_guest_cant_see_product_in_basket_opened_from_product_page(
            self,
            browser: WebDriver,
            link: str,
            translation_fixture: dict[str, str]
    ) -> None:
        """
        Checks that a guest cannot see a product in the basket when opened from the product page.

        :param browser: WebDriver instance
        :param link: URL of the product page
        :param translation_fixture: Dictionary with translations
        """
        # Гость открывает страницу товара
        page = ProductPage(browser, link)  # ⬅️ Используйте параметр link
        page.open()

        # Переходит в корзину по кнопке в шапке
        page.go_to_basket_from_header()

        # Проверяем, что мы на странице корзины
        basket_page = BasketPage(browser, browser.current_url)
        basket_page.should_be_basket_page()

        # Получаем сообщение о пустой корзине из фикстуры
        basket_empty_message = translation_fixture["basket_is_empty"]

        # Проверяем что корзина пуста
        assert basket_page.is_basket_empty(basket_empty_message), "Basket is not empty, but should be empty"


class TestUserAddToBasketFromProductPage:
    """Класс для тестов зарегистрированного пользователя"""


    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser: WebDriver, login_page_url: str) -> None:
        """
        Setup - performed before each test in the class
        Registers a new user

        Browser and Login_Page_Url are automatically available from Conftest.PY!
        """
        # 1. Открываем страницу регистрации
        login_page = LoginPage(browser, login_page_url)
        login_page.open()

        # 2. Регистрируем нового пользователя
        email = f"test{random.randint(1000, 9999)}@example.com"
        password = "TestPassword123"
        login_page.register_new_user(email, password)

        # 3. Проверяем что пользователь залогинен
        login_page.should_be_authorized_user()


    @Decorators.no_implicit_wait
    def test_user_cant_see_success_message_after_adding_product_to_basket(
            self,
            browser: WebDriver,
            product_page_url: str,
            product_slug: str,
            translation_fixture: dict[str, str]
    ) -> None:
        """
        Verifies that the success message does NOT appear after clicking,
        when the page is first opened. Implicit wait is disabled.

        :param browser: WebDriver instance
        :param link: URL of the product page
        :param translation_fixture: dictionary with message texts in the selected language
        """
        page = ProductPage(browser, product_page_url)
        page.open()

        added_to_basket_message = translation_fixture["added_to_basket"]

        page.click_add_to_basket()

        page.should_not_be_success_message(added_to_basket_message)

    #@pytest.mark.new
    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    @pytest.mark.parametrize("link", [product_page_link])
    def test_user_can_add_product_to_basket(
        self,
        browser: WebDriver,
        link: str,
        translation_fixture: dict[str, str]
    ) -> None:
        """
        Checks that a guest can add a product to the basket.

        Steps:
        1. Save the product's name and price.
        2. Verify that the "Add to basket" button is present.
        3. Click the "Add to basket" button and handle the quiz alert if it appears.
        4. Verify the success message.
        5. Verify that the product name in the message matches the product.
        6. Verify that the product price in the message matches the product.

        :param browser: WebDriver instance
        :param link: URL of the product page
        :param translation_fixture: dictionary with message texts in the selected language
        """
        page = ProductPage(browser, link)
        page.open()
        page.wait_for_page_load()

        added_to_basket_message = translation_fixture["added_to_basket"]

        # 1️⃣ Save product name and price
        page.set_product_name()
        page.set_product_price()

        # 2️⃣ Verify "Add to basket" button exists
        page.should_be_add_to_basket_button()

        # 3️⃣ Click "Add to basket"
        page.click_add_to_basket()

        # 3.1️⃣ Handle quiz alert if present
        try:
            page.solve_quiz_and_get_code()
        except Exception:
            pass  # alert may not appear

        # 4️⃣ Check success message
        page.should_be_added_to_basket_message(added_to_basket_message)

        # 5️⃣ Check product name in the message
        page.should_match_product_name_in_basket()

        # 6️⃣ Check product price in the message
        page.should_match_product_price_in_basket()

    @pytest.mark.version
    @pytest.mark.headed
    def test_get_dict_basket_total(self, browser, product_page_url):
        page = ProductPage(browser, product_page_url)
        page.open()
        page.wait_for_page_load()
        page.click_add_to_basket()

        page.get_dict_basket_total()


