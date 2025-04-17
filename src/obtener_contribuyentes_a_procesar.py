from models.Contribuyente import Contribuyente, DatosVep


def get_contribuyentes(df):
    contribuyentes = []

    if df is not None:
        for index, row in df.iterrows():
            datos_vep = DatosVep(
                grupo_de_tipo_pago=row['Grupo de Tipos de Pagos'],
                tipo_pago=row['Tipo de Pago'],
                periodo_fiscal=row['PERIODO FISCAL Mes'],
                anio_fiscal=row['PERIODO FISCAL Año'],
                categoria=row['CATEGORIA/CRA'],
                medio_de_pago=row['Medio de Pago']
            )

            # Crear un objeto Contribuyente para cada fila
            contribuyente = Contribuyente(
                cuit_contribuyente=str(row['CuitContribuyente']),
                cliente=row['Nombre'],
                filtro=row['Procesar?'],
                mail=row['MailCliente'],
                envio_mail=row['Enviar Mail?'],
                usuario=row['CuitIngreso'],
                password=row['Clave'],
                cur=row['CUR'],
                datos_vep=datos_vep
            )

            contribuyentes.append(contribuyente)

    return contribuyentes
