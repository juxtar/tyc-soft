class NombreExistente(Exception):
    """Excepcion para manejar errores de nombre ya existente"""
    def __init__(self, mensaje):
        self.mensaje = mensaje
    def __str__(self):
        return repr(self.mensaje)


class FaltaDeDatos(Exception):
    """Excepcion para manejar errores de falta de datos"""
    def __init__(self, mensaje):
        self.mensaje = mensaje
    def __str__(self):
        return repr(self.mensaje)
