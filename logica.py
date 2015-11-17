from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from almacenamiento import *
import time


class Singleton:
    """Implementacion de una clase singleton"""

    instancia = None

    @classmethod
    def get_instance(cls):
        """Devuelve una unica instancia de la clase"""
        if cls.instancia is None:
            cls.instancia = cls()
        return cls.instancia


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


class GestorCompetencia(Singleton):
    """Realiza tareas correspondiente al manejo de clases Competencia"""
    def __init__(self):
        pass
    def nueva_competencia(self, dto):
        lista_competencias = GestorBaseDeDatos.get_instance().listar_competencias()
        deporte = GestorBaseDeDatos.get_instance().listar_deportes(nombre = dto.deporte)
        lista_sedes = []
        for DTOLugares in dto.lugares:
            lugar = GestorLugar.get_instance().listar_lugar(id_lugar = DTOLugares.id)
            sede = Sede(lugar=lugar, disponibilidad=DTOLugares.disponibilidad)
            lista_sedes.append(sede)
        for competencias in lista_competencias:
            if dto.nombre == competencias.nombre:
                raise NombreExistente('Ya existe ese nombre de competencia en la base de datos.')
        if dto.tipo == 'eliminatoriasimple':
            competencia_new= CompetenciaEliminatoriaSimple(nombre= dto.nombre, tipo_puntuacion=dto.tipo_puntuacion, cantidad_de_sets=dto.cantidad_de_sets,
            reglamento=dto.reglamento, estado='Creada', tantos_presentismo = dto.tantos_presentismo, id_usuario= dto.id_usuario,
             sedes= lista_sedes, deporte = deporte)
        elif dto.tipo == 'eliminatoriadoble':
            competencia_new= CompetenciaEliminatoriaDoble(nombre= dto.nombre, tipo_puntuacion=dto.tipo_puntuacion, cantidad_de_sets=dto.cantidad_de_sets,
            reglamento=dto.reglamento, estado='Creada', tantos_presentismo = dto.tantos_presentismo, id_usuario= dto.id_usuario,
             sedes= lista_sedes, deporte = deporte)
        else:
            competencia_new= CompetenciaLiga(nombre= dto.nombre, tipo_puntuacion=dto.tipo_puntuacion, cantidad_de_sets=dto.cantidad_de_sets,
            reglamento=dto.reglamento, estado='Creada', tantos_presentismo = dto.tantos_presentismo, id_usuario= dto.id_usuario,
            sedes= lista_sedes, puntos_por_presentarse = dto.puntos_por_presentarse, puntos_por_ganar = dto.puntos_por_ganar,
            puntos_por_empate = dto.puntos_por_empate, deporte = deporte)

        GestorBaseDeDatos.get_instance().agregar_competencia(competencia_new)
        return 1

    def eliminar_competencia(self):
        pass
    def listar_competencias(self, id_competencia = None, nombre=None, id_usuario = None, deporte = None, modalidad = None, estado = None):
        """Realiza la correspondiente busqueda de competencias, devuelve una lista de DTOs Competencias"""
        lista_dtos = []
        if id_competencia is not None:
            competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia=id_competencia)
            usuario = GestorUsuario.get_instance().obtener_usuario(competencia.id_usuario)
            if competencia.tipo =='eliminatoriasimple' or competencia.tipo =='eliminatoriadoble':
                 lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion, competencia.estado,
                    competencia.reglamento, competencia.id_usuario, usuario.nombre,
                    competencia.tipo, competencia.cantidad_de_sets, None, None, None, competencia.deporte.nombre, None, competencia.tantos_presentismo))
            else:
                lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion,
                    competencia.estado, competencia.reglamento, competencia.id_usuario, usuario.nombre, competencia.tipo, competencia.cantidad_de_sets,
                    competencia.puntos_por_presentarse, competencia.puntos_por_ganar, competencia.puntos_por_empate, competencia.deporte.nombre, None, competencia.tantos_presentismo))
        else:
            lista_competencias = GestorBaseDeDatos.get_instance().listar_competencias(nombre=nombre, id_usuario=id_usuario, deporte=deporte, modalidad=modalidad, estado=estado)
            for competencia in lista_competencias:
                usuario = GestorUsuario.get_instance().obtener_usuario(competencia.id_usuario)
                if competencia.tipo == 'eliminatoriasimple' or competencia.tipo == 'eliminatoriadoble':
                    lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion, competencia.estado, competencia.reglamento,
                        competencia.id_usuario, usuario.nombre, competencia.tipo, competencia.cantidad_de_sets, None, None, None, competencia.deporte.nombre, None, competencia.tantos_presentismo))
                else: 
                    lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion, competencia.estado, competencia.reglamento,
                        competencia.id_usuario, usuario.nombre, competencia.tipo, competencia.cantidad_de_sets, 
                        competencia.puntos_por_presentarse, competencia.puntos_por_ganar, competencia.puntos_por_empate, competencia.deporte.nombre, None, competencia.tantos_presentismo))
        return lista_dtos

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

    def nuevo_participante(self, dto):
        """Realiza las correspondientes validaciones con del participante y luego lo agrega al sistema"""
        if dto.nombre is None:
               raise FaltaDeDatos('Debe escribir un nombre para este participante')
        if dto.correo_electronico is None:
                raise FaltaDeDatos('Debe escribir un correo electronico para este participante')
        competencia = GestorBaseDeDatos.get_instance().listar_competencias(nombre = dto.competencia)
        lista_participantes = GestorBaseDeDatos.get_instance().listar_participantes(id_competencia = competencia.id)
        for participante in lista_participantes:
            if participante.nombre == dto.nombre:
                raise NombreExistente('Este participante ya existe en esta competencia')
            if participante.correo_electronico == dto.correo_electronico:
                raise NombreExistente('Este correo electronico ya existe en esta competencia')
        part = Participante(nombre=dto.nombre, correo_electronico = dto.correo_electronico)
        GestorBaseDeDatos.get_instance().agregar_participante(part)
        """historial = HistorialNombres(nombre = part.nombre, fecha = time.strftime("%d/%m/%y"), id_participante = part.id)
        GestorBaseDeDatos.get_instance().agregar_historial(historial= historial)
        competencia.estado == 'Creada'
        GestorBaseDeDatos.get_instance().modificar_competencia()"""
        

    def modificar_participante(self):
        pass

    def eliminar_participante(self):
        pass

    def listar_participantes(self, id_competencia= None):
        lista_participantes = GestorBaseDeDatos.get_instance().listar_participantes(id_competencia= id_competencia)
        lista = []
        competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia = id_competencia)
        for participante in lista_participantes:
            historial = GestorBaseDeDatos.get_instance().listar_historial(participante.id)
            nombresEnHistorial = []
            for nombre in historial:
                nombresEnHistorial.add(historial.nombre)
            dto_participante = DTOParticipante(participante.id, participante.nombre, participante.correo_electronico, competencia.nombre, nombresEnHistorial, participante.imagen)
            lista.add(dto_participante)
        return lista

    def registrar_historial(self):
        pass


