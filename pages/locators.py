from selenium.webdriver.common.by import By

class MainPaigeLocators:
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")

class LoginPageLocators:
    LOGIN_FORM = (By.CSS_SELECTOR, 'form[id*="login"]')
    REGISTRATION_FORM = (By.CSS_SELECTOR, 'form[id*="register"]')

class ProductPageLocators:
    ADD_TO_BASKET_BTN = (By.CSS_SELECTOR, '[class*="btn-add-to-basket"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[class*=product_main] h1')
    PRODUCT_PRICE = (By.CSS_SELECTOR, '[class*=price_color]')
    BASKET_MESSAGE_BOX = (By.CSS_SELECTOR, '[id="messages"]')
    MESSAGE_ELEMENT = (By.CSS_SELECTOR, '[class*="alertinner"]')
