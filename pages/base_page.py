from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math


class BasePage():
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait = timeout
        self.timeout = timeout

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def open(self):
        self.browser.get(self.url)

    def solve_quiz_and_get_code(self):
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")

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
