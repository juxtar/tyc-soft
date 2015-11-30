from main import Singleton
from gestorbasededatos import GestorBaseDeDatos
from dtos import DTOLugar
from gestorcompetencia import GestorCompetencia


class GestorPartida(Singleton):
    """Realiza tareas correspondientes al manejo de clases Lugar"""
    def __init__(self):
        pass

    def listar_partidas(self, id_usuario = None, id_competencia = None):
        if id_competencia is not None:
            return GestorBaseDeDatos.get_instance().listar_partidas(id_competencia = id_competencia)
        if id_usuario is not None:
            return GestorBaseDeDatos.get_instance().listar_partidas(id_usuario = id_usuario)