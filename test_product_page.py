import pytest
from .pages.product_page import ProductPage
from .decorators import Decorators

#  pytest -s test_product_page.py

"""link_list = [
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer7",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer1",
    "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=newYear2019"
]"""
product_base_link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207"
link_list = [f"{product_base_link}/?promo=offer{no}" for no in range(10)]
bugged_link = f"{product_base_link}/?promo=offer7"
link_list.remove(bugged_link)  # Убираем багнутый линк из списка

class TestProductPage:
    @Decorators.print_function_name
    @Decorators.screenshot_on_error
    @pytest.mark.parametrize('link', [*link_list, pytest.param(bugged_link, marks=pytest.mark.xfail)])
    def test_guest_can_add_product_to_basket(self, browser, link, translation_fixture):
        page = ProductPage(browser, link)
        page.open()

        # 1️⃣ Сохраняем имя и цену продукта
        page.set_product_name()
        page.set_product_price()

        # 2️⃣ Проверяем, что кнопка "Добавить в корзину" присутствует
        page.should_be_add_to_basket_button()

        # 3️⃣ Нажимаем кнопку "Добавить в корзину"
        page.click_add_to_basket()

        # 3.1️⃣ Безопасно обрабатываем alert с квизом, если он появился
        try:
            page.solve_quiz_and_get_code()
        except Exception:
            # Если alert не появился, пропускаем
            pass

        # 4️⃣ Проверяем сообщение о добавлении продукта в корзину
        expected_message = translation_fixture['added_to_basket']
        page.should_be_added_to_basket_message(expected_message)

        # 5️⃣ Проверка соответствия названия продукта в сообщении
        page.should_match_product_name_in_basket()

        # 6️⃣ Проверка соответствия цены продукта в корзине
        page.should_match_product_price_in_basket()


