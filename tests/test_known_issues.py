
import pytest

from stepik_autotests_final_task.known_issues import KnownIssues
from stepik_autotests_final_task.pages.product_page import ProductPage
from stepik_autotests_final_task.pages.locators import ProductPageLocators

# pytest -s -v tests/test_known_issues.py
class TestKnownIssues:
    """
    Tests to check known issues in the application.
    """

    @pytest.mark.parametrize("issue_name", KnownIssues.get_active_issues())
    def test_known_bugs_still_exist(self, browser, issue_name):
        """Тест проверяет, что известные баги все еще существуют"""
        issue = KnownIssues.ISSUES[issue_name]

        if issue_name == "NOTSET":  # Защита от пустого параметра
            pytest.skip("No active issues to test")

        if issue_name == "incorrect_product_name_bug":
            self._test_incorrect_product_name(browser, issue)

        # Здесь можно добавить дополнительные проверки, если необходимо


    def _test_incorrect_product_name(self, browser, issue):
        """Тест для бага с неправильным именем продукта"""

        page = ProductPage(browser, issue['url'])
        page.open()

        # 1. Save product name
        page.set_product_name()

        # 2. Click "Add to basket"
        page.click_add_to_basket()

        # 3. Handle quiz alert if present
        try:
            page.solve_quiz_and_get_code()
        except Exception:
            pass  # alert may not appear

        # 4. Получаем фактическое имя в корзине
        actual_name = None
        strong_elements = page.get_texts_from_elements(ProductPageLocators.MESSAGE_ELEMENT_STRONG)

        for element in strong_elements:
            if page.product_name in element or issue['expected_incorrect_value'] in element:
                actual_name = element
                break

        if actual_name is None:
            pytest.fail(f"Product name not found in basket messages. "
                        f"Expected bug: {issue['expected_incorrect_value']}")

        if issue['status'] == 'open':
            # БАГ ДОЛЖЕН СУЩЕСТВОВАТЬ
            assert actual_name == issue['expected_incorrect_value'], (
                f"Bug '{issue.get('name', 'unknown')}' might be fixed! "  # Используйте .get() для безопасности
                f"Expected: '{issue['expected_incorrect_value']}', Got: '{actual_name}'"
            )

        elif issue['status'] == 'fixed':
            # БАГ ДОЛЖЕН БЫТЬ ПОФИКШЕН
            assert actual_name == issue['expected_correct_value'], (
                f"Bug '{issue.get('name', 'unknown')}' is marked as fixed but still exists! "
                f"Expected: '{issue['expected_correct_value']}', Got: '{actual_name}'"
            )

        elif issue['status'] == 'wont_fix':
            pytest.skip(f"Bug won't be fixed: {issue.get('description', 'No description')}")

        else:
            pytest.fail(f"Unknown bug status: {issue['status']}")
