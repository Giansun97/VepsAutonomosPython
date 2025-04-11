import time
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

    seleccionar_periodo_fiscal(driver, contribuyente.datos_vep.periodo_fiscal)
    seleccionar_anio_fiscal(driver, contribuyente.datos_vep.anio_fiscal)

    if contribuyente.datos_vep.grupo_de_tipo_pago == "Autonomo":
        seleccionar_categoria(driver, contribuyente.datos_vep.categoria)

    time.sleep(0.5)
    try:
        # Hacer clic en un área vacía para cerrar cualquier menú abierto
        actions = ActionChains(driver)
        actions.move_by_offset(10, 10).click().perform()
        actions.reset_actions()
    except Exception:
        pass

    if contribuyente.datos_vep.grupo_de_tipo_pago in ["Monotributo", "Monotributo Unificado"]:
        if hasattr(contribuyente, 'cur') and contribuyente.cur:
            ingresar_cur(driver, contribuyente.cur)

    click_siguiente_datos_periodo(driver)

    click_siguiente_dos(driver)

    seleccionar_medio_de_pago(driver, contribuyente.datos_vep.medio_de_pago)

    # confirmar vep
    generar_vep_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceptar']"))
    )
    generar_vep_button.click()

    # descargar pdf
    export_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='picture_as_pdf']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", export_link)
    time.sleep(random.randint(1, 2))
    driver.execute_script("arguments[0].click();", export_link)


def ingresar_cur(driver, cur):
    """
    Función para ingresar el CUR en el campo correspondiente,
    manejando elementos interceptados
    
    Args:
        driver: El WebDriver de Selenium
        cur (str): El CUR a ingresar
    """
    try:
        # Esperar a que cualquier menú desplegable o diálogo se cierre
        time.sleep(1)
        
        # Intentar cerrar cualquier elemento interceptor (como menús desplegables)
        try:
            # Hacer clic en un área vacía para cerrar cualquier menú abierto
            actions = ActionChains(driver)
            actions.move_by_offset(10, 10).click().perform()
            actions.reset_actions()
            time.sleep(0.5)
        except Exception:
            pass
        
        # Esperar a que el campo esté disponible
        wait = WebDriverWait(driver, 10)
        xpath = "//div[./label[text()='CUR']]//input[@class='e-input form-control']"
        campo_cur = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Intentar hacer scroll al elemento para asegurarnos de que es visible
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", campo_cur)
        time.sleep(0.5)
        
        # Intento 1: Usar ActionChains para moverse al elemento y hacer clic
        try:
            actions = ActionChains(driver)
            actions.move_to_element(campo_cur).click().send_keys(cur).perform()
            print(f"CUR {cur} ingresado correctamente con ActionChains")
            return True
        except ElementClickInterceptedException:
            print("Primer intento fallido, probando método alternativo")
        
        # Intento 2: Usar JavaScript para establecer el valor directamente
        try:
            driver.execute_script("arguments[0].value = arguments[1];", campo_cur, cur)
            print(f"CUR {cur} ingresado correctamente con JavaScript")
            return True
        except Exception as e:
            print(f"Segundo intento fallido: {str(e)}")
        
        # Intento 3: Esperar a que sea clickeable y luego hacer clic normal
        try:
            campo_cur = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            campo_cur.click()
            campo_cur.clear()
            campo_cur.send_keys(cur)
            print(f"CUR {cur} ingresado correctamente con método estándar")
            return True
        except Exception as e:
            print(f"Tercer intento fallido: {str(e)}")
            raise e
        
    except Exception as e:
        print(f"Error al ingresar el CUR: {str(e)}")
        return False


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
    seleccionar_opcion_dropdown(driver, "PERIODO FISCAL Mes", periodo_fiscal)


def seleccionar_anio_fiscal(driver, anio_fiscal):
    wait = WebDriverWait(driver, 10)

    try:
        # Paso 1: Encontrar el label que contiene "PERIODO FISCAL Año"
        label_xpath = "//label[contains(text(), 'PERIODO FISCAL Año')]"
        label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

        # Paso 2: Subir al contenedor general (ej. form-group o similar)
        container = label.find_element(By.XPATH, "./parent::div")

        # Paso 3: Hacer clic en la flechita (icono del dropdown)
        flechita = container.find_element(By.CLASS_NAME, "icon-multiselect")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", flechita)
        time.sleep(random.uniform(0.3, 0.7))
        flechita.click()
        time.sleep(random.uniform(0.4, 0.8))

        # Paso 4: Buscar las opciones
        opciones = container.find_elements(By.XPATH, ".//ul[contains(@class, 'multiselect-options')]//li")

        opciones_texto = [op.text.strip() for op in opciones]
        print(f"[DEBUG] Opciones encontradas en 'PERIODO FISCAL Año': {opciones_texto}")

        for opcion in opciones:
            if opcion.text.strip() == anio_fiscal:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcion)
                time.sleep(random.uniform(0.3, 0.7))
                opcion.click()
                print(f"[OK] Año fiscal seleccionado: {anio_fiscal}")
                return

        print(f"[WARN] No se encontró el año fiscal '{anio_fiscal}' en el dropdown.")

    except Exception as e:
        print(f"[ERROR] al seleccionar el año fiscal: {e}")


