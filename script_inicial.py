# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyged.almacenamiento import *
engine = create_engine('sqlite:///pyged.db', echo=True, convert_unicode=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

lucho = Usuario(dni=34891051, tipo_dni='DNI', nombre='Luciano',
                apellido='David', correo_electronico='lucianoad25@hotmail.com',
                contrasenia='holis', localidad='Feliciano',
                provincia=Provincia(nombre='Entre Rios', pais=Pais(nombre='Argentina')))
futbol = Deporte(nombre='Futbol')
lucho.lugares = [
        Lugar(nombre='Marangoni', descripcion='Atiende el Luis', deportes=[futbol]),
        Lugar(nombre='Marado', descripcion='En verano hace un calor barbaro', deportes=[futbol]),
        Lugar(nombre='El Pasillo', descripcion='Esta hecho un desastre', deportes=[futbol])
]
lucho.competencias = [
    CompetenciaEliminatoriaSimple(nombre='TORNEO INTERNO', tipo_puntuacion='porpuntuacion',
                                  reglamento='El que gana, gana.', estado='Creada', deporte=futbol,
                                  sedes=[
                                        Sede(lugar=lucho.lugares[0], disponibilidad=5)
                                      ])
    ]
session.add(lucho)
session.commit()

deportes = [Deporte(nombre='Basketball'), Deporte(nombre='Ajedrez'), Deporte(nombre='Voleyball'), Deporte(nombre='Tenis')]
session.add_all(deportes)
session.commit()
