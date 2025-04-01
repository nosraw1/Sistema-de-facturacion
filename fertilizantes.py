from modelo.producto import Producto

class ControlFertilizantes(Producto):
    def __init__(self, nombre, precio, registro_ica, frecuencia_aplicacion, fecha_ultima_aplicacion):
        super().__init__(nombre, precio)
        self.registro_ica = registro_ica
        self.frecuencia_aplicacion = frecuencia_aplicacion
        self.fecha_ultima_aplicacion = fecha_ultima_aplicacion
