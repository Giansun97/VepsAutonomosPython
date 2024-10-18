import streamlit as st
import pandas as pd
import time
from src.vep_generation_service import vep_generation_service

# Configuración de la página
st.set_page_config(page_title="Generación Automática de VEPS", page_icon="📊", layout="wide")

# Función para cargar CSS personalizado
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Cargar CSS personalizado
local_css("style.css")

# Barra lateral
with st.sidebar:
    # st.image("logo.png", width=200)
    st.title("Configuración")
    
    # Opciones de configuración (puedes agregar más según sea necesario)
    show_preview = st.checkbox("Mostrar vista previa de datos", value=True)
    max_rows = st.slider("Número máximo de filas en la vista previa", 5, 50, 10)

# Contenido principal
st.title('Generación Automática de VEPS')

# Instrucciones
with st.expander("Instrucciones de uso", expanded=False):
    st.write("""
    1. Cargue un archivo Excel con los datos necesarios.
    2. Revise la vista previa de los datos (si está habilitada).
    3. Haga clic en 'Generar VEPS' para iniciar el proceso.
    4. Espere a que se complete la generación de VEPS.
    5. Descargue los VEPS generados.
    """)

# Cargar el archivo Excel
uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(
            uploaded_file,
            usecols='A:K',
            skiprows=1,
            dtype={
                'CuitIngreso': str,
                'CuitContribuyente': str,
                'PERIODO FISCAL Mes': str,
                'PERIODO FISCAL Año': str
            }
        )

        df_filtrado = df[df['Procesar?'] == 'Si']

        # Mostrar una vista previa de los datos
        if show_preview:
            st.subheader('Vista previa de los datos cargados')
            st.dataframe(df_filtrado.head(max_rows), use_container_width=True)

        # Botón para ejecutar el scraper
        if st.button("Generar VEPS", key="generate_veps"):
            with st.spinner("Generando VEPS..."):
                # Barra de progreso
                progress_bar = st.progress(0)
                
                # Aquí se llamaría la función del scraper usando los datos del DataFrame df
                total_rows = len(df_filtrado)
                for i, row in df_filtrado.iterrows():
                    # Simular el proceso de generación de VEP (reemplazar con la llamada real)
                    time.sleep(0.1)
                    # Actualizar la barra de progreso
                    progress_bar.progress((i + 1) / total_rows)

                # Llamada real al servicio de generación de VEP
                vep_generation_service(df_filtrado)
                
            st.success("VEPS generados exitosamente.")

            # Aquí se puede agregar la lógica para descargar los VEPS generados
            # st.download_button(
            #     label="Descargar VEPS generados",
            #     data="datos_de_veps_generados.zip",  # Reemplazar con los datos reales
            #     file_name="veps_generados.zip",
            #     mime="application/zip"
            # )

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info('Por favor, carga un archivo Excel con los datos necesarios.')

# Pie de página
st.markdown("---")
st.markdown("Desarrollado por Gian Franco Lorenzo Patti| © 2023")