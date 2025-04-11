import os
from src.inicializar_navegador import inicializar_navegador
from src.ingresar_afip import ingresar_credenciales
from src.seleccionar_servicio import seleccionar_servicio
from src.obtener_contribuyentes_a_procesar import get_contribuyentes
from src.generar_vep import generar_vep
from utils import constants
import pandas as pd
import time

df = pd.read_excel(
    './data/INPUT_DATOS_VEPS.xlsx',
    usecols='A:L',
    skiprows=1,
    dtype={
        'CuitIngreso': str,
        'CuitContribuyente': str,
        'PERIODO FISCAL Mes': str,
        'PERIODO FISCAL Año': str,
        'CUR': str
    }
)

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
        seleccionar_servicio(driver)
        generar_vep(driver, contribuyente)

        time.sleep(1)

        driver.close()
