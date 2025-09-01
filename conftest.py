import pytest
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default='en',
                     help='Choose your language: en, es, fi etc.')


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    user_language = request.config.getoption("language")
    browser = get_browser_settings(browser_name, user_language)

    yield browser
    print("\nquit browser..")
    browser.quit()

def get_browser_settings(browser_name='chrome', user_language='en'):
    if browser_name == "chrome":
        print(f"\nstart chrome browser for test with language: {user_language}..")
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option('prefs', {
            'intl.accept_languages': f'en,{user_language}'  # английский по умолчанию, затем пользовательский
        })
        browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    elif browser_name == "firefox":
        print(f"\nstart firefox browser for test with language: {user_language}..")
        firefox_options = FirefoxOptions()
        firefox_options.set_preference('intl.accept_languages', f'en,{user_language}')
        browser = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=firefox_options
        )
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")

    return browser

