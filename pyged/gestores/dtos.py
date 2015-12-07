class DTOParticipante:
    """Almacena informacion para la transfrencia de datos de una competencia"""
    def __init__(self, id_participante, nombre, correo_electronico, id_competencia, historial_nombre, imagen):
        self.id = id_participante
        self.nombre = nombre
        """Nombre del participante"""
        self.correo_electronico = correo_electronico
        """Correo electronico del participante"""
        self.id_competencia = id_competencia
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
                id_usuario, nombre_usuario, tipo, cantidad_de_sets, puntos_por_presentarse, puntos_por_ganar,
                puntos_por_empate, deporte, lugares, tantos_presentismo, permitir_empate):
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
        self.permitir_empate = permitir_empate

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

class DTOTabla:
    """Almacena informacion para la transferencia de datos de resultados"""
    def __init__(self, id_participante, nombre, puntos, partidos_ganados, partidos_empatados, partidos_perdidos,
                 goles_a_favor, goles_en_contra):
        self.id = id_participante
        self.nombre = nombre
        self.puntos = puntos
        self.partidos_ganados = partidos_ganados
        self.partidos_empatados = partidos_empatados
        self.partidos_perdidos = partidos_perdidos
        self.goles_a_favor = goles_a_favor
        self.goles_en_contra = goles_en_contra

    def __repr__(self):
        return '<DTOTabla(%r, %r, %r, %r, %r, %r, %r)>' %(self.nombre, self.puntos, self.partidos_ganados,
                                                          self.partidos_empatados, self.partidos_perdidos,
                                                          self.goles_a_favor, self.goles_en_contra)

class DTOPartida:
    """Almacena informacion para la transfrencia de datos de partidas"""
    def __init__(self, id, estado, instancia, local_presente, visitante_presente, id_resultado, nombre_local,
                 nombre_visitante, permitir_empate, tipo_puntuacion, cantidad_de_sets):
        self.id = id
        self.estado = estado
        self.instancia = instancia
        self.local_presente = local_presente
        self.visitante_presente = visitante_presente
        self.id_resultado = id_resultado
        self.nombre_local = nombre_local
        self.nombre_visitante = nombre_visitante
        self.permitir_empate = permitir_empate
        self.tipo_puntuacion = tipo_puntuacion
        self.cantidad_de_sets = cantidad_de_sets