class GestorBaseDeDatos(Singleton):
    """Realiza tareas correspondientes a las interacciones con la Base de Datos"""
    def __init__(self):
        engine = create_engine('sqlite:///pyged.db', echo=True, convert_unicode=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def agregar_usuario(self, usuario):
        self.session.add(usuario)
        self.session.commit()

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

    def listar_participantes(self, id_competencia):
        return self.session.query(Participante).filter(Participante.id_competencia == id_competencia).all()

    def listar_competencias(self, id_competencia= None, nombre = None, id_usuario = None, deporte = None, modalidad = None, estado = None):
        query = self.session.query(Competencia)
        if id_competencia is not None:
            query = query.filter(Competencia.id == id_competencia)
            return query.one()
        if nombre is not None:
            query = query.filter(Competencia.nombre == nombre)
            return query.one()
        if id_usuario is not None:
            query = query.filter(Competencia.id_usuario == id_usuario)
        if deporte is not None:
            query = query.join(Deporte).filter(Deporte.nombre == deporte)
        if modalidad is not None:
            query = query.filter(Competencia.tipo == modalidad)
        if estado is not None:
            query = query.filter(Competencia.estado == estado)
        return query.all()

    def listar_lugar(self, id_usuario= None, id_lugar = None):
        query = self.session.query(Lugar)
        if id_lugar is not None:
            query = query.filter(Lugar.id == id_lugar)
            return query.one()
        elif id_usuario is not None:
            query = query.filter(Lugar.id_usuario == id_usuario)
            return query.all()


class GestorUsuario(Singleton):
    """Realiza tareas correspondiente al manejo de clases Usuario"""
    def __init__(self):
        pass
    def obtener_usuario(self, id_usuario):
        """Obtiene, teniendo un id de usuario, el objeto Usuario correspondiente a este id"""
        user = GestorBaseDeDatos.get_instance().listar_usuario(id_usuario)
        return user


class GestorLugar(Singleton):
    """Realiza tareas correspondientes al manejo de clases Lugar"""
    def __init__(self):
        pass

    def listar_lugar(self, id_usuario = None, id_lugar = None):
        if id_lugar is not None:
           return GestorBaseDeDatos.get_instance().listar_lugar(id_lugar=id_lugar)
        if id_usuario is not None:
            lista_dto = []
            lista_lugares = GestorBaseDeDatos.get_instance().listar_lugar(id_usuario= id_usuario)
            for lugar in lista_lugares:
                dto = DTOLugar(lugar.id, lugar.nombre, lugar.descripcion, None)
                lista_dto.append(dto)
            return lista_dto


class DTOParticipante:
    """Almacena informacion para la transfrencia de datos de una competencia"""
    def __init__(self, id_participante, nombre, correo_electronico, competencia, historial_nombre, imagen):
        self.id = id_participante
        self.nombre = nombre 
        """Nombre del participante"""
        self.correo_electronico = correo_electronico 
        """Correo electronico del participante"""
        self.competencia = competencia 
        """Nombre de la competencia"""
        self.historial_nombre = historial_nombre 
        """Lista de nombres (strings)"""
        self.imagen = imagen 
        """Imagen"""

    def __repr__(self):
        return '<DTOParticipante(%r, %r)' %(self.nombre, self.correo_electronico)


class DTOCompetencia:
    """Almacena informacion para la transfrencia de datos de una competencia"""
    def __init__(self, id_competencia, nombre, tipo_puntuacion, estado, reglamento,
                id_usuario, nombre_usuario, tipo, cantidad_de_sets, puntos_por_presentarse, puntos_por_ganar, puntos_por_empate, deporte, lugares, tantos_presentismo):
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
        self.deporte = deporte
        self.lugares = lugares
        self.tantos_presentismo = tantos_presentismo
        
    def __repr__(self):
        return '<DTOCompetencia(%r, %r, %r)>' % (self.nombre, self.estado, self.tipo)


class DTOLugar:
    """Almacena informacion para la transfrencia de datos de un lugar"""
    def __init__(self, id_lugar, nombre, descripcion, disponibilidad):
        self.id = id_lugar
        self.nombre = nombre
        self.descripcion = descripcion
        self.disponibilidad = disponibilidad
    
    def __repr__(self):
        return '<DTOLugar(%r, %r, %r)>' % (self.nombre, self.descripcion, self.disponibilidad)
