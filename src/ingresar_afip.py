import time
from utils import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from models import Contribuyente


def ingresar_cuit(browser, cuit):
    cuit_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'F1:username')))
    cuit_input.clear()
    cuit_input.send_keys(cuit)
    time.sleep(0.5)
    browser.find_element(By.ID, 'F1:btnSiguiente').click()


def ingresar_password(driver, password):
    clave_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'F1:password')))
    clave_input.send_keys(password)
    time.sleep(0.5)
    driver.find_element(By.ID, 'F1:btnIngresar').click()


def ingresar_credenciales(driver, contribuyente: Contribuyente):
    try:
        driver.get(constants.URL_AFIP)
        ingresar_cuit(driver, contribuyente.usuario)
        ingresar_password(driver, contribuyente.password)
    except TimeoutException:
        print("Timed out waiting for elements to load")
    except Exception as e:
        print(f"An error occurred: {e}")


def cerrar_sesion_contribuyente(driver):

    ID_ICONO_CIERRE_SESION = 'userIconoChico'
    CERRAR_SESION_XPATH = "//button[@title='Salir']"

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # espera a que esté disponible el icono
    icono_cierre_sesion = WebDriverWait(
        driver, 10
    ).until(EC.presence_of_element_located((By.ID, ID_ICONO_CIERRE_SESION)))

    driver.execute_script("arguments[0].scrollIntoView();", icono_cierre_sesion)
    time.sleep(2)

    driver.execute_script("arguments[0].click();", icono_cierre_sesion)

    time.sleep(2)
    # espera a que esté disponible el icono
    cerrar_sesion_button = WebDriverWait(
        driver, 10
    ).until(EC.presence_of_element_located((By.XPATH, CERRAR_SESION_XPATH)))

    time.sleep(2)
    cerrar_sesion_button.click()
