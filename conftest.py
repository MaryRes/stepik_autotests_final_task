import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .translations import translations


def pytest_addoption(parser):
    """Добавление опций командной строки для выбора браузера и языка."""

    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language', action='store', default='en',
                     help="Choose language: ru, en, es, fr, etc.")

@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для запуска браузера с заданными параметрами."""

    # Получаем параметры командной строки
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    print(f"\nstart {browser_name} browser for test..")
    # Устанавливаем настройки браузера для языка
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
    # Инициализируем браузер в зависимости от выбранного
    if browser_name == "chrome":
        browser = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(options=options)
    else:
        # Если браузер не поддерживается, выбрасываем исключение
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    print("\nstart browser for test..")

    yield browser
    print("\nquit browser..")
    browser.quit()

@pytest.fixture(scope="function")
def translation_fixture(request):
    """Фикстура для получения переводов в зависимости от выбранного языка."""
    user_language = request.config.getoption("language")
    return translations.get(user_language, translations['en'])
