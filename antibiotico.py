from modelo.producto import Producto

class Antibiotico(Producto):
    def __init__(self, nombre, precio, dosis, tipo_animal):
        super().__init__(nombre, precio)
        self.dosis = dosis
        self.tipo_animal = tipo_animal
