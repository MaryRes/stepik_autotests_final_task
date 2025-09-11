"""
BASE PAGE OBJECT МОДЕЛЬ - БАЗОВЫЙ КЛАСС ДЛЯ ВСЕХ СТРАНИЦ

Данный модуль содержит базовый класс BasePage, от которого наследуются все другие Page Object классы.
Класс предоставляет общие методы для работы с веб-страницами, управления ожиданиями и обработки исключений.

ОСНОВНЫЕ ФУНКЦИОНАЛЬНЫЕ ВОЗМОЖНОСТИ:
- Навигация по страницам и базовые взаимодействия с браузером
- Управление явными и неявными ожиданиями элементов
- Обработка алертов и математических капч
- Проверки авторизации пользователя и наличия элементов
- Универсальные методы ожидания элементов
"""

from selenium.common.exceptions import (NoSuchElementException,
                                        NoAlertPresentException,
                                        TimeoutException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
from typing import Union, Tuple, Any

# Импорты Page Object моделей и локаторов
from .locators import BasePageLocators


class BasePage():
    """
    Базовый класс для всех Page Object моделей.

    Содержит общие методы для работы с веб-страницами, которые могут быть
    использованы на любой странице сайта. Все специфичные страницы наследуются
    от этого класса.

    Атрибуты:
        browser: Экземпляр веб-браузера для управления страницей
        url: URL-адрес страницы
        timeout: Таймаут неявного ожидания по умолчанию в секундах
    """

    def __init__(self, browser, url: str, timeout: int = 10) -> None:
        """
        Инициализация базовой страницы.

        Args:
            browser: Экземпляр веб-браузера
            url: URL адрес страницы
            timeout: Таймаут неявного ожидания в секундах (по умолчанию 10)
        """
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait = timeout

    def go_to_basket_page(self) -> None:
        """
        Переходит на страницу корзины через клик по ссылке в шапке сайта.

        Находит ссылку на корзину в верхней части страницы и выполняет клик
        для перехода на страницу корзины покупок.

        Пример использования:
            base_page.go_to_basket_page()

        Raises:
            NoSuchElementException: Если ссылка на корзину не найдена
        """
        link = self.browser.find_element(*BasePageLocators.BASKET_LINK_IN_HEADER)
        link.click()

    def go_to_login_page(self) -> None:
        """
        Переходит на страницу логина с обработкой различных селекторов.

        Некоторые страницы используют разные селекторы для ссылки логина.
        Метод ожидает появления любого из возможных элементов логина.

        Raises:
            TimeoutException: Если ни один элемент логина не появился в течение 10 секунд
        """
        # Ожидаем появления любого из возможных элементов логина
        login_link = WebDriverWait(self.browser, 10).until(
            EC.any_of(
                EC.presence_of_element_located(BasePageLocators.LOGIN_LINK),
                EC.presence_of_element_located(BasePageLocators.REGISTRATION_LINK)
            )
        )
        login_link.click()

    def is_disappeared(self, how: Any, what: str, timeout: int = 4) -> bool:
        """
        Проверяет, что элемент исчезает со страницы в течение заданного времени.

        Args:
            how: Метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            what: Селектор элемента
            timeout: Максимальное время ожидания в секундах (по умолчанию 4)

        Returns:
            bool: True если элемент исчез в течение timeout, иначе False

        Example:
            page.is_disappeared(By.ID, "loading-spinner")
        """
        try:
            WebDriverWait(self.browser, timeout, poll_frequency=1).until_not(
                EC.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return False
        return True

    def is_element_present(self, how: Any, what: str) -> bool:
        """
        Проверяет наличие элемента на странице без явных ожиданий.

        Args:
            how: Метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            what: Селектор элемента

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

    def is_not_element_present(self, how: Any, what: str, timeout: int = 4) -> bool:
        """
        Проверяет отсутствие элемента на странице в течение заданного времени.

        Args:
            how: Метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            what: Селектор элемента
            timeout: Максимальное время ожидания в секундах (по умолчанию 4)

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

    def open(self) -> None:
        """
        Открывает страницу по указанному URL.

        Использует метод get() браузера для перехода по указанному адресу.
        """
        self.browser.get(self.url)

    def solve_quiz_and_get_code(self) -> None:
        """
        Решает математическую капчу в alert-окне и получает код.

        Обрабатывает алерт с математическим выражением, вычисляет ответ
        и вводит его в поле алерта. Используется для промо-акций с капчей.

        Raises:
            NoAlertPresentException: Если алерт не присутствует на странице
        """
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

    def should_be_authorized_user(self) -> None:
        """
        Проверяет, что пользователь авторизован в системе.

        Убеждается, что на странице присутствует иконка пользователя,
        которая обычно отображается только для авторизованных пользователей.

        Raises:
            AssertionError: Если иконка пользователя не найдена
        """
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
                                                                     " probably unauthorised user"

    def should_be_login_link(self) -> None:
        """
        Проверяет наличие хотя бы одной ссылки для входа на странице.

        Ожидает до 10 секунд появления любого из возможных селекторов
        ссылки логина или регистрации.

        Raises:
            AssertionError: Если ни одна ссылка логина не найдена в течение 10 секунд
            TimeoutException: Если время ожидания истекло
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

    def wait_for_element(self, by: Any, selector: str, timeout: int = 10) -> Any:
        """
        Ожидает появление элемента на странице.

        Args:
            by: Метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            selector: Селектор элемента
            timeout: Максимальное время ожидания в секундах (по умолчанию 10)

        Returns:
            WebElement: Найденный элемент

        Raises:
            TimeoutException: Если элемент не найден в течение timeout
        """
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, selector)),
            message=f"Element not found: {selector}"
        )

    def wait_for_element_visible(self, by: Any, selector: str, timeout: int = 10) -> Any:
        """
        Ожидает пока элемент станет видимым на странице.

        Args:
            by: Метод поиска (By.ID, By.CSS_SELECTOR и т.д.)
            selector: Селектор элемента
            timeout: Максимальное время ожидания в секундах (по умолчанию 10)

        Returns:
            WebElement: Видимый элемент

        Raises:
            TimeoutException: Если элемент не стал видимым в течение timeout
        """
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located((by, selector)),
            message=f"Element not visible: {selector}"
        )
