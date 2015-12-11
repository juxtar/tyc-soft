from main import Singleton
from gestorbasededatos import GestorBaseDeDatos
from excepciones import NombreExistente, FaltaDeDatos
from dtos import *
from pyged.almacenamiento import *

class GestorCompetencia(Singleton):
    """Realiza tareas correspondiente al manejo de clases Competencia"""
    def nueva_competencia(self, dto):
        from gestorusuario import GestorUsuario
        from gestorlugar import GestorLugar

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
            competencia_new = CompetenciaEliminatoriaSimple(nombre=dto.nombre, tipo_puntuacion=dto.tipo_puntuacion,
                                            cantidad_de_sets=dto.cantidad_de_sets, reglamento=dto.reglamento,
                                            estado='Creada', tantos_presentismo=dto.tantos_presentismo,
                                            sedes=lista_sedes, deporte=deporte)
        elif dto.tipo == 'eliminatoriadoble':
            competencia_new = CompetenciaEliminatoriaDoble(nombre=dto.nombre, tipo_puntuacion=dto.tipo_puntuacion,
                                            cantidad_de_sets=dto.cantidad_de_sets, reglamento=dto.reglamento,
                                            estado='Creada', tantos_presentismo=dto.tantos_presentismo,
                                            sedes=lista_sedes, deporte=deporte)
        else:
            competencia_new = CompetenciaLiga(nombre=dto.nombre, tipo_puntuacion=dto.tipo_puntuacion,
                                             cantidad_de_sets=dto.cantidad_de_sets, reglamento=dto.reglamento,
                                             estado='Creada', tantos_presentismo=dto.tantos_presentismo,
                                             sedes=lista_sedes,
                                             puntos_por_presentarse=dto.puntos_por_presentarse,
                                             puntos_por_ganar=dto.puntos_por_ganar,
                                             puntos_por_empate=dto.puntos_por_empate, deporte = deporte,
                                             permitir_empate=dto.permitir_empate)
        GestorUsuario.get_instance().agregar_competencia(dto.id_usuario, competencia_new)
        return 1

    def eliminar_competencia(self):
        pass
    def listar_competencias(self, id_competencia = None, nombre=None, id_usuario = None, deporte = None,
                            modalidad = None, estado = None):
        """Realiza la correspondiente busqueda de competencias, devuelve una lista de DTOs Competencias"""
        from gestorusuario import GestorUsuario

        lista_dtos = []
        if id_competencia is not None:
            competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia=id_competencia)
            usuario = GestorUsuario.get_instance().obtener_usuario(competencia.id_usuario)
            if competencia.tipo =='eliminatoriasimple' or competencia.tipo =='eliminatoriadoble':
                lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion,
                                                 competencia.estado, competencia.reglamento, competencia.id_usuario,
                                                 usuario.nombre, competencia.tipo, competencia.cantidad_de_sets,
                                                 None, None, None, competencia.deporte.nombre, None,
                                                 competencia.tantos_presentismo, None))
            else:
                lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion,
                                                 competencia.estado, competencia.reglamento, competencia.id_usuario,
                                                 usuario.nombre, competencia.tipo, competencia.cantidad_de_sets,
                                                 competencia.puntos_por_presentarse, competencia.puntos_por_ganar,
                                                 competencia.puntos_por_empate, competencia.deporte.nombre, None,
                                                 competencia.tantos_presentismo, competencia.permitir_empate))
        else:
            lista_competencias = GestorBaseDeDatos.get_instance().listar_competencias(nombre=nombre,
                                                                                      id_usuario=id_usuario,
                                                                                      deporte=deporte,
                                                                                      modalidad=modalidad,
                                                                                      estado=estado)
            for competencia in lista_competencias:
                usuario = GestorUsuario.get_instance().obtener_usuario(competencia.id_usuario)
                if competencia.tipo == 'eliminatoriasimple' or competencia.tipo == 'eliminatoriadoble':
                    lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion,
                                                     competencia.estado, competencia.reglamento,
                                                     competencia.id_usuario, usuario.nombre, competencia.tipo,
                                                     competencia.cantidad_de_sets, None, None, None,
                                                     competencia.deporte.nombre, None, competencia.tantos_presentismo,
                                                     None))
                else:
                    lista_dtos.append(DTOCompetencia(competencia.id, competencia.nombre, competencia.tipo_puntuacion,
                                                     competencia.estado, competencia.reglamento, competencia.id_usuario,
                                                     usuario.nombre, competencia.tipo, competencia.cantidad_de_sets,
                                                     competencia.puntos_por_presentarse, competencia.puntos_por_ganar,
                                                     competencia.puntos_por_empate, competencia.deporte.nombre, None,
                                                     competencia.tantos_presentismo, competencia.permitir_empate))
        return lista_dtos

    def generar_fixture(self, id_competencia):
        competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia=id_competencia)
        if len(competencia.partidas) > 0:
            GestorCompetencia.get_instance().eliminar_fixture(id_competencia=id_competencia)
            competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia=id_competencia)
        competencia.estado = 'Planificada'
        lista_participantes = competencia.participantes[:]
        if len(lista_participantes) < 2:
            raise FaltaDeDatos('No hay suficientes participantes en la competencia.')
        cantidad_de_participantes = len(lista_participantes)
        nombre_dummy = "Dummy" + competencia.nombre
        if (cantidad_de_participantes % 2) == 1:
            dummy  = Participante(nombre= nombre_dummy, correo_electronico = nombre_dummy,
                                  id_competencia = competencia.id)
            lista_participantes.append(dummy)
            cantidad_de_participantes = len(lista_participantes)
        for fecha in range(cantidad_de_participantes - 1):
            for partida in range(cantidad_de_participantes/2):
                if lista_participantes[partida].nombre == nombre_dummy:
                    nueva_partida = Partida(estado='Finalizado', instancia= fecha+1,
                                            participante_local = lista_participantes[partida],
                                            participante_visitante = lista_participantes[cantidad_de_participantes - (partida + 1)])
                elif lista_participantes[cantidad_de_participantes - (partida + 1)].nombre== nombre_dummy:
                    nueva_partida = Partida(estado='Finalizado', instancia= fecha+1,
                                            participante_local = lista_participantes[partida],
                                            participante_visitante = lista_participantes[cantidad_de_participantes - (partida + 1)])
                else:
                    nueva_partida = Partida(estado='Creada', instancia= fecha+1,
                                            participante_local = lista_participantes[partida],
                                            participante_visitante = lista_participantes[cantidad_de_participantes - (partida + 1)])

                competencia.partidas.append(nueva_partida)
            lista_participantes.append(lista_participantes.pop(1))
        GestorBaseDeDatos.get_instance().modificar_competencia()
        return 1

    def modificar_competencia(self, dto_competencia):
        competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia = dto_competencia.id)
        competencia.estado = dto_competencia.estado
        GestorBaseDeDatos.get_instance().modificar_competencia()

    def generar_tabla_posiciones(self, id_competencia):
        competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia = id_competencia)
        presentarse = competencia.puntos_por_presentarse
        ganar = competencia.puntos_por_ganar
        empate = competencia.puntos_por_empate
        lista_dtos = []
        lista_participantes = competencia.participantes
        for participante in lista_participantes:
            lista_partidas = competencia.partidas
            puntos = 0
            goles_a_favor = 0
            goles_en_contra = 0
            partidos_ganados = 0
            partidos_perdidos = 0
            partidos_empatados = 0
            tipo = None
            nombre_dummy = 'Dummy' + competencia.nombre
            if participante.nombre == nombre_dummy:
                continue
            for partida in lista_partidas:
                if partida.estado != 'Finalizada':
                    continue
                if partida.resultado.tipo == 'porpuntuacion':
                    tipo = 'porpuntuacion'
                    puntos += presentarse
                    if partida.participante_local == participante:
                        if partida.resultado.puntos_de_local > partida.resultado.puntos_de_visitante:
                            puntos += ganar
                            partidos_ganados += 1
                            goles_a_favor += partida.resultado.puntos_de_local
                            goles_en_contra += partida.resultado.puntos_de_visitante
                        elif partida.resultado.puntos_de_local < partida.resultado.puntos_de_visitante:
                            partidos_perdidos += 1
                            goles_a_favor += partida.resultado.puntos_de_local
                            goles_en_contra += partida.resultado.puntos_de_visitante
                        else:
                            puntos += empate
                            partidos_empatados += 1
                            goles_a_favor += partida.resultado.puntos_de_local
                            goles_en_contra += partida.resultado.puntos_de_visitante
                    if partida.participante_visitante == participante:
                        if partida.resultado.puntos_de_visitante > partida.resultado.puntos_de_local:
                            puntos += ganar
                            partidos_ganados += 1
                            goles_a_favor += partida.resultado.puntos_de_visitante
                            goles_en_contra += partida.resultado.puntos_de_local
                        elif partida.resultado.puntos_de_visitante < partida.resultado.puntos_de_local:
                            partidos_perdidos += 1
                            goles_a_favor += partida.resultado.puntos_de_visitante
                            goles_en_contra += partida.resultado.puntos_de_local
                        else:
                            puntos += empate
                            partidos_empatados += 1
                            goles_a_favor += partida.resultado.puntos_de_visitante
                            goles_en_contra += partida.resultado.puntos_de_local
                if partida.resultado.tipo == 'porresultadofinal':
                    tipo = 'porresultadofinal'
                    puntos = puntos + presentarse
                    if partida.participante_local == participante:
                        if partida.resultado.resultado_de_local == 1:
                            puntos += ganar
                            partidos_ganados += 1
                        elif partida.resultado.resultado_de_local == 0.5:
                            partidos_empatados += 1
                            puntos += empate
                        else:
                            partidos_perdidos += 1
                    if partida.participante_visitante == participante:
                        if partida.resultado.resultado_de_visitante == 1:
                            partidos_ganados += 1
                            puntos += ganar
                        elif partida.resultado.resultado_de_visitante == 0.5:
                            partidos_empatados += 1
                            puntos += empate
                        else:
                            partidos_perdidos += 1
                if partida.resultado.tipo == 'porsets':
                    tipo = 'porsets'
                    puntos += presentarse
                    if partida.participante_local == participante:
                        lista_sets = partida.resultado.sets
                        ganador_local = 0
                        ganador_visitante = 0
                        for sets in lista_sets:
                            if sets.puntaje_de_local > sets.puntaje_de_visitante:
                                ganador_local += 1
                                goles_a_favor += sets.puntaje_de_local
                                goles_en_contra += sets.puntaje_de_visitante
                            if sets.puntaje_de_local < sets.puntaje_de_visitante:
                                ganador_visitante += 1
                                goles_a_favor += sets.puntaje_de_local
                                goles_en_contra += sets.puntaje_de_visitante
                        if ganador_local > ganador_visitante:
                            puntos += ganar
                            partidos_ganados += 1
                        else:
                            partidos_perdidos += + 1
                    if partida.participante_visitante == participante:
                        lista_sets = partida.resultado.sets
                        ganador_local = 0
                        ganador_visitante = 0
                        for sets in lista_sets:
                            if sets.puntaje_de_local > sets.puntaje_de_visitante:
                                ganador_local += 1
                                goles_a_favor += sets.puntaje_de_visitante
                                goles_en_contra += sets.puntaje_de_local
                            if sets.puntaje_de_local < sets.puntaje_de_visitante:
                                ganador_visitante += 1
                                goles_a_favor += sets.puntaje_de_visitante
                                goles_en_contra += sets.puntaje_de_local
                        if ganador_local < ganador_visitante:
                            puntos += ganar
                            partidos_ganados += 1
                        else:
                            partidos_perdidos += 1
            if tipo == 'porpuntuacion':
                dto = DTOTabla(participante.id, participante.nombre, puntos, partidos_ganados, partidos_empatados,
                               partidos_perdidos, goles_a_favor, goles_en_contra)
                lista_dtos.append(dto)
            if tipo == 'porresultadofinal':
                dto = DTOTabla(participante.id, participante.nombre, puntos, partidos_ganados, partidos_empatados,
                               partidos_perdidos, goles_a_favor, goles_en_contra)
                lista_dtos.append(dto)
            if tipo == 'porsets':
                dto = DTOTabla(participante.id, participante.nombre, puntos,partidos_ganados, 0, partidos_perdidos,
                               goles_a_favor, goles_en_contra)
                lista_dtos.append(dto)
        return lista_dtos

    def eliminar_fixture(self, id_competencia):
        from gestorparticipante import GestorParticipante

        competencia = GestorBaseDeDatos.get_instance().listar_competencias(id_competencia = id_competencia)
        for participante in competencia.participantes:
            nombre_dummy = 'Dummy' + competencia.nombre
            if participante.nombre == nombre_dummy:
                competencia.participantes.remove(participante)
                GestorParticipante.get_instance().eliminar_participante(participante)
                break
        for partida in competencia.partidas:
            GestorBaseDeDatos.get_instance().eliminar_partida(partida)

    def listar_deportes(self):
        deportes = GestorBaseDeDatos.get_instance().listar_deportes()
        lista_deportes = []
        for d in deportes:
            lista_deportes.append(d.nombre)
        return lista_deportes
