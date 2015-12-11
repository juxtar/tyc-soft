from main import Singleton
from gestorbasededatos import GestorBaseDeDatos
from dtos import *
from pyged.almacenamiento import *
from datetime import datetime
from excepciones import *
from gestorcompetencia import GestorCompetencia

class GestorPartida(Singleton):
    """Realiza tareas correspondientes al manejo de clases Lugar"""
    def __init__(self):
        pass

    def listar_partidas(self, id_participante=None, id_partida=None, id_competencia=None):
        from gestorcompetencia import GestorCompetencia

        lista_partidas = GestorBaseDeDatos.get_instance().listar_partidas(id_participante = id_participante,
                                                                          id_partida = id_partida,
                                                                          id_competencia = id_competencia)
        if id_partida is not None:
            lista_partidas = [lista_partidas]
        lista_dtos = []
        for partida in lista_partidas:
            competencia = GestorCompetencia.get_instance().listar_competencias(id_competencia=partida.id_competencia)[0]
            dto = DTOPartida(partida.id, partida.estado, partida.instancia, partida.local_presente,
                             partida.visitante_presente, partida.id_resultado, partida.participante_local.nombre,
                             partida.participante_visitante.nombre, competencia.permitir_empate,
                             competencia.tipo_puntuacion, competencia.cantidad_de_sets)
            lista_dtos.append(dto)
        return lista_dtos

    def listar_resultado(self, id_partida):
        partida = GestorBaseDeDatos.get_instance().listar_partidas(id_partida = id_partida)
        if partida.resultado is None:
            raise FaltaDeDatos('No existen Resultados para esta partida.')
        if partida.resultado.tipo == 'porsets':
            lista_sets = []
            for sets in partida.resultado.sets:
                dtoSet = DTOSet(sets.id, sets.puntaje_de_local, sets.puntaje_de_visitante,sets.numero)
                lista_sets.append(dtoSet)
            return DTOResultado(partida.resultado.id, partida.id, partida.resultado.tipo,partida.local_presente, partida.visitante_presente,
                                None, None, lista_sets)
        if partida.resultado.tipo == 'porresultadofinal':
            return DTOResultado(partida.resultado.id, partida.id, partida.resultado.tipo,partida.local_presente,partida.visitante_presente,
                               partida.resultado.resultado_de_local, partida.resultado.resultado_de_visitante, None)
        if partida.resultado.tipo == 'porpuntuacion':
            return DTOResultado(partida.resultado.id, partida.id, partida.resultado.tipo,partida.local_presente,partida.visitante_presente,
                               partida.resultado.puntos_de_local, partida.resultado.puntos_de_visitante, None)
    def agregar_resultado(self, dto):
        partida = GestorBaseDeDatos.get_instance().listar_partidas(id_partida = dto.id_partida)
        resultado_new = None
        if dto.tipo == 'porsets':
            lista_de_sets = []
            for dtoset in dto.lista_dto_sets:
                new_set = Set( puntaje_de_local = dtoset.puntaje_local, puntaje_de_visitante = dtoset.puntaje_visitante,
                          numero = dtoset.numero_de_set)
                lista_de_sets.append(new_set)
            resultado_new = ResultadoPorSet(fecha = datetime.now().date(), sets = lista_de_sets)
        elif dto.tipo == 'porresultadofinal':
            resultado_new = ResultadoPorResultadoFinal(fecha = datetime.now().date(), resultado_de_local = dto.resultado_local,
                resultado_de_visitante = dto.resultado_visitante)
        elif dto.tipo == 'porpuntuacion':
            resultado_new = ResultadoPorPuntuacion(fecha = datetime.now().date(), puntos_de_local = dto.resultado_local,
                puntos_de_visitante = dto.resultado_visitante)
        if partida.resultado is None:
            dtocompetencia = DTOCompetencia(partida.id_competencia, None, None, 'En Disputa',None, None, None, None, None, None,None,
                                 None, None, None, None, None)
            GestorCompetencia.get_instance().modificar_competencia(dtocompetencia)
        partida.resultado = resultado_new
        partida.visitante_presente = dto.visitante_presente
        partida.local_presente = dto.local_presente
        partida.estado = 'Finalizada'
        partida.historial.append(resultado_new)
        GestorBaseDeDatos.get_instance().modificar_partida()
        lista_partidas = GestorBaseDeDatos.get_instance().listar_partidas(id_competencia = partida.id_competencia)
        terminado = 0
        for partidas in lista_partidas:
            if partidas.estado in ['Finalizado', 'Finalizada']:
                terminado += 1
        if terminado == len(lista_partidas):
            dtocompetencia = DTOCompetencia(partida.id_competencia,None, None, 'Finalizada', None, None, None, None, None, None, None,
                             None, None, None, None, None)
            GestorCompetencia.get_instance().modificar_competencia(dtocompetencia)
        return 1