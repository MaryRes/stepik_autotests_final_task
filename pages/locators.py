from selenium.webdriver.common.by import By

class MainPaigeLocators:
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")

class LoginPageLocators:
    LOGIN_FORM = (By.CSS_SELECTOR, 'form[id*="login"]')
    REGISTRATION_FORM = (By.CSS_SELECTOR, 'form[id*="register"]')

class ProductPageLocators:
    ADD_TO_BASKET_BTN = (By.CSS_SELECTOR, '[class*="btn-add-to-basket"]')
    # до и после клика на add_to_basket
    PRODUCT_NAME = (By.CSS_SELECTOR, '[class*=product_main] h1')  # до и после клика один и тот же селектор
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[class*=price_color]')  # до и после клика один и тот же селектор
    # сообщения, 1 из них содержит название книги и текст, что она добавлена в корзину
    BASKET_MESSAGE_BOX = (By.CSS_SELECTOR, '[id="messages"]')
    # список элементов "хлебные крошки", в которых последним элементом должно быть название книги
    BREADCRUMB_BOX = (By.XPATH, '//ul[@class="breadcrumb"]//li[last()]')

    # несколько сообщений: название книги, сообщение о получении бонуса, общая стоимость всей корзины
    MESSAGE_ELEMENT_STRONG = (By.CSS_SELECTOR, '[class*="alertinner"] strong')
    MESSAGE_ELEMENT = (By.CSS_SELECTOR, '[class*="alertinner"]')
    PRODUCT_PRICE_INCLUDED_TAX_ROW = (By.XPATH, "//th[text()='Price (incl. tax)']/..//td")

    # Общая цена корзины
    BASKET_TOTAL_IN_NAVBAR = (By.XPATH, "//a[contains(@href, '/basket') and contains(., 'Total:')]")
    BASKET_TOTAL_IN_MESSAGE_BOX = (By.XPATH, "//div[@id='messages']//p[contains(., 'basket total')]//strong")
    # список элементов, которые содержат название продукта (названия должны быть одинаковыми)
    # элементы могут быть списками элементов, например, MESSAGE_ELEMENT_STRONG
    list_of_product_titles = [PRODUCT_NAME, MESSAGE_ELEMENT_STRONG, BREADCRUMB_BOX]

    # список элементов, которые содержат цену с НДС за 1 шт. товара
    list_of_item_prices = [PRODUCT_PRICE, PRODUCT_PRICE_INCLUDED_TAX_ROW]

    # список элементов с общей ценой корзины (может содержать одиночные элементы и списки элементов,
    # содержащих цену, например, MESSAGE_ELEMENT_STRONG)
    list_of_basket_total = [BASKET_TOTAL_IN_NAVBAR, BASKET_TOTAL_IN_MESSAGE_BOX]
