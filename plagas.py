from modelo.producto import Producto

class ControlPlagas(Producto):
    def __init__(self, nombre, precio, registro_ica, frecuencia_aplicacion, periodo_carencia):
        super().__init__(nombre, precio)
        self.registro_ica = registro_ica
        self.frecuencia_aplicacion = frecuencia_aplicacion
        self.periodo_carencia = periodo_carencia
