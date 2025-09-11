"""
МОДУЛЬ URL-АДРЕСОВ ДЛЯ ТЕСТИРОВАНИЯ

Содержит все URL-адреса, используемые в тестах.
Централизованное хранение URL упрощает поддержку и обновление тестов.

ВСЕ URL ДОЛЖНЫ ХРАНИТЬСЯ ЗДЕСЬ - избегаем hardcoded ссылок в тестах!
"""

from typing import List

# Базовый URL тестового приложения
BASE_URL: str = "http://selenium1py.pythonanywhere.com"

# Основные страницы приложения
LOGIN_PAGE_URL: str = f"{BASE_URL}/fi/accounts/login/"
MAIN_PAGE_URL: str = BASE_URL  # Главная страница совпадает с базовым URL
PRODUCT_PAGE_URL: str = f"{BASE_URL}/en-gb/catalogue/the-city-and-the-stars_95/"

# Тестовые страницы для различных сценариев
TEST_PAGE_URL: str = f"{BASE_URL}/catalogue/the-shellcoders-handbook_209?promo=midsummer"
TEST_PROMO_PRODUCT_PAGE_URL: str = f"{BASE_URL}/catalogue/the-shellcoders-handbook_209/?promo=newYear"


def get_promo_urls(count: int = 10) -> List[str]:
    """
    Генерирует список промо-URL для тестирования различных акционных предложений.

    Используется для параметризованных тестов, проверяющих функциональность
    корзины на разных промо-страницах.

    Args:
        count: Количество генерируемых URL (по умолчанию 10)

    Returns:
        List[str]: Список промо-URL в формате:
        http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/?promo=offer{number}
    """
    return [f"{BASE_URL}/catalogue/coders-at-work_207/?promo=offer{no}" for no in range(count)]