def seleccionar_opcion_dropdown(driver, label_text, valor_a_seleccionar):
    wait = WebDriverWait(driver, 10)

    try:
        # Buscar el label
        label_xpath = f"//label[contains(text(), '{label_text}')]"
        label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

        # Subir al contenedor padre del multiselect
        container = label.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-group')]")

        # Buscar y clickear la flechita dentro del contenedor
        flechita = container.find_element(By.CLASS_NAME, "icon-multiselect")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", flechita)
        time.sleep(random.uniform(0.3, 0.7))
        flechita.click()
        time.sleep(random.uniform(0.5, 1))
    except Exception as e:
        print(f"[ERROR] No se pudo abrir el dropdown de '{label_text}': {e}")
        return

    # Buscar y seleccionar la opción
    try:
        opciones_xpath = "//ul[contains(@class, 'multiselect-options')]//li"
        wait.until(EC.presence_of_all_elements_located((By.XPATH, opciones_xpath)))
        opciones = driver.find_elements(By.XPATH, opciones_xpath)

        # Modificación: Obtener el texto desde los spans dentro de los li
        opciones_texto = []
        for opcion in opciones:
            try:
                # Intentar obtener el texto del span dentro del li
                span_text = opcion.find_element(By.TAG_NAME, "span").text.strip()
                opciones_texto.append(span_text)
            except:
                # Si no hay span, usar el texto del li
                opciones_texto.append(opcion.text.strip())
                
        print(f"[DEBUG] Opciones encontradas en '{label_text}': {opciones_texto}")

        for i, opcion in enumerate(opciones):
            if opciones_texto[i] == valor_a_seleccionar:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcion)
                time.sleep(random.uniform(0.3, 0.7))
                opcion.click()
                print(f"[OK] '{label_text}' seleccionado: {valor_a_seleccionar}")
                return

        print(f"[WARN] No se encontró la opción '{valor_a_seleccionar}' en '{label_text}'")
    except Exception as e:
        print(f"[ERROR] No se pudo seleccionar '{valor_a_seleccionar}' en '{label_text}': {e}")


def seleccionar_categoria(driver, categoria):
    label_xpath = "//label[text()='CATEGORIA/CRA']"
    dropdown_xpath = ".//following-sibling::div//input[@class='multiselect-search']"
    selected_option_xpath = ".//following-sibling::div//span[@class='multiselect-single-label-text']"
    option_xpath = "//ul[contains(@class, 'multiselect-options')]//li"
    
    wait = WebDriverWait(driver, 10)
    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))
    
    # Verificar si ya está seleccionada la categoría correcta
    try:
        selected_option = label.find_element(By.XPATH, selected_option_xpath)
        if selected_option.text.strip() == categoria:
            print(f"La categoría {categoria} ya está seleccionada, continuando...")
            return
    except:
        pass  # Si no encuentra el elemento seleccionado, continuamos con la selección normal
    
    dropdown_input = label.find_element(By.XPATH, dropdown_xpath)
    
    # Hacer scroll y click con JavaScript para mayor fiabilidad
    driver.execute_script("arguments[0].scrollIntoView();", dropdown_input)
    time.sleep(random.uniform(1, 2))
    driver.execute_script("arguments[0].click();", dropdown_input)
    
    # Esperar a que aparezcan las opciones
    wait.until(EC.presence_of_element_located((By.XPATH, option_xpath)))
    
    # Obtener todas las opciones
    dropdown_options = driver.find_elements(By.XPATH, option_xpath)
    
    # Si hay muchas opciones y la categoría tiene un número conocido, podemos usar la búsqueda
    if ":" in categoria:  # Si el formato es como "103: T1 Cat III Ingresos hasta $15.000"
        category_number = categoria.split(":")[0].strip()
        dropdown_input.clear()
        dropdown_input.send_keys(category_number)
        time.sleep(1)  # Esperar a que se filtre
    
    # Buscar y seleccionar la opción correcta
    for option in dropdown_options:
        if option.text.strip() == categoria:
            try:
                # Hacer scroll hasta la opción para asegurarnos que es visible
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                time.sleep(random.uniform(0.5, 1))
                
                # Hacer click con JavaScript para mayor fiabilidad
                driver.execute_script("arguments[0].click();", option)
                time.sleep(0.5)
                print(f"Categoría {categoria} seleccionada correctamente")

                # Verificar si el desplegable sigue abierto
                try:
                    if driver.find_element(By.XPATH, "//ul[contains(@class, 'multiselect-options') and not(contains(@class, 'is-hidden'))]"):
                        dropdown_input.send_keys(Keys.ESCAPE)
                except:
                    pass  # El desplegable ya está cerrado
                return
            except Exception as e:
                print(f"Error al seleccionar la categoría: {e}")
                
    # Si llegamos aquí, no se encontró la categoría
    print(f"No se encontró la categoría: {categoria}")
    
    # Forzar el cierre del desplegable en caso de que siga abierto
    try:
        dropdown_input.send_keys(Keys.ESCAPE)
        time.sleep(0.5)
        # Hacer click fuera del dropdown para asegurarnos que se cierre
        driver.execute_script("document.body.click();")
    except:
        pass


