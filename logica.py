

class Singleton:
    """Implementacion de una clase singleton"""

    instancia = None

    @classmethod
    def singleton(cls):
        """Devuelve una unica instancia de la clase"""
        if cls.instancia is None:
            cls.instancia = cls()
        return cls.instancia


class GestorParticipante(Singleton):
    """Realiza tareas correspondiente al manejo de clases Participante"""
    def __init__(self):
        pass

    def nuevo_participante(self):
        pass

    def modificar_participante(self):
        pass

    def eliminar_participante(self):
        pass

    def listar_participantes(self):
        pass

    def registrar_historial(self):
        pass