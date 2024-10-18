import os
from utils.selenium_utils import inicializar_navegador
from ingresar_afip_service import ingresar_credenciales
from utils.afip_utils import seleccionar_servicio
from processor.contribuyentes_processor import get_contribuyentes
from processor.vep_processor import generar_vep
from utils import constants
import pandas as pd
import time

# df = pd.read_excel(
#     './data/INPUT_DATOS_VEPS.xlsx',
#     usecols='A:K',
#     skiprows=1,
#     dtype={
#         'CuitIngreso': str,
#         'CuitContribuyente': str,
#         'PERIODO FISCAL Mes': str,
#         'PERIODO FISCAL Año': str
#     }
# )

def vep_generation_service(df):
    contribuyentes = get_contribuyentes(df)

    for contribuyente in contribuyentes:
        if contribuyente.filtro == 'Si':

            resultado_proceso = ''
            cantidad_faltas_presentacion = ''

            print(f"Procesando Contribuyente: {contribuyente}")
            print(f"DatosVEP:")
            print(f"Impuesto: {contribuyente.datos_vep.tipo_pago}")
            print(f"Periodo: {contribuyente.datos_vep.periodo_fiscal}-{contribuyente.datos_vep.anio_fiscal}")
            print(f"Categoria: {contribuyente.datos_vep.categoria}")

            # Creamos la ubicacion temporal para la corrida.
            if not os.path.exists(constants.UBICACION_TEMPORAL):
                os.makedirs(constants.UBICACION_TEMPORAL)

            driver = inicializar_navegador()
            ingresar_credenciales(driver, contribuyente)
            print("Login exitoso.")
            seleccionar_servicio(driver, 'Presentación de DDJJ y Pagos')
            print("Servicio seleccionado exitosamente.")
            generar_vep(driver, contribuyente)

            time.sleep(1)
            
            driver.close()
