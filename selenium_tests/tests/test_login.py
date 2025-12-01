import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    from selenium_tests.utils.driver import create_driver
    driver = create_driver()
    yield driver
    driver.quit()


def esperar_alert(driver, timeout=4):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        return driver.switch_to.alert
    except TimeoutException:
        return None


def save_shot(driver, name):
    time.sleep(0.8)
    path = f"selenium_tests/screenshots/{name}.png"
    driver.save_screenshot(path)
    print(f"Screenshot guardado en: {path}")


def test_login_camino_feliz(driver):
    driver.get("file:///C:/Users/maria/OneDrive/Desktop/P3/CRUD/login.html")

    driver.execute_script(
        'localStorage.setItem("users", JSON.stringify([{ "email":"marializ@gmail.com", "password":"12345" }]))'
    )

    driver.find_element(By.ID, "email").send_keys("marializ@gmail.com")
    driver.find_element(By.ID, "password").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    alert = esperar_alert(driver)
    assert alert, "No apareció alerta de login"

    texto = alert.text.lower()
    alert.accept()

    time.sleep(1.2)
    save_shot(driver, "test_login_camino_feliz")

    assert "exitoso" in texto
    assert "personajes" in driver.current_url.lower()


def test_login_negativo(driver):
    driver.get("file:///C:/Users/maria/OneDrive/Desktop/P3/CRUD/login.html")

    driver.execute_script("localStorage.clear();")

    driver.find_element(By.ID, "email").send_keys("Lizzy@mail.com")
    driver.find_element(By.ID, "password").send_keys("wrong")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    alert = esperar_alert(driver)

    assert alert, "No apareció alerta de credenciales incorrectas"

    texto = alert.text.lower()
    alert.accept()

    save_shot(driver, "test_login_negatvo")

    assert "incorrectas" in texto
