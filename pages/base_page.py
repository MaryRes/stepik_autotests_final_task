from selenium.common.exceptions import (NoSuchElementException,
                                        NoAlertPresentException,
                                        TimeoutException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
from .locators import BasePageLocators


class BasePage():
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait = timeout

    def go_to_basket_page(self):
        """
        Находит в шапке сайта ссылну на страницу корзины и кликает на нее
        :return: None
        """
        link = self.browser.find_element(*BasePageLocators.BASKET_LINK_IN_HEADER)
        link.click()

    def go_to_login_page(self):
        """
        Navigates to login page using either LOGIN_LINK or REGISTRATION_LINK locator.

        Some product pages use different selectors for login link. This method
        handles both cases with explicit waiting.

        :raises TimeoutException: If no login element appears within 10 seconds
        :return: None
        """
        # Ждем появления любого из элементов
        login_link = WebDriverWait(self.browser, 10).until(
            EC.any_of(
                EC.presence_of_element_located(BasePageLocators.LOGIN_LINK),
                EC.presence_of_element_located(BasePageLocators.REGISTRATION_LINK)
            )
        )
        login_link.click()


    def is_disappeared(self, how, what, timeout=4):
        """
        Проверяет, что элемент исчезает со страницы в течение заданного времени.

        Args:
            how: метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            what: селектор элемента
            timeout: максимальное время ожидания в секундах (по умолчанию 4)

        Returns:
            bool: True если элемент исчез в течение timeout, иначе False

        Example:
            page.is_disappeared(By.ID, "loading-spinner")
            True
    """
        try:
            WebDriverWait(self.browser, timeout, poll_frequency=1).until_not(
                EC.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return False
        return True

    def is_element_present(self, how, what):
        """
        Проверяет наличие элемента на странице.

        Args:
            how: метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            what: селектор элемента

        Returns:
            bool: True если элемент найден, иначе False

        Note:
            Не использует явные ожидания. Проверяет наличие элемента мгновенно.
    """
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        """
        Проверяет отсутствие элемента на странице в течение заданного времени.

        Args:
            how: метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            what: селектор элемента
            timeout: максимальное время ожидания в секундах (по умолчанию 4)

        Returns:
            bool: True если элемент не появился в течение timeout, иначе False

        Note:
            Использует явные ожидания для проверки отсутствия элемента.
        """
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def open(self):
        self.browser.get(self.url)

    def solve_quiz_and_get_code(self):
        try:
            alert = self.browser.switch_to.alert
            x = alert.text.split(" ")[2]
            answer = str(math.log(abs((12 * math.sin(float(x))))))
            alert.send_keys(answer)
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")

    def should_be_login_link(self):
        """
        Verifies that at least one login link is present with explicit waiting.

        Some product pages use LOGIN_LINK selector while others use REGISTRATION_LINK.
        This method checks for both selectors with 10 seconds explicit wait.

        Steps:
        1. Waits up to 10 seconds for either LOGIN_LINK or REGISTRATION_LINK to appear
        2. Returns silently if any login link is found
        3. Raises AssertionError with diagnostic info if no link appears

        Raises:
            AssertionError: If neither login link selector is present after timeout
            TimeoutException: If wait timeout occurs (handled internally)

        :return: None
        """
        try:
            WebDriverWait(self.browser, 10).until(
                lambda driver: (
                        self.is_element_present(*BasePageLocators.LOGIN_LINK) or
                        self.is_element_present(*BasePageLocators.REGISTRATION_LINK)
                )
            )
        except TimeoutException:
            login_present = self.is_element_present(*BasePageLocators.LOGIN_LINK)
            registration_present = self.is_element_present(*BasePageLocators.REGISTRATION_LINK)

            raise AssertionError(
                f"Ссылка для входа не появилась за 10 секунд. "
                f"LOGIN_LINK: {login_present}, REGISTRATION_LINK: {registration_present}"
            )

    def wait_for_element(self, by, selector, timeout=10):
        """
        Ждет появление элемента на странице
        """
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, selector)),
            message=f"Element not found: {selector}"
        )

    def wait_for_element_visible(self, by, selector, timeout=10):
        """
        Ждет пока элемент станет видимым
        """
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located((by, selector)),
            message=f"Element not visible: {selector}"
        )
