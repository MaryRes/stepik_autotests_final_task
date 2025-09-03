from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_LINK_INVALID = (By.CSS_SELECTOR, "#login_link_inc")
    USER_ICON = (By.CSS_SELECTOR, ".icon-user")


class BasketPageLocators:
    BASKET_BOX = (By.CSS_SELECTOR, 'div[id="content_inner"]')
    ITEMS_IN_BASKET = (By.CSS_SELECTOR, 'div[id="content_inner"] form')


class MainPaigeLocators:
    # ссылка на корзину в шапке сайта
    BASKET_LINK_IN_HEADER = (By.CSS_SELECTOR, 'div[class*="basket-mini"] > span.btn-group > a[href*="basket"]')


class LoginPageLocators:
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")
    LOGIN_FORM = (By.CSS_SELECTOR, 'form[id*="login"]')
    REGISTRATION_FORM = (By.CSS_SELECTOR, 'form[id*="register"]')
    REGISTRATION_EMAIL = (By.CSS_SELECTOR, "[id='register_form'] input[id*='registration-email']")
    REGISTRATION_PASSWORD1 = (By.CSS_SELECTOR, "[id='register_form'] input[id*='password1']")
    REGISTRATION_PASSWORD2 = (By.CSS_SELECTOR, "[id='register_form'] input[id*='password2']")
    REGISTRATION_BUTTON = (By.CSS_SELECTOR, "[id='register_form'] button[type='submit']")


class ProductPageLocators:
    ADD_TO_BASKET_BTN = (By.CSS_SELECTOR, '[class*="btn-add-to-basket"]')
    # ссылка на корзину в шапке сайта
    BASKET_LINK_IN_HEADER = (By.CSS_SELECTOR, 'div[class*="basket-mini"] > span.btn-group > a[href*="basket"]')
    # селектор для названия продукта, который будет одинаковым
    # до и после клика на add_to_basket
    PRODUCT_NAME = (By.CSS_SELECTOR, '[class*=product_main] h1')  # до и после клика один и тот же селектор
    PRODUCT_PRICE = (
    By.CSS_SELECTOR, '[class*="product_main"] [class*="price_color"]')  # до и после клика один и тот же селектор
    # сообщения, 1 из них содержит название книги и текст, что она добавлена в корзину
    BASKET_MESSAGE_BOX = (By.CSS_SELECTOR, '[id="messages"]')
    # список элементов "хлебные крошки", в которых последним элементом должно быть название книги
    BREADCRUMB_BOX = (By.XPATH, '//ul[@class="breadcrumb"]//li[last()]')

    # несколько сообщений: название книги, сообщение о получении бонуса, общая стоимость всей корзины
    MESSAGE_ELEMENT_STRONG = (By.CSS_SELECTOR, '[class*="alertinner"] strong')
    MESSAGE_ELEMENT = (By.CSS_SELECTOR, '[class*="alertinner"]')
    PRODUCT_PRICE_INCLUDED_TAX_ROW = (By.XPATH, "//th[text()='Price (incl. tax)']/..//td")

    # Общая цена корзины
    BASKET_TOTAL_IN_NAVBAR = (By.CSS_SELECTOR, '[class*="basket-mini pull-right"]')
    BASKET_TOTAL_IN_NAVBAR_STRONG = (By.CSS_SELECTOR, '[class*="basket-mini pull-right"] strong')
    BASKET_TOTAL_IN_NAVBAR_ONLY_TEXT = (By.CSS_SELECTOR, '[class*="basket-mini pull-right"] span[class*="total"]')
    BASKET_TOTAL_IN_MESSAGE_BOX = (By.XPATH, "//div[@id='messages']//p[contains(., 'basket total')]//strong")
    # список элементов, которые содержат название продукта (названия должны быть одинаковыми)
    # элементы могут быть списками элементов, например, MESSAGE_ELEMENT_STRONG
    list_of_product_titles = [PRODUCT_NAME, MESSAGE_ELEMENT_STRONG, BREADCRUMB_BOX]

    # список элементов, которые содержат цену с НДС за 1 шт. товара
    list_of_item_prices = [PRODUCT_PRICE, PRODUCT_PRICE_INCLUDED_TAX_ROW]

    # список элементов с общей ценой корзины (может содержать одиночные элементы и списки элементов,
    # содержащих цену, например, MESSAGE_ELEMENT_STRONG)
    list_of_basket_total = [BASKET_TOTAL_IN_NAVBAR, BASKET_TOTAL_IN_MESSAGE_BOX]
