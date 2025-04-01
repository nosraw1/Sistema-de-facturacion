import datetime

class Factura:
    def __init__(self, cliente):
        self.cliente = cliente
        self.fecha = datetime.datetime.now()
        self.productos = []
        self.total = 0

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.total += producto.precio

    def __str__(self):
        return f"Factura de {self.cliente.nombre} - Total: ${self.total}"
