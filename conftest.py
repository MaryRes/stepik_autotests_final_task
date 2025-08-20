import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .translations import translations, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
import time
from stepik_autotests_final_task.urls import Urls
from stepik_autotests_final_task.problematic_urls import ProblematicUrls
import sys

# порог для "долго" в секундах
LONG_TEST_THRESHOLD = 1.0

def pytest_addoption(parser):
    """Добавление опций командной строки для выбора браузера, языка и headless/headed режима."""

    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language', action='store', default='en-gb',
                     help="Choose language: ru, en-gb, es, fr, etc.")

    parser.addoption('--headed', action='store_true', default=False,
                     help="Run browser in headed (non-headless) mode")

@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для запуска браузера с заданными параметрами."""

    # Получаем параметры командной строки
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")

    # Автоматически определяем валидный язык
    valid_language = get_valid_language(user_language)

    if user_language != valid_language:
        print(f"⚠️  Язык '{user_language}' не поддерживается. Используется '{valid_language}'")

    # Проверяем есть ли маркер headed у теста
    has_headed_marker = request.node.get_closest_marker('headed') is not None

    # Если тест помечен headed или явно указан --headed
    headed = request.config.getoption("--headed") or has_headed_marker # True если указана --headed

    print(f"\nstart {browser_name} browser for test..")

    # Инициализируем браузер в зависимости от выбранного
    if browser_name == "chrome":
        options = Options()
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
        options.add_argument('window-size=1920x935')   # Устанавливаем размер окна

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

def get_system_language():
    """Получает язык системы."""
    try:
        system_lang, _ = locale.getdefaultlocale()
        if system_lang:
            return system_lang.lower()
    except:
        pass
    return DEFAULT_LANGUAGE

def get_valid_language(user_language):
    """
    Определяет валидный язык на основе пользовательских настроек.
    Если язык не поддерживается, возвращает английский.
    """
    if not user_language or user_language == 'auto':
        user_language = get_system_language()
    # Проверяем полное совпадение
    if user_language in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[user_language]

    # Проверяем основную часть языка (например, 'en' из 'en-US')
    language_base = user_language.split('-')[0].lower()
    if language_base in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[language_base]

    # Если язык не найден, возвращаем английский
    return DEFAULT_LANGUAGE

@pytest.fixture(scope="function")
def translation_fixture(request):
    """Фикстура для получения переводов в зависимости от выбранного языка."""
    user_language = request.config.getoption("language")
    valid_language = get_valid_language(user_language)
    return translations.get(valid_language, translations[DEFAULT_LANGUAGE])


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


def pytest_collection_modifyitems(config, items):
    pass
    #if not config.getoption("--headed"):
        #for item in items:
            #if "headed" in item.keywords:
                #pytest.skip(f"Тест пропущен, так как не выбран режим headed: {item.name}")

# ===
# get links
@pytest.fixture(scope="function")
def main_page_url(request) -> str:
    """Returns the main page URL for the detected language.
    :param request: pytest request object to access command line options
    """
    user_language = request.config.getoption("language")
    valid_language = get_valid_language(user_language)
    return Urls.main_page_url(valid_language)

@pytest.fixture(scope="function")
def login_page_url(request) -> str:
    """Returns the login page URL for the detected language.
    :param request: pytest request object to access command line options
    """
    user_language = request.config.getoption("language")
    valid_language = get_valid_language(user_language)
    return Urls.login_page_url(valid_language)

@pytest.fixture(scope="function")
def product_page_url(product_slug: str, request) -> str:
    """
    Returns the product page URL for the detected language.
    :param product_slug: Slug of the product
    :param request: pytest request object to access command line options
    """
    user_language = request.config.getoption("language")
    valid_language = get_valid_language(user_language)
    return Urls.product_page_url(product_slug, valid_language)

@pytest.fixture(scope="function")
def basket_page_url(request) -> str:
    """
    Returns the basket page URL for the detected language.
    :param request: pytest request object to access command line options
    """
    user_language = request.config.getoption("language")
    valid_language = get_valid_language(user_language)
    return Urls.basket_page_url(valid_language)

@pytest.fixture(scope="function")
def catalogue_page_url(request) -> str:
    """
    Returns the catalogue page URL for the detected language.
    :param request: pytest request object to access command line options
    """
    user_language = request.config.getoption("language")
    valid_language = get_valid_language(user_language)
    return Urls.catalogue_page_url(valid_language)


# ===
@pytest.fixture(params=ProblematicUrls.UI_BUGS.items())
def ui_bug_url(request):
    """
    Fixture to provide URLs that are known to have UI bugs.
    :return: Tuple of (URL, description)
    """
    bug_name, url = request.param
    return bug_name, url

@pytest.fixture
def known_broken_urls():
    """All known problematic URLs."""
    return ProblematicUrls.ALL_PROBLEMATIC_URLS
