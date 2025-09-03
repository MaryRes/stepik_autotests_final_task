import pytest
from .pages.product_page import ProductPage
from .urls import TEST_PROMO_PRODUCT_PAGE_URL, TEST_PAGE_URL

@pytest.mark.new
@pytest.mark.parametrize('url', [TEST_PROMO_PRODUCT_PAGE_URL])
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