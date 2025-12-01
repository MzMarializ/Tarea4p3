import time
import pytest
from selenium.webdriver.common.by import By
from selenium_tests.utils.driver import create_driver


@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


def test_crear_personaje(driver):
    driver.get("file:///C:/Users/maria/OneDrive/Desktop/P3/CRUD/personajes.html")

    driver.find_element(By.ID, "nombre").send_keys("Robin")
    driver.find_element(By.ID, "rol").send_keys("Estratégico")
    driver.find_element(By.ID, "nivel").send_keys("8")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(1)
    driver.save_screenshot("screenshots/crear_personaje.png")

    filas = driver.find_elements(By.CSS_SELECTOR, "#tablaPersonajes tbody tr")
    assert len(filas) >= 1


def test_crear_personaje_negativo(driver):
    driver.get("file:///C:/Users/maria/OneDrive/Desktop/P3/CRUD/personajes.html")

    driver.execute_script("localStorage.clear();")

    filas_antes = driver.find_elements(By.CSS_SELECTOR, "#tablaPersonajes tbody tr")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)

    filas_despues = driver.find_elements(By.CSS_SELECTOR, "#tablaPersonajes tbody tr")

    driver.save_screenshot("screenshots/crear_personaje_error.png")

    assert len(filas_antes) == len(filas_despues), "El formulario se envió aun cuando estaba vacío"




def test_editar_personaje(driver):
    driver.get("file:///C:/Users/maria/OneDrive/Desktop/P3/CRUD/personajes.html")

    driver.find_element(By.ID, "nombre").send_keys("Flash")
    driver.find_element(By.ID, "rol").send_keys("Velocidad")
    driver.find_element(By.ID, "nivel").send_keys("9")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(1)

    editar_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Editar')]")
    editar_btn.click()

    time.sleep(1)

    nombre_input = driver.find_element(By.ID, "nombre")
    nombre_input.clear()
    nombre_input.send_keys("Flash Actualizado")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(1)
    driver.save_screenshot("screenshots/editar_personaje.png")

    tabla_texto = driver.find_element(By.ID, "tablaPersonajes").text.lower()
    assert "actualizado" in tabla_texto


def test_eliminar_personaje(driver):
    driver.get("file:///C:/Users/maria/OneDrive/Desktop/P3/CRUD/personajes.html")

    driver.find_element(By.ID, "nombre").send_keys("Batman")
    driver.find_element(By.ID, "rol").send_keys("Líder")
    driver.find_element(By.ID, "nivel").send_keys("10")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(1)

    eliminar_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Eliminar')]")
    eliminar_btn.click()

    time.sleep(1)
    driver.save_screenshot("screenshots/eliminar_personaje.png")


    filas = driver.find_elements(By.CSS_SELECTOR, "#tablaPersonajes tbody tr")
    assert len(filas) == 0
