import functools
import os
from datetime import datetime

class Decorators:
    @staticmethod
    def print_function_name(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            print(f"🔧 Calling: {func.__name__}")
            print(f"Result: {result}")
            return result
        return wrapper

    @staticmethod
    def screenshot_on_error(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
                print(f"✅ {func.__name__} executed successfully.")
                print(f"Result: {result}")
                return result
            except AssertionError as e:
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                func_name = func.__name__
                filename = f"screenshots/{func_name}_{timestamp}.png"
                os.makedirs("screenshots", exist_ok=True)

                if hasattr(self, "browser"):
                    self.browser.save_screenshot(filename)
                    print(f"📸 Screenshot saved to {filename}")
                else:
                    print(f"⚠️ Can't take screenshot: no 'browser' attribute.")

                raise e
        return wrapper

    @staticmethod
    def no_implicit_wait(func):
        """
        Decorator to disable implicit wait for the duration of the function call.
        :param func:
        :return:
        """
        @functools.wraps(func)
        def wrapper(self, browser, *args, **kwargs):
            old_wait = browser.timeouts.implicit_wait
            browser.implicitly_wait(0)
            try:
                return func(self, browser, *args, **kwargs)
            finally:
                browser.implicitly_wait(old_wait)  # вернуть обратно

        return wrapper
