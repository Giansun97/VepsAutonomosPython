import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import random


def generar_vep(driver, contribuyente):
    _cambiar_pestana(driver)

    aceptar_importante(driver)
    click_nuevo_vep(driver)
    seleccionar_cuit_contribuyente(driver, contribuyente)
    seleccionar_grupo_tipo_pago(driver, contribuyente.datos_vep.grupo_de_tipo_pago)
    seleccionar_tipo_pago(driver, contribuyente.datos_vep.tipo_pago)
    click_siguiente(driver)
    print('Seleccionando periodo ...')
    seleccionar_periodo_fiscal(driver, contribuyente.datos_vep.periodo_fiscal)

    print('Seleccionando año ...')
    seleccionar_anio_fiscal(driver, contribuyente.datos_vep.anio_fiscal)

    print('Seleccionando categoria ...')
    seleccionar_categoria(driver, contribuyente.datos_vep.categoria)

    print('Click siguiennte ...')
    click_siguiente_datos_periodo(driver)

    print('Click siguiennte dos ...')
    click_siguiente_dos(driver)

    print('Seleccionando medio de pago ...')
    seleccionar_medio_de_pago(driver, contribuyente.datos_vep.medio_de_pago)

    print('Confirmando VEP ...')
    # confirmar vep
    generar_vep_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceptar']"))
    )
    generar_vep_button.click()

    print('Descargando VEP Generado ...')
    # descargar pdf
    export_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='picture_as_pdf']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", export_link)
    time.sleep(random.randint(1, 2))
    export_link.click()



def click_siguiente_dos(driver):
    XPATH_SIGUIENTE = ("//button[contains(@class, 'btn') and contains(@class, 'e-button') and contains(@class, "
                       "'btn-primary') and normalize-space()='Siguiente']")

    wait = WebDriverWait(driver, 10)

    while True:
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SIGUIENTE)))
            time.sleep(random.randint(1, 2))
            button.click()
            break  # Si el clic es exitoso, salir del bucle

        except StaleElementReferenceException:
            # Sí ocurre la excepción, simplemente reintentar
            pass


def seleccionar_medio_de_pago(driver, medio_de_pago):

    ID_MEDIO_DE_PAGO = medio_de_pago.split(" - ")[0]

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.ID, ID_MEDIO_DE_PAGO)))
    driver.execute_script("arguments[0].scrollIntoView();", button)

    time.sleep(random.randint(1, 2))
    
    button.click()


def seleccionar_periodo_fiscal(driver, periodo_fiscal):
    label_xpath = "//label[text()='PERIODO FISCAL Mes']"
    dropdown_xpath = ".//following-sibling::div//input[@class='multiselect-search']"
    option_xpath = ".//following-sibling::div//ul[contains(@class, 'multiselect-options')]//li"

    wait = WebDriverWait(driver, 10)
    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()
    # dropdown_input.send_keys(periodo_fiscal)

    # Corregir la expresión XPath para encontrar los elementos li dentro del dropdown
    dropdown_options = dropdown_input.find_elements(By.XPATH, option_xpath)

    for option in dropdown_options:

        if option.text == periodo_fiscal:
            time.sleep(random.randint(1, 2))
            try:
                option.click()
                break

            except Exception:
                print("El periodo esta seleccionado por defecto.")
                dropdown_input.send_keys(Keys.TAB)
                break


def seleccionar_anio_fiscal(driver, anio_fiscal):
    label_xpath = "//label[text()='PERIODO FISCAL Año']"
    dropdown_xpath = ".//following-sibling::div//input[@class='multiselect-search']"
    option_xpath = ".//following-sibling::div//ul[contains(@class, 'multiselect-options')]//li"

    wait = WebDriverWait(driver, 10)
    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    dropdown_options = dropdown_input.find_elements(By.XPATH, option_xpath)

    for option in dropdown_options:

        if option.text == anio_fiscal:
            time.sleep(random.randint(1, 2))
            try:

                option.click()
                break

            except Exception:
                print("El Año esta seleccionado por defecto.")
                dropdown_input.send_keys(Keys.TAB)
                break


