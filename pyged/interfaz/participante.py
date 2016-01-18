import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path
from main import agregar_cuadro_error,Interfaz
from pyged.gestores.gestorparticipante import GestorParticipante
from pyged.gestores.gestorcompetencia import GestorCompetencia
from pyged.gestores.dtos import DTOParticipante
from aviso import Exito
from pyged.gestores.excepciones import NombreExistente, FaltaDeDatos
import re

class NuevoParticipante(Interfaz):
    """Interfaz para crear un nuevo participante"""
    def __init__(self, id_competencia, clase_padre):
        self.id_competencia = id_competencia
        self.clase_padre = clase_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\participante.glade')
        self.main_window = self.glade.get_object('nuevo_participante')
        self.glade.get_object('button5').connect('clicked', self.aceptar)
        self.glade.get_object('button6').connect('clicked', self.volver)
        self.glade.get_object('filechooserbutton1').connect('file-set', self.imagen_seleccionada)
        self.glade.get_object('entry1').connect('changed', self.dinamizar)
        self.glade.get_object('entry2').connect('changed', self.dinamizar)
        filtro_imagen = gtk.FileFilter()
        filtro_imagen.set_name("Imagenes")
        filtro_imagen.add_mime_type("image/png")
        filtro_imagen.add_mime_type("image/jpeg")
        filtro_imagen.add_mime_type("image/gif")
        filtro_imagen.add_pattern("*.png")
        filtro_imagen.add_pattern("*.jpg")
        filtro_imagen.add_pattern("*.gif")
        filtro_imagen.add_pattern("*.tif")
        filtro_imagen.add_pattern("*.xpm")
        self.glade.get_object('filechooserbutton1').add_filter(filtro_imagen)

        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def imagen_seleccionada(self, widget):
        ruta_imagen = widget.get_filename()
        self.glade.get_object('image1').set_from_file(ruta_imagen)

    def aceptar(self, widget):
        nombre = self.glade.get_object('entry1').get_text()
        email = self.glade.get_object('entry2').get_text()
        imagen = self.glade.get_object('filechooserbutton1')

        errores = self.validar_nombre(nombre) + self.validar_email(email)
        if not errores:
            dto = DTOParticipante(None, nombre, email, self.id_competencia, None, imagen)
            try:
                exito = GestorParticipante.get_instance().nuevo_participante(dto)
                if exito is 1:
                    Exito(self)
            except NombreExistente as e:
                self.mostrar_error(e.mensaje)
            except FaltaDeDatos as f:
                self.mostrar_error(f.mensaje)
        else:
            self.mostrar_error(*errores)

    def destroy(self, widget):
        gtk.main_quit()

    def volver(self, widget):
        self.main_window.hide()
        self.clase_padre.listar_participantes()
        self.clase_padre.main_window.show()

    def validar_nombre(self, nombre):
        if not re.match(r"^[A-Z0-9]+( [A-Z0-9]+)*$", nombre, re.IGNORECASE):
            return ['Nombre incorrecto, solo puede contener letras, numeros y espacios',
                    'y no debe empezar ni terminar con un espacio.']
        else:
            return []

    def validar_email(self, email):
        email_re = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
            r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain
        if email_re.match(email):
            return []
        else:
            return ['Correo invalido.']

    def dinamizar(self, widget):
        texto = widget.get_text()
        widget.set_text(texto[:100])

class VerParticipantes(Interfaz):
    """Interfaz para ver los participantes de una competencia"""
    def __init__(self, id_competencia, clase_padre):
        self.id_competencia = id_competencia
        self.clase_padre = clase_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\participante.glade')
        self.main_window = self.glade.get_object('ver_participantes')
        self.glade.get_object('button4').connect('clicked', self.volver)
        self.glade.get_object('button1').connect('clicked', self.nuevo_participante)
        datos_competencia = GestorCompetencia.get_instance().listar_competencias(id_competencia=id_competencia)[0]
        self.glade.get_object('label1').set_text(datos_competencia.nombre)

        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

        self.listar_participantes()

    def listar_participantes(self):
        lista_participantes = GestorParticipante().get_instance().listar_participantes(id_competencia=self.id_competencia)
        modelo = self.glade.get_object('treeview1').get_model()
        modelo.clear()
        for participante in lista_participantes:
            if 'Dummy' in participante.nombre:
                continue
            modelo.append([participante.nombre, participante.correo_electronico])

    def nuevo_participante(self, widget):
        n = NuevoParticipante(self.id_competencia, self)
        self.main_window.hide()

    def destroy(self, widget):
        gtk.main_quit()

    def volver(self, widget):
        self.main_window.hide()
        self.clase_padre.actualizar()

