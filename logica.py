from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from almacenamiento import *


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


class GestorBaseDeDatos(Singleton):
    """Realiza tareas correspondientes a las interacciones con la Base de Datos"""
    def __init__(self):
        engine = create_engine('sqlite:///prueba.db', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def agregar_competencia(self, competencia):
        self.session.add(competencia)
        self.session.commit()

    def agregar_participante(self, participante):
        self.session.add(participante)
        self.session.commit()

    def listar_participantes(self, id_competencia):
        return self.session.query(Participante).filter(Participante.id_competencia == id_competencia).all()

    def listar_competencias(self, id_competencia= None, nombre = None, id_usuario = None, deporte = None, modalidad = None, estado = None):
        query = self.session.query(Competencia)
        if id_competencia is not None:
            query = query.filter(Competencia.id == id_competencia)
            return query.one()
        if nombre is not None:
            query = query.filter(Competencia.nombre == nombre)
        if id_usuario is not None:
            query = query.filter(Competencia.id_usuario == id_usuario)
        if deporte is not None:
            query = query.filter(Competencia.deporte == deporte)
        if modalidad is not None:
            query = query.filter(Competencia.modalidad == modalidad)
        if estado is not None:
            query = query.filter(Competencia.estado == estado)
        return query.all()

    def listar_lugar(self, id_usuario):
        return self.session.query(Lugar).filter(Lugar.id_usuario == id_usuario).all()
        pass
