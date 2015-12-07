from main import Singleton
from gestorbasededatos import GestorBaseDeDatos
from gestorcompetencia import GestorCompetencia
from gestorparticipante import GestorParticipante
from dtos import DTOPartida

class GestorPartida(Singleton):
    """Realiza tareas correspondientes al manejo de clases Lugar"""
    def __init__(self):
        pass

    def listar_partidas(self, id_participante=None, id_partida=None):
        lista_partidas = GestorBaseDeDatos.get_instance().listar_partidas(id_participante = id_participante,
                                                                          id_partida = id_partida)
        if id_partida is not None:
            lista_partidas = [lista_partidas]
        lista_dtos = []
        for partida in lista_partidas:
            competencia = GestorCompetencia.get_instance().listar_competencias(id_competencia=partida.id_competencia)
            dto = DTOPartida(partida.id, partida.estado, partida.instancia, partida.local_presente,
                             partida.local_visitante, partida.id_resultado, partida.participante_local.nombre,
                             partida.participante_visitante.nombre, competencia.permitir_empate,
                             competencia.tipo_puntuacion, competencia.cantidad_de_sets)
            lista_dtos.append(dto)
        return lista_dtos