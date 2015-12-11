from main import Singleton
from excepciones import FaltaDeDatos, NombreExistente
from gestorbasededatos import GestorBaseDeDatos
from dtos import DTOParticipante
from pyged.almacenamiento import *
from datetime import *


class GestorParticipante(Singleton):
    """Realiza tareas correspondiente al manejo de clases Participante"""
    def __init__(self):
        pass

    def nuevo_participante(self, dto):
        """Realiza las correspondientes validaciones con del participante y luego lo agrega al sistema"""
        if dto.nombre in [None, '']:
                raise FaltaDeDatos('Debe escribir un nombre para este participante.')
        if dto.correo_electronico in [None, '']:
                raise FaltaDeDatos('Debe escribir un correo electronico para este participante.')
        competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia = dto.id_competencia)
        if competencia.estado in ['En Disputa', 'Finalizada']:
            raise FaltaDeDatos('No se puede agregar participante a una competencia a la que ya se le agregaron resultados.')
        for participante in competencia.participantes:
            if participante.nombre == dto.nombre:
                raise NombreExistente('Este participante ya existe en esta competencia.')
            if participante.correo_electronico == dto.correo_electronico:
                raise NombreExistente('Este correo electronico ya existe en esta competencia.')
        part = Participante(nombre=dto.nombre, correo_electronico = dto.correo_electronico)
        historial = HistorialNombres(nombre = part.nombre, fecha = datetime.now().date(), id_participante = part.id)
        part.historial_nombres = [historial]
        competencia.participantes.append(part)
        competencia.estado = 'Creada'
        GestorBaseDeDatos.get_instance().modificar_competencia()
        return 1

    def modificar_participante(self):
        pass

    def eliminar_participante(self, participante):
        GestorBaseDeDatos.get_instance().eliminar_participante(participante)

    def listar_participantes(self, id_competencia = None, id_participante=None):
        lista_participantes = []
        if id_participante is not None:
            lista_participantes.append(GestorBaseDeDatos.get_instance().listar_participantes(id_participante=id_participante))
        else:
            lista_participantes += GestorBaseDeDatos.get_instance().listar_participantes(id_competencia=id_competencia)
        lista = []
        competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia=id_competencia)
        for participante in lista_participantes:
            nombres_en_historial = []
            for nombre in participante.historial_nombres:
                nombres_en_historial.append(nombre.nombre)
            dto_participante = DTOParticipante(participante.id, participante.nombre, participante.correo_electronico,
                                               competencia.nombre, nombres_en_historial, None)
            lista.append(dto_participante)
        return lista

    def registrar_historial(self):
        pass
