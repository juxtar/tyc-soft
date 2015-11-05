from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from almacenamiento import *


class Singleton:
    """Implementacion de una clase singleton"""

    instancia = None

    @classmethod
    def get_instance(cls):
        """Devuelve una unica instancia de la clase"""
        if cls.instancia is None:
            cls.instancia = cls()
        return cls.instancia

class GestorCompetencia(Singleton):
    """Realiza tareas correspondiente al manejo de clases Participante"""
    def __init__(self):
        pass
    def nueva_competencia(self, nombre = None, deporte = None, lugares = None, ):
        pass
    def eliminar_competencia(self):
        pass
    def listar_competencias(self, id_competencia = None, nombre=None, id_usuario = None, deporte = None, modalidad = None, estado = None):
        """Realiza la correspondiente busqueda de competencias, devuelve una lista de DTOs Competencias"""
        lista_DTOs = []
        if id_competencia is not None:
            competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia=id_competencia)
            usuario = GestorUsuario.get_instance().obtener_usuario(lista_competencia.id_usuario)
            if competencia.tipo =='eliminatoriasimple' or competencia.tipo =='eliminatoriadoble':
                 lista_DTOs.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion, competencia.estado, 
                    competencia.reglamento, competencia.id_usuario, usuario.nombre,
                    competencia.tipo, competencia.cantidad_de_sets, None, None, None))
            else:
                lista_DTOs.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion, 
                    competencia.estado, competencia.reglamento, competencia.dada_de_baja, competencia.fecha_de_baja, 
                    competencia.id_usuario, usuario.nombre, competencia.tipo, competencia.cantidad_de_sets, 
                    competencia.puntos_por_set, competencia.puntos_por_ganar, competencia.puntos_por_empate))
        else:
            lista_competencias = GestorBaseDeDatos.get_instance().listar_competencias(nombre=nombre, id_usuario=id_usuario, deporte=deporte, modalidad=modalidad, estado=estado)
            for competencia in lista_competencias:
                usuario = GestorUsuario.get_instance().obtener_usuario(competencia.id_usuario)
                if competencia.tipo == 'eliminatoriasimple' or competencia.tipo == 'eliminatoriadoble':
                    lista_DTOs.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion, competencia.estado, competencia.reglamento, 
                        competencia.id_usuario, usuario.nombre, competencia.tipo, competencia.cantidad_de_sets, None, None, None))
                else: 
                    lista_DTOs.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion, competencia.estado, competencia.reglamento, 
                        competencia.id_usuario, usuario.nombre, competencia.tipo, competencia.cantidad_de_sets, 
                        competencia.puntos_por_set, competencia.puntos_por_ganar, competencia.puntos_por_empate))
        return lista_DTOs

    def generar_fixture(self):
        pass
    def modificar_competencia(self):
        pass
    def generar_tabla_posiciones(self):
        pass
    def eliminar_fiture(self):
        pass

class GestorParticipante(Singleton):
    """Realiza tareas correspondiente al manejo de clases Participante"""
    def __init__(self):
        pass

    def nuevo_participante(self, DTOParticipante):
        """Realiza las correspondientes validaciones con del participante y luego lo agrega al sistema"""

        lista_participantes = GestorBaseDeDatos.get_instance().listar_participantes(id_competencia = DTOParticipante.id_competencia)
        if DTOParticipante.nombre == None:
                agregar_cuadro_error.get_instance().mostrar_error(mensajes = 'Debe escribir un nombre para este participante')
        if DTOParticipante.correo_electronico == None:
                agregar_cuadro_error.get_instance().mostrar_error(mensajes = 'Debe escribir un correo electronico para este participante')
        for i in lista_participantes:
            if i.nombre == DTOParticipante.nombre:
                agregar_cuadro_error.get_instance().mostrar_error(mensajes = 'Este participante ya existe en esta competencia')
            if i.correo_electronico == DTOParticipante.correo_electronico:
                agregar_cuadro_error.get_instance().mostrar_error(mensajes = 'Este correo electronico ya existe en esta competencia')
        part = Participante(nombre=DTOParticipante.nombre, correo_electroonico = DTOParticipante.correo_electroonico, imagen = DTOParticipante.imagen)
        GestorBaseDeDatos.get_instance().agregar_participante(part)
        

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

    def agregar_usuario(self, usuario):
        self.session.add(usuario)
        self.session.commit()

    def agregar_competencia(self, competencia):
        self.session.add(competencia)
        self.session.commit()

    def agregar_participante(self, participante):
        self.session.add(participante)
        self.session.commit()

    def modificar_competencia(self, competencia):
        self.session.commit()

    def listar_usuario(self, id_usuario):
        query = self.session.query(Usuario)
        query = query.filter(Usuario.id == id_usuario)
        return query.one()

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

class DTOCompetencia:
    """Almacena informacion para la transfrencia de datos de una competencia"""
    def __init__(self, id_competencia, nombre, tipo_puntuacion, estado, reglamento,
                id_usuario, nombre_usuario, tipo, cantidad_de_sets, puntos_por_presentarse, puntos_por_ganar, puntos_por_empate):
        self.id = id_competencia
        self.nombre = nombre
        self.tipo_puntuacion = tipo_puntuacion
        self.estado = estado
        self.reglamento = reglamento
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.tipo = tipo
        self.cantidad_de_sets = cantidad_de_sets
        self.puntos_por_presentarse = puntos_por_presentarse
        self.puntos_por_ganar = puntos_por_ganar
        self.puntos_por_empate = puntos_por_empate
        
    def __repr__(self):
        return '<DTOCompetencia(%r, %r, %r)>' % (self.nombre, self.estado, self.tipo)

class GestorUsuario(Singleton):
    """Realiza tareas correspondiente al manejo de clases Usuario"""
    def __init__(self):
        pass
    def obtener_usuario(self, id_usuario):
        """Obtiene, teniendo un id de usuario, el objeto Usuario correspondiente a este id"""
        user = GestorBaseDeDatos.get_instance().listar_usuario(id_usuario)
        return user
