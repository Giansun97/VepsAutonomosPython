import os
from src.inicializar_navegador import inicializar_navegador
from src.ingresar_afip import ingresar_credenciales
from src.seleccionar_servicio import seleccionar_servicio
from src.obtener_contribuyentes_a_procesar import get_contribuyentes
from src.generar_vep import generar_vep
from src.enviar_mail import enviar_vep_por_email
from utils import constants
import pandas as pd
import time

df = pd.read_excel(
    './data/INPUT_DATOS_VEPS.xlsx',
    usecols='A:N',
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

        # # Creamos la ubicacion temporal para la corrida.
        # if not os.path.exists(constants.UBICACION_TEMPORAL):
        #     os.makedirs(constants.UBICACION_TEMPORAL)

        driver = inicializar_navegador(contribuyente)
        ingresar_credenciales(driver, contribuyente)
        seleccionar_servicio(driver)
        file_path = generar_vep(driver, contribuyente)

        if file_path and contribuyente.envio_mail == 'Si':
            enviar_vep_por_email(file_path, contribuyente)
        else:
            if not file_path:
                print("No se pudo enviar el correo porque no se encontró el archivo PDF")
            

        time.sleep(1)

        driver.close()
