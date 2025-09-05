import pytest
from .pages.product_page import ProductPage
from .pages.basket_page import BasketPage
from .urls import TEST_PROMO_PRODUCT_PAGE_URL, BASE_URL, TEST_PAGE_URL, PRODUCT_PAGE_URL, get_promo_urls

# Определяем багнутую ссылку
BUGGED_OFFER = "offer7"

all_urls = get_promo_urls()

# Создаем список параметров с маркировками
test_data = []
for url in all_urls:
    if BUGGED_OFFER in url:
        test_data.append(pytest.param(url, marks=pytest.mark.xfail(reason="Known bug in offer7")))
    else:
        test_data.append(url)


@pytest.mark.parametrize('url', test_data)
def test_guest_can_add_product_to_basket(browser, url):
    page = ProductPage(browser, url)
    page.open()

    # проверить, что есть кнопка добавить в корзину
    page.should_be_add_to_basket_button()

    page.click_add_to_basket()
    # *Посчитать результат математического выражения и ввести ответ.
    page.solve_quiz_and_get_code()
    # Ожидаемый результат:
    # Сообщение о том, что товар добавлен в корзину.
    page.should_be_success_message()
    # Название товара в сообщении должно совпадать с тем товаром,
    # который вы действительно добавили.
    page.should_have_correct_product_name_in_message_box()
    #Сообщение со стоимостью корзины.
    page.should_show_basket_total_message()
    # Стоимость корзины совпадает с ценой товара.
    page.should_have_correct_price_in_message_box()


@pytest.mark.xfail(reason="Success message SHOULD appear after adding product, this test checks the opposite behavior")
@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_should_be_and_not_to_be_success_message(browser, url):
    page = ProductPage(browser, url)
    page.open()

    # на странице товара ожидаем, что там нет сообщения об успешном добавлении в корзину
    page.should_not_be_success_message()
    page.click_add_to_basket()
    # Посчитать результат математического выражения и ввести ответ.
    page.solve_quiz_and_get_code()
    # Сообщение о том, что товар добавлен в корзину.
    page.should_be_success_message()
    # элемент присутствует на странице и должен исчезнуть
    page.success_message_should_disappear()


@pytest.mark.xfail(reason="Success message SHOULD appear after adding product, this test checks the opposite behavior")
@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_guest_cant_see_success_message_after_adding_product_to_basket(browser, url):
    """
    This test SHOULD fail - success message appears after adding product to basket.
    Tests incorrect behavior, so marked as xfail.
    """
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()
    # Добавляем товар в корзину
    page.click_add_to_basket()
    # Проверяем, что нет сообщения об успехе с помощью is_not_element_present.
    page.should_not_be_success_message()


@pytest.mark.parametrize('url', [PRODUCT_PAGE_URL])
def test_guest_can_go_to_login_page_from_product_page(browser, url):
    page = ProductPage(browser, url)
    page.open()
    page.go_to_login_page()


@pytest.mark.parametrize('url', [TEST_PAGE_URL, PRODUCT_PAGE_URL])
def test_guest_should_see_login_link_on_product_page(browser, url):
    page = ProductPage(browser, url)
    page.open()
    page.should_be_login_link()


@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_guest_cant_see_success_message(browser, url):
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()
    # Проверяем, что нет сообщения об успехе с помощью is_not_element_present
    page.should_not_be_success_message()


@pytest.mark.xfail(reason="Success message should NOT disappear immediately after adding product")
@pytest.mark.parametrize('url', [TEST_PAGE_URL])
def test_message_disappeared_after_adding_product_to_basket(browser, url):
    """
    This test SHOULD fail - success message doesn't disappear immediately after adding.
    Tests incorrect behavior, so marked as xfail.
    """
    # Открываем страницу товара
    page = ProductPage(browser, url)
    page.open()
    # Добавляем товар в корзину
    page.click_add_to_basket()
    # Проверяем, что нет сообщения об успехе с помощью is_disappeared
    page.success_message_should_disappear()

@pytest.mark.new
@pytest.mark.parametrize('url', [PRODUCT_PAGE_URL])
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser, url):

    # Гость открывает страницу товара
    page = ProductPage(browser, url)
    page.open()
    page.click_add_to_basket()
    # Переходит в корзину по кнопке в шапке
    page.go_to_basket_page()
    # Ожидаем, что в корзине нет товаров
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_basket_empty()
    # Ожидаем, что есть текст о том что корзина пуста
    basket_page.should_display_empty_basket_message()
