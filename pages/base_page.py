import math
from typing import List, Tuple, Optional, Union
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time


class BasePage:
    """Базовый класс страницы. Содержит общие методы для всех страниц."""

    def __init__(self, browser: WebDriver, url: str, timeout: int = 10, implicitly_wait_on: bool = True):
        """
        :param browser: экземпляр WebDriver
        :param url: адрес страницы
        :param timeout: время ожидания элементов
        :param implicitly_wait_on: если True, устанавливает неявное ожидание timeout для браузера
        """
        self.browser = browser
        self.url = url
        if implicitly_wait_on:
            self.browser.implicitly_wait(timeout)


    def open(self) -> None:
        """Открывает страницу."""
        self.browser.get(self.url)

    def take_screenshot(self, name: str) -> str:
        """
        Делает скриншот страницы.
        :param name: имя файла скриншота
        :return: путь к сохраненному файлу
        """
        filename = f"{name}.png"
        self.browser.save_screenshot(filename)
        return filename

    def is_element_present(self, how: By, what: str) -> bool:
        """
        Проверяет наличие элемента на странице.
        :param how: способ поиска (By.ID, By.CSS_SELECTOR и т.д.)
        :param what: значение локатора
        :return: True если элемент найден, иначе False
        """
        try:
            self.browser.find_element(how, what)
            return True
        except NoSuchElementException:
            return False

    def solve_quiz_and_get_code(self) -> None:
        """
        Решает математический квиз из alert и принимает результат.
        Если есть второй alert, выводит код.
        """
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs(12 * math.sin(float(x)))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")

    # ====== Методы для работы с текстом элементов ======

    def _get_element_text(self, locator: Tuple[By, str]) -> str:
        """Возвращает текст первого найденного элемента по локатору."""
        return self.browser.find_element(*locator).text.strip()

    def _get_elements_texts(self, locator: Tuple[By, str]) -> List[str]:
        """Возвращает список текстов всех найденных элементов по локатору."""
        return [el.text.strip() for el in self.browser.find_elements(*locator)]

    def get_text_from_element(self, locator: Tuple[By, str]) -> str:
        """Публичная версия для получения текста одного элемента."""
        return self._get_element_text(locator)

    def get_texts_from_elements(self, locator: Tuple[By, str]) -> List[str]:
        """Публичная версия для получения текста всех элементов."""
        return self._get_elements_texts(locator)

    @staticmethod
    def wait_certain_seconds_before_action(seconds: int = 10) -> None:
        """Ожидает указанное количество секунд перед выполнением действия."""
        time.sleep(seconds)

    # ====== Методы проверки ======

    def assert_exact_match(self, locator_a: Tuple[By, str], locator_b: Tuple[By, str]) -> None:
        """Проверяет, что текст элемента A равен тексту элемента B."""
        text_a = self._get_element_text(locator_a)
        text_b = self._get_element_text(locator_b)
        assert text_a == text_b, f"'{text_a}' != '{text_b}'"

    def assert_texts_equal(self, locators: List[Union[Tuple[By, str], List[Tuple[By, str]]]]) -> None:
        """Проверяет, что все элементы из списка имеют одинаковый текст."""
        texts = []
        for locator in locators:
            if isinstance(locator, tuple):
                texts.extend(self._get_elements_texts(locator))
            elif isinstance(locator, list):
                for sublocator in locator:
                    texts.extend(self._get_elements_texts(sublocator))
        assert len(set(texts)) == 1, f"Тексты не совпадают: {texts}"

    def assert_contains_any(self, source_locator: Tuple[By, str], target_locators: List[Union[Tuple[By, str], List[Tuple[By, str]]]]) -> None:
        """
        Проверяет, что хотя бы один из элементов из target_locators содержится в тексте source_locator.
        """
        source_text = self._get_element_text(source_locator)
        for locator in target_locators:
            if isinstance(locator, tuple):
                if any(text in source_text for text in self._get_elements_texts(locator)):
                    return
            elif isinstance(locator, list):
                for sublocator in locator:
                    if any(text in source_text for text in self._get_elements_texts(sublocator)):
                        return
        raise AssertionError(f"Ни один элемент {target_locators} не найден в тексте '{source_text}'")

    def check_same_value_in_different_sections(
        self,
        list_of_elements: List[Union[Tuple[By, str], List[Tuple[By, str]]]],
        expected_value: Optional[str] = None,
        flexible: bool = False
    ) -> Tuple[bool, str]:
        """
        Проверяет, что во всех переданных элементах одно и то же значение (текст или число).
        :param list_of_elements: список локаторов или списков локаторов
        :param expected_value: если передан, сверяем с ним; иначе берём первый найденный
        :param flexible: если True — сравнение числовых значений после конвертации
        :return: (True, "") если все совпадает, иначе (False, сообщение об ошибке)
        """
        found_values: List[str] = []

        for element in list_of_elements:
            if isinstance(element, list):
                for sub_element in element:
                    elems = self.browser.find_elements(*sub_element)
                    found_values.extend([el.text.strip() for el in elems])
            else:
                elems = self.browser.find_elements(*element)
                found_values.extend([el.text.strip() for el in elems])

        if not found_values:
            return False, "Не найдено ни одного элемента для проверки."

        if expected_value is None:
            expected_value = found_values[0]

        def to_float(val: str) -> Optional[float]:
            try:
                return float("".join(ch for ch in val if ch.isdigit() or ch in ".,").replace(",", "."))
            except ValueError:
                return None

        if flexible:
            expected_float = to_float(str(expected_value))
            mismatches = [val for val in found_values if to_float(str(val)) != expected_float]
        else:
            mismatches = [val for val in found_values if val != expected_value]

        if mismatches:
            return False, f"Значения не совпадают. Ожидалось: '{expected_value}', найдено: {found_values}"

        return True, ""