def seleccionar_categoria(driver, categoria):
    label_xpath = "//label[text()='CATEGORIA/CRA']"
    dropdown_xpath = ".//following-sibling::div//input[@class='multiselect-search']"
    option_xpath = ".//following-sibling::div//ul[contains(@class, 'multiselect-options')]//li"

    wait = WebDriverWait(driver, 10)
    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    dropdown_options = dropdown_input.find_elements(By.XPATH, option_xpath)

    for option in dropdown_options:

        if option.text == categoria:
            time.sleep(random.randint(1, 2))
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                time.sleep(2)
                option.click()
                break

            except Exception:
                print("La categoria esta seleccionada por defecto.")
                dropdown_input.send_keys(Keys.TAB)
                break


def click_siguiente_datos_periodo(driver):
    XPATH_SIGUIENTE = "//button[normalize-space()='Siguiente']"

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SIGUIENTE)))

    time.sleep(random.randint(1, 3))

    button.click()


def click_siguiente(driver):
    XPATH_SIGUIENTE = "//button[normalize-space()='Siguiente']"

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SIGUIENTE)))

    time.sleep(random.randint(1, 2))

    button.click()


def seleccionar_tipo_pago(driver, tipo_pago):
    label_xpath = "//label[text()='Tipo de Pago']"
    dropdown_xpath = ".//following-sibling::div//input[@class='multiselect-search']"
    option_xpath = ".//following-sibling::div//ul[contains(@class, 'multiselect-options')]//li"

    wait = WebDriverWait(driver, 10)
    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    # Corregir la expresión XPath para encontrar los elementos li dentro del dropdown
    dropdown_options = dropdown_input.find_elements(By.XPATH, option_xpath)

    for option in dropdown_options:
        if option.text == tipo_pago:
            time.sleep(random.randint(1, 2))
            option.click()
            break


def seleccionar_grupo_tipo_pago(driver, grupo_tipo_pago):
    label_xpath = "//label[text()='Grupos de Tipos de Pagos']"
    dropdown_xpath = ".//following-sibling::div//input[@class='multiselect-search']"
    option_xpath = ".//following-sibling::div//ul[contains(@class, 'multiselect-options')]//li"

    wait = WebDriverWait(driver, 10)
    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)

    time.sleep(random.randint(1, 2))
    dropdown_input.click()

    # Corregir la expresión XPath para encontrar los elementos li dentro del dropdown
    dropdown_options = dropdown_input.find_elements(By.XPATH, option_xpath)

    for option in dropdown_options:
        if option.text == grupo_tipo_pago:
            time.sleep(random.randint(1, 2))
            option.click()
            break


def seleccionar_cuit_contribuyente(driver, contribuyente):
    XPATH_DROPDOWN_INPUT = "//input[@class='multiselect-search']"
    XPATH_DROP_DOWN_OPTIONS = "//ul[contains(@class, 'multiselect-options')]//li"

    # Espera hasta que el campo de entrada del menú desplegable esté presente
    wait = WebDriverWait(driver, 10)
    dropdown_input = wait.until(EC.presence_of_element_located((By.XPATH, XPATH_DROPDOWN_INPUT)))

    time.sleep(random.randint(1, 3))

    # Haz clic en el campo de entrada para expandir el menú desplegable
    dropdown_input.click()

    # Espera hasta que los elementos del menú desplegable estén presentes
    dropdown_options = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH_DROP_DOWN_OPTIONS)))

    # Busca y selecciona el elemento deseado del menú desplegable
    for option in dropdown_options:
        if option.text == f"{contribuyente.cuit_contribuyente}":
            time.sleep(random.randint(1, 3))
            option.click()
            break


def aceptar_importante(driver):
    XPATH_ACEPTAR = "//button[@title='Aceptar']"

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_ACEPTAR)))

    time.sleep(random.randint(1, 3))

    button.click()


def click_nuevo_vep(driver):
    XPATH_LINK = "//a[@href='#/pago/nuevo-vep']"

    wait = WebDriverWait(driver, 10)
    link = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_LINK)))

    time.sleep(random.randint(1, 3))

    # Haz clic en el enlace
    link.click()


def _cambiar_pestana(driver):
    window_handles = driver.window_handles
    new_popup_handle = window_handles[-1]
    time.sleep(random.randint(1, 3))
    driver.switch_to.window(new_popup_handle)
    time.sleep(random.randint(1, 3))
