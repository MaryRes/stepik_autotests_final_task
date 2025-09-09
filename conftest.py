"""
CONFTEST.PY - КОНФИГУРАЦИЯ PYTEST И ФИКСТУРЫ ДЛЯ ТЕСТИРОВАНИЯ

Данный модуль содержит:
- Настройки командной строки для pytest
- Фикстуру браузера с поддержкой разных браузеров и языков
- Конфигурацию WebDriver Manager для автоматического управления драйверами
"""

import pytest
import logging
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Generator, Any

# Настройка логгера
logger = logging.getLogger(__name__)


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Добавляет кастомные опции командной строки для pytest.

    Args:
        parser: Парсер аргументов командной строки pytest
    """
    parser.addoption(
        '--browser_name',
        action='store',
        default="chrome",
        choices=["chrome", "firefox"],
        help="Выберите браузер для тестов: chrome или firefox"
    )
    parser.addoption(
        '--language',
        action='store',
        default='en',
        help='Выберите язык интерфейса: en, ru, es, fi, fr, de и т.д.'
    )
    parser.addoption(
        '--headless',
        action='store_true',
        default=False,
        help='Запуск браузера в headless-режиме (без графического интерфейса)'
    )


@pytest.fixture(scope="function")
def browser(request: pytest.FixtureRequest) -> Generator[webdriver.Remote, None, None]:
    """
    Фикстура для инициализации и закрытия браузера.

    Создает экземпляр браузера с указанными настройками и автоматически
    закрывает его после завершения теста.

    Args:
        request: Объект запроса фикстуры pytest

    Yields:
        webdriver.Remote: Экземпляр WebDriver для тестирования

    Raises:
        pytest.UsageError: При указании неподдерживаемого браузера
    """
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    headless = request.config.getoption("headless")

    logger.info("🔄 Инициализация браузера: %s, язык: %s", browser_name, user_language)

    # Получаем настройки браузера
    driver = get_browser_settings(browser_name, user_language, headless)

    # Устанавливаем неявные ожидания по умолчанию
    driver.implicitly_wait(10)

    # Максимизируем окно браузера
    driver.maximize_window()

    yield driver

    # Завершение работы браузера
    logger.info("🛑 Завершение работы браузера")
    print("\nquit browser..")
    driver.quit()


def get_browser_settings(
        browser_name: str = 'chrome',
        user_language: str = 'en',
        headless: bool = False
) -> webdriver.Remote:
    """
    Создает и настраивает экземпляр WebDriver с указанными параметрами.

    Args:
        browser_name: Название браузера ('chrome' или 'firefox')
        user_language: Язык интерфейса браузера
        headless: Флаг headless-режима

    Returns:
        webdriver.Remote: Настроенный экземпляр WebDriver

    Raises:
        pytest.UsageError: При указании неподдерживаемого браузера
    """
    if browser_name == "chrome":
        logger.debug("🚀 Запуск Chrome браузера с языком: %s", user_language)
        chrome_options = ChromeOptions()

        # Настройки языка
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': f'en,{user_language}'
        })

        # Headless режим
        if headless:
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # Дополнительные опции для стабильности
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')

        browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    elif browser_name == "firefox":
        logger.debug("🚀 Запуск Firefox браузера с языком: %s", user_language)
        firefox_options = FirefoxOptions()

        # Настройки языка
        firefox_options.set_preference('intl.accept_languages', f'en,{user_language}')

        # Headless режим
        if headless:
            firefox_options.add_argument('--headless')

        # Дополнительные настройки
        firefox_options.set_preference('dom.webnotifications.enabled', False)

        browser = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )

    else:
        error_msg = f"Неподдерживаемый браузер: {browser_name}. Используйте chrome или firefox"
        logger.error(error_msg)
        raise pytest.UsageError(error_msg)

    return browser


# Дополнительные хуки для улучшения тестирования
def pytest_configure(config: pytest.Config) -> None:
    """Конфигурация pytest при запуске."""
    config.addinivalue_line(
        "markers", "slow: маркировка медленных тестов (пропускать при --fast)"
    )


def pytest_sessionstart(session: pytest.Session) -> None:
    """Действия при начале тестовой сессии."""
    logger.info("🎬 Начало тестовой сессии")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Действия при завершении тестовой сессии."""
    logger.info("🏁 Завершение тестовой сессии с статусом: %s", exitstatus)
