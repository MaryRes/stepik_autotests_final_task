import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .translations import translations
import time

# порог для "долго" в секундах
LONG_TEST_THRESHOLD = 1.0

def pytest_addoption(parser):
    """Добавление опций командной строки для выбора браузера, языка и headless/headed режима."""

    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language', action='store', default='en',
                     help="Choose language: ru, en, es, fr, etc.")

    parser.addoption('--headed', action='store_true', default=False,
                     help="Run browser in headed (non-headless) mode")

@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для запуска браузера с заданными параметрами."""

    # Получаем параметры командной строки
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    headed = request.config.getoption("headed")  # True если указана --headed
    print(f"\nstart {browser_name} browser for test..")

    # Инициализируем браузер в зависимости от выбранного
    if browser_name == "chrome":
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        options.add_argument('window-size=1920x935')   # Устанавливаем размер окна
        options.add_argument('--disable-gpu')  # Отключение GPU для headless режима
        #options.add_argument('--no-sandbox')  # Для некоторых окружений
        if not headed:
            options.add_argument('headless')  # headless по умолчанию

        browser = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", user_language)
        options.add_argument('--width=1920')
        options.add_argument('--height=935')

        if not headed:
            options.add_argument('--headless')  # headless по умолчанию

        browser = webdriver.Firefox(options=options)

    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    yield browser
    print("\nquit browser..")
    browser.quit()

@pytest.fixture(scope="function")
def translation_fixture(request):
    """Фикстура для получения переводов в зависимости от выбранного языка."""
    user_language = request.config.getoption("language")
    return translations.get(user_language, translations['en'])



@pytest.fixture(autouse=True)
def timer(request):
    """Фикстура для замера времени выполнения каждого теста с выводом URL страницы."""
    start = time.time()
    yield
    end = time.time()
    duration = end - start
    test_name = request.node.name

    # Пытаемся получить URL страницы
    url = None
    if 'page' in request.node.funcargs:
        page = request.node.funcargs['page']
        url = getattr(page, 'url', None)
    elif 'link' in request.node.funcargs:
        url = request.node.funcargs['link']

    url_str = f" | URL: {url}" if url else ""

    if duration > LONG_TEST_THRESHOLD:
        print(f"\n⏱ [SLOW TEST] {test_name}{url_str} took {duration:.3f} seconds")
    else:
        print(f"\n⏱ {test_name}{url_str} took {duration:.3f} seconds")
