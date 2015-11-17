from main import Singleton
from gestorbasededatos import GestorBaseDeDatos
from gestorusuario import GestorUsuario
from gestorlugar import GestorLugar
from excepciones import NombreExistente
from dtos import DTOCompetencia
from pyged.almacenamiento import *

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
