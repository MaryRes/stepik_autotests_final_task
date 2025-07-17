from selenium.webdriver.common.by import By

class MainPaigeLocators():
    LOGIN_LINK = (By.CSS_SELECTOR, "#login_link")

class LoginPageLocators():
    LOGIN_FORM = (By.CSS_SELECTOR, 'form[id*="login"]')
    REGISTRATION_FORM = (By.CSS_SELECTOR, 'form[id*="register"]')
