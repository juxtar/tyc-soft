class Singleton:
    """Implementacion de una clase singleton"""

    instancia = None

    @classmethod
    def get_instance(cls):
        """Devuelve una unica instancia de la clase"""
        if cls.instancia is None:
            cls.instancia = cls()
        return cls.instancia