import sys
import pytest
import os
sys.path.append("C:/Users/maria/OneDrive/Desktop/P3/selenium_tests")
from utils.driver import create_driver
from selenium.common.exceptions import UnexpectedAlertPresentException

SCREENSHOT_DIR = "selenium_tests/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    """

    outcome = yield
    report = outcome.get_result()

    driver = item.funcargs.get("driver", None)
    if driver is None:
        return

    if report.when == "call":
        test_name = report.nodeid.replace("/", "_").replace("::", "_")
        filename = f"{SCREENSHOT_DIR}/{test_name}.png"

        try:
            driver.save_screenshot(filename)
            print(f"\n Captura automática: {filename}")
        except Exception as e:
            print(f" No se pudo guardar screenshot: {e}")


@pytest.fixture
def driver():
    from selenium_tests.utils.driver import create_driver
    driver = create_driver()
    yield driver
    driver.quit()
