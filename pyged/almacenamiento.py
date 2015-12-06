from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Boolean, DateTime, Float
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Pais(Base):
    """Almacena informacion de un pais"""
    
    __tablename__ = 'pais'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)

    def __repr__(self):
        return '<Pais(%r)>' % self.nombre

class Provincia(Base):
    """Almacena informacion de una provincia"""
    
    __tablename__ = 'provincia'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    id_pais = Column(Integer, ForeignKey('pais.id'))

    pais = relationship("Pais")

    def __repr__(self):
        return '<Provincia(%r)>' % self.nombre

class Usuario(Base):
    """Almacena informacion de un usuario"""

    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, unique=True)
    dni = Column(Integer, nullable=False, unique=True)
    tipo_dni = Column(String, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    correo_electronico = Column(String, nullable=False, unique=True)
    contrasenia = Column(String, nullable=False)
    localidad = Column(String)
    id_provincia = Column(Integer, ForeignKey('provincia.id'))

    provincia = relationship("Provincia")
    lugares = relationship("Lugar")
    competencias = relationship("Competencia")

    def __repr__(self):
        return '<Usuario(%r, %r, %r)>' % (self.nombre, self.apellido, self.correo_electronico)

class Sesion(Base):
    """Almacena informacion de una sesion de logueo de un usuario"""

    __tablename__ = 'sesion'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    hora = Column(DateTime)
    fecha = Column(Date)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))

    usuario = relationship("Usuario")

    def __repr__(self):
        return '<Sesion(%r, %r)>' % (self.nombre, self.usuario)

tabla_se_desarrolla = Table('se_desarrolla', Base.metadata,
    Column('id_deporte', Integer, ForeignKey('deporte.id')),
    Column('id_lugar', Integer, ForeignKey('lugar.id'))
)

class Lugar(Base):
    """Almacena informacion de un lugar"""

    __tablename__ = 'lugar'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_baja = Column(Date)
    dado_de_baja = Column(Boolean)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))

    deportes = relationship("Deporte",
                    secondary=tabla_se_desarrolla)

    def __repr__(self):
        return '<Lugar(%r)>' % (self.nombre)

class Sede(Base):
    """Almacena informacion de una sede"""
    
    __tablename__ = 'sede'

    id_competencia = Column(Integer, ForeignKey('competencia.id'), primary_key=True)
    id_lugar = Column(Integer, ForeignKey('lugar.id'), primary_key=True)
    disponibilidad = Column(Integer)

    lugar = relationship("Lugar")

    def __repr__(self):
        return '<Sede(%r)>' % (self.disponibilidad)

class Deporte(Base):
    """Almacena informacion de un deporte"""

    __tablename__ = 'deporte'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)

    def __repr__(self):
        return '<Deporte(%r)>' % self.nombre

class Competencia(Base):
    """Almacena informacion de una competencia"""
    
    __tablename__ = 'competencia'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    tipo_puntuacion = Column(String)
    cantidad_de_sets = Column(Integer)
    reglamento = Column(String)
    estado = Column(String)
    tantos_presentismo = Column(Integer)
    dada_de_baja = Column(Boolean)
    fecha_de_baja = Column(Date)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    tipo = Column(String, nullable=False)
    id_deporte = Column(Integer, ForeignKey('deporte.id'))

    deporte = relationship("Deporte")
    sedes = relationship("Sede")
    participantes = relationship("Participante")
    partidas = relationship("Partida")

    __mapper_args__ = {
        'polymorphic_identity':'competencia',
        'polymorphic_on':tipo
    }
    def __repr__(self):
        return '<Competencia(%r, %r)>' % (self.nombre, self.estado)

class CompetenciaLiga(Competencia):
    """Almacena informacion de una competencia modalidad liga"""
    
    __tablename__ = 'liga'

    id = Column(Integer, ForeignKey('competencia.id'), primary_key=True)
    puntos_por_presentarse = Column(Integer)
    puntos_por_ganar = Column(Integer)
    puntos_por_empate = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity':'liga'
    }
    def __repr__(self):
        return '<CompetenciaLiga(%r, %r)>' % (self.nombre, self.estado)

