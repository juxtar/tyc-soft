from main import Singleton
from gestorbasededatos import GestorBaseDeDatos
from dtos import DTOLugar


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
