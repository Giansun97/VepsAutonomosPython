class Contribuyente:
    def __init__(self, cuit_contribuyente, cliente, usuario, password, filtro, datos_vep):

        self.cuit_contribuyente = cuit_contribuyente
        self.cliente = cliente
        self.usuario = usuario
        self.password = password
        self.filtro = filtro
        self.datos_vep = datos_vep

    def __str__(self):
        return f"CUIT: {self.cuit_contribuyente}, Cliente: {self.cliente}"


class DatosVep:
    def __init__(self, grupo_de_tipo_pago, tipo_pago, periodo_fiscal, anio_fiscal, categoria, medio_de_pago):

        self.grupo_de_tipo_pago = grupo_de_tipo_pago
        self.tipo_pago = tipo_pago
        self.periodo_fiscal = periodo_fiscal
        self.anio_fiscal = anio_fiscal
        self.categoria = categoria
        self.medio_de_pago = medio_de_pago