def click_siguiente_datos_periodo(driver):
    """
    Función para hacer clic en el botón Siguiente después de ingresar los datos del período
    con manejo de elementos interceptados
    """
    try:
        # Esperamos a que el botón esté disponible
        wait = WebDriverWait(driver, 10)
        button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Siguiente']"))
        )
        
        # Scroll para asegurarnos de que el botón esté en el viewport
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(1)  # Dar tiempo para que el scroll termine
        
        # Intento 1: Clic normal
        try:
            button.click()
            return
        except Exception as e:
            print(f"No se pudo hacer clic normal en Siguiente: {str(e)}")
        
        # Intento 2: Usar ActionChains
        try:
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            return
        except Exception as e:
            print(f"No se pudo hacer clic con ActionChains en Siguiente: {str(e)}")
        
        # Intento 3: JavaScript click como último recurso
        try:
            driver.execute_script("arguments[0].click();", button)
            return
        except Exception as e:
            print(f"No se pudo hacer clic con JavaScript en Siguiente: {str(e)}")
            raise e
            
    except Exception as e:
        print(f"Error al hacer clic en Siguiente datos período: {str(e)}")
        raise e


def click_siguiente(driver):
    XPATH_SIGUIENTE = "//button[normalize-space()='Siguiente']"

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_SIGUIENTE)))

    time.sleep(random.randint(1, 3))

    button.click()


def seleccionar_tipo_pago(driver, tipo_pago):
    label_xpath = "//label[text()='Tipo de Pago']"
    dropdown_xpath = ".//following-sibling::div//span[contains(@class, 'icon-multiselect')]"
    option_xpath = "//ul[contains(@class, 'multiselect-options')]//li"

    wait = WebDriverWait(driver, 15)

    # Esperar el label y encontrar el dropdown
    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))
    dropdown_button = label.find_element(By.XPATH, dropdown_xpath)

    # Hacer scroll hasta el dropdown y hacer clic con JavaScript
    driver.execute_script("arguments[0].scrollIntoView();", dropdown_button)
    time.sleep(random.uniform(1, 2))
    driver.execute_script("arguments[0].click();", dropdown_button)

    print("Dropdown abierto, esperando opciones...")

    # Esperar que el menú esté presente antes de buscar opciones
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'multiselect-options')]")))

    # Obtener opciones globalmente
    dropdown_options = driver.find_elements(By.XPATH, option_xpath)

    if not dropdown_options:
        print("No se encontraron opciones disponibles.")
        return

    for option in dropdown_options:
        if option.text.strip() == tipo_pago:
            print(f"Seleccionando opción: {tipo_pago}")
            time.sleep(random.uniform(1, 2))
            driver.execute_script("arguments[0].click();", option)  # Click forzado con JS
            return

    print(f"No se encontró la opción: {tipo_pago}")


def seleccionar_grupo_tipo_pago(driver, grupo_tipo_pago):
    label_xpath = "//label[text()='Grupos de Tipos de Pagos']"
    dropdown_xpath = ".//following-sibling::div//span[contains(@class, 'icon-multiselect')]"
    option_xpath = "//ul[contains(@class, 'multiselect-options')]//li"

    wait = WebDriverWait(driver, 15)  # Aumenta el tiempo de espera

    label = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))

    dropdown_button = label.find_element(By.XPATH, dropdown_xpath)

    # Hacer scroll hasta el dropdown y hacer clic con JS
    driver.execute_script("arguments[0].scrollIntoView();", dropdown_button)
    time.sleep(random.uniform(1, 2))
    driver.execute_script("arguments[0].click();", dropdown_button)

    print("Dropdown abierto, esperando opciones...")

    # Asegurar que el menú esté presente
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'multiselect-options')]")))

    # Obtener opciones
    dropdown_options = driver.find_elements(By.XPATH, option_xpath)

    if not dropdown_options:
        print("No se encontraron opciones disponibles.")
        return

    for option in dropdown_options:
        if option.text.strip() == grupo_tipo_pago:
            print(f"Seleccionando opción: {grupo_tipo_pago}")
            time.sleep(random.uniform(1, 2))
            driver.execute_script("arguments[0].click();", option)
            return

    print(f"No se encontró la opción: {grupo_tipo_pago}")


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
