from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import Singleton
from pyged.almacenamiento import *


class GestorBaseDeDatos(Singleton):
    """Realiza tareas correspondientes a las interacciones con la Base de Datos"""
    def __init__(self):
        engine = create_engine('sqlite:///pyged2.db', echo=True, convert_unicode=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def agregar_usuario(self, usuario):
        self.session.add(usuario)
        self.session.commit()

    def listar_partidas(self, id_participante=None, id_partida=None):
        query = self.session.query(Partida)
        if id_partida is not None:
            query = query.filter(Partida.id == id_partida)
            return query.one()
        if id_participante is not None:
            query = query.filter(Partida.id_competidor_local == id_participante or
                             Partida.id_competidor_visitante == id_participante)
        return query.all()

    def agregar_competencia(self, competencia):
        self.session.add(competencia)
        self.session.commit()
        
    def agregar_lugar(self, lugar):
        self.session.add(lugar)
        self.session.commit()

    def agregar_deporte(self, deporte):
        self.session.add(deporte)
        self.session.commit()
    
    def listar_deportes(self, nombre= None):
        query = self.session.query(Deporte)
        if nombre is not None:
            query = query.filter(Deporte.nombre == nombre)
            return query.one()
        else:
            return query.all()
   
    def agregar_participante(self, participante):
        self.session.add(participante)
        self.session.commit()

    def agregar_historial(self, historial):
        self.session.add(historial)
        self.session.commit()

    def ver_historial(self, id_participante):
        query = self.session.query(HistorialNombres)
        query = query.filter(HistorialNombres.id_participante == id_participante)
        return query.all()

    def modificar_competencia(self):
        self.session.commit()

    def listar_usuario(self, id_usuario):
        query = self.session.query(Usuario)
        query = query.filter(Usuario.id == id_usuario)
        return query.one()

    def listar_hitorial(self, id_participante):
        query = self.session.query(HistorialNombres)
        query = query.filter(HistorialNombres.id_participante == id_participante)
        return query.all()

    def listar_participantes(self, id_competencia=None, id_participante=None):
        if id_participante is not None:
            return self.session.query(Participante).filter(Participante.id == id_participante).one()
        else:
            return self.session.query(Participante).filter(Participante.id_competencia == id_competencia).all()

    def listar_competencias(self, id_competencia= None, nombre = None, id_usuario = None, deporte = None,
                            modalidad = None, estado = None):
        query = self.session.query(Competencia)
        if id_competencia is not None:
            query = query.filter(Competencia.id == id_competencia)
            return query.one()
        if id_usuario is not None:
            query = query.filter(Competencia.id_usuario == id_usuario)
        if deporte is not None:
            query = query.join(Deporte).filter(Deporte.nombre == deporte)
        if modalidad is not None:
            query = query.filter(Competencia.tipo == modalidad)
        if estado is not None:
            query = query.filter(Competencia.estado == estado)
        if nombre is not None:
            query = query.filter(Competencia.nombre.like('%{}%'.format(nombre)))
        return query.all()

    def listar_lugar(self, id_usuario= None, id_lugar = None):
        query = self.session.query(Lugar)
        if id_lugar is not None:
            query = query.filter(Lugar.id == id_lugar)
            return query.one()
        elif id_usuario is not None:
            query = query.filter(Lugar.id_usuario == id_usuario)
            return query.all()