class CompetenciaEliminatoriaSimple(Competencia):
    """Almacena informacion de una competencia modalidad eliminatoria simple"""

    __tablename__ = 'eliminatoriasimple'

    id = Column(Integer, ForeignKey('competencia.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'eliminatoriasimple',
    }
    def __repr__(self):
        return '<CompetenciaEliminatoriaSimple(%r, %r)>' % (self.nombre, self.estado)

class CompetenciaEliminatoriaDoble(Competencia):
    """Almacena informacion de una competencia modalidad eliminatoria doble"""

    __tablename__ = 'eliminatoriadoble'

    id = Column(Integer, ForeignKey('competencia.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'eliminatoriadoble',
    }
    def __repr__(self):
        return '<CompetenciaEliminatoriaDoble(%r, %r)>' % (self.nombre, self.estado)

class Participante(Base):
    """Almacena informacion de un participante"""

    __tablename__ = 'participante'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    correo_electronico = Column(String, nullable=False, unique=True)
    id_competencia = Column(Integer, ForeignKey('competencia.id'))
    historial_nombres = relationship("HistorialNombres")

    def __repr__(self):
        return '<Participante(%r, %r)>' % (self.nombre, self.correo_electronico)

class HistorialNombres(Base):
    """Almacena informacion del historial de nombres del usuario"""

    __tablename__ = 'historialnombres'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    fecha = Column(Date)
    id_participante = Column(Integer, ForeignKey('participante.id'))

    def __repr__(self):
        return '<HistorialNombres(%r, %r)>' % (self.nombre)

class Partida(Base):
    """Almacena informacion de una partida"""

    __tablename__ = 'partida'
    __table_args__ = (
            CheckConstraint('id_competidor_local != id_competidor_visitante', name='check_competidores'),
            CheckConstraint('id_proximo_ganador != id_proximo_perdedor', name='check_proximos')
        )

    id = Column(Integer, primary_key=True)
    estado = Column(String)
    instancia = Column(String)
    local_presente = Column(Boolean)
    visitante_presente = Column(Boolean)
    id_participante_local = Column(Integer, ForeignKey('participante.id'))
    id_participante_visitante = Column(Integer, ForeignKey('participante.id'))
    id_proximo_ganador = Column(Integer, ForeignKey('partida.id'))
    id_proximo_perdedor = Column(Integer, ForeignKey('partida.id'))
    id_resultado = Column(Integer, ForeignKey('resultado.id'))
    id_competencia = Column(Integer, ForeignKey('competencia.id'))

    proximo_ganador = relationship("Partida", uselist=False, foreign_keys="Partida.id_proximo_ganador")
    proximo_perdedor = relationship("Partida", uselist=False, foreign_keys="Partida.id_proximo_perdedor")
    participante_local = relationship("Participante", uselist=False, foreign_keys="Partida.id_participante_local")
    participante_visitante = relationship("Participante", uselist=False, foreign_keys="Partida.id_participante_visitante")
    resultado = relationship("Resultado", uselist=False, foreign_keys="Partida.id_resultado")
    historial = relationship("Resultado", foreign_keys="Resultado.id_partida")

    def __repr__(self):
        return '<Partida(%r, %r)>' % (self.instancia, self.estado)

class Resultado(Base):
    """Almacena informacion del resultado de una partida"""

    __tablename__ = 'resultado'

    id = Column(Integer, primary_key=True)
    fecha = Column(Date)
    id_partida = Column(Integer, ForeignKey('partida.id'))
    tipo = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'resultado',
        'polymorphic_on':tipo
    }

    def __repr__(self):
        return '<Resultado(%r, %r)>' % (self.fecha)

class ResultadoPorResultadoFinal(Resultado):
    """Almacena informacion de un resultado de tipo final (ganado o perdido)"""
    
    __tablename__ = 'porresultadofinal'

    id = Column(Integer, ForeignKey('resultado.id'), primary_key=True)
    resultado_de_local = Column(Float, nullable=False)
    resultado_de_visitante = Column(Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'porresultadofinal',
    }
    def __repr__(self):
        return '<ResultadoPorResultadoFinal(%r, %r)>' % (self.resultado_de_local, self.resultado_de_visitante)

class ResultadoPorPuntuacion(Resultado):
    """Almacena informacion de un resultado de tipo puntuacion"""

    __tablename__ = 'porpuntuacion'

    id = Column(Integer, ForeignKey('resultado.id'), primary_key=True)
    puntos_de_local = Column(Integer, nullable=False)
    puntos_de_visitante = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'porpuntuacion',
    }
    def __repr__(self):
        return '<ResultadoPorPuntuacion(%r, %r)>' % (self.puntos_de_local, self.puntos_de_visitante)

class ResultadoPorSet(Resultado):
    """Almacena informacion de un resultado de tipo sets"""

    __tablename__ = 'porsets'

    id = Column(Integer, ForeignKey('resultado.id'), primary_key=True)
    sets = relationship("Set")

    __mapper_args__ = {
        'polymorphic_identity':'porsets',
    }
    def __repr__(self):
        return '<ResultadoPorSet(%r, %r)>' % (self.fecha, self.sets)

class Set(Base):
    """Almacena informacion de un set"""

    __tablename__ = 'set'

    id = Column(Integer, primary_key=True)
    puntaje_de_local = Column(Integer, nullable=False)
    puntaje_de_visitante = Column(Integer, nullable=False)
    numero = Column(Integer, nullable=False)
    id_resultado = Column(Integer, ForeignKey('porsets.id'))

    def __repr__(self):
        return '<Set(%r, %r, %r)>' % (self.numero, self.puntaje_de_local, self.puntaje_de_visitante)
