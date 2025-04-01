class Cliente:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula
        self.historial_compras = []

    def agregar_factura(self, factura):
        self.historial_compras.append(factura)
