from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils import constants
import os


def configurar_opciones_chrome(contribuyente):
    
    # Crear la carpeta de descargas si no existe
    vep_folder = os.path.join(constants.UBICACION_TEMPORAL, "veps")
    if not os.path.exists(vep_folder):
        os.makedirs(vep_folder)
    
    # Ruta absoluta para Chrome
    ubicacion_temporal = os.path.abspath(vep_folder)
    print(f"Configurando directorio de descargas de Chrome: {ubicacion_temporal}")
    
    if contribuyente and hasattr(contribuyente, 'cuit'):
        contribuyente_folder = os.path.join(ubicacion_temporal, f"{contribuyente.cuit_contribuyente}")
        if not os.path.exists(contribuyente_folder):
            os.makedirs(contribuyente_folder)
        ubicacion_temporal = contribuyente_folder
        print(f"Configurando directorio específico para contribuyente: {ubicacion_temporal}")
    
    chrome_options = webdriver.ChromeOptions()

    download_prefs = {
        "download.default_directory": ubicacion_temporal,
        "download.prompt_for_download": False,
        "profile.managed_default_content_settings.images": 2,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        'build': 'Python Sample Build',
    }

    if contribuyente:
        # Crear subcarpeta específica para este contribuyente si deseamos más organización
        contribuyente_folder = os.path.join(ubicacion_temporal, f"{contribuyente.cuit_contribuyente}")
        if not os.path.exists(contribuyente_folder):
            os.makedirs(contribuyente_folder)
        download_prefs["download.default_directory"] = contribuyente_folder
    
    chrome_options.add_experimental_option("prefs", download_prefs)
    chrome_options.add_argument("--start-maximized")
    
    return chrome_options


def inicializar_navegador(contribuyente):
    chrome_options = configurar_opciones_chrome(contribuyente)
    service = Service(executable_path="chromedriver.exe")
    # driver = webdriver.Chrome(service=service, options=chrome_options)    
    driver = webdriver.Chrome(service=service, options=chrome_options) 
    return driver
