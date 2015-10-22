import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from main import agregar_cuadro_error


class NuevoParticipante:
    """Interfaz para crear un nuevo participante"""
    def __init__(self):
        self.glade = gtk.Builder()
        self.glade.add_from_file('glade\participante.glade')
        self.main_window = self.glade.get_object('nuevo_participante')
        self.glade.get_object('button5').connect('clicked', self.aceptar)
        self.main_window.show_all()
        self.infobar, boton_cerrar, self.cerrar_error, self.mostrar_error = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)

    def aceptar(self, widget):
        pass

    def cancelar(self, widget):
        pass

    def validar_nombre(self, nombre):
        pass


class VerParticipantes:
    """Interfaz para ver los participantes de una competencia"""
    def __init__(self):
        self.glade = gtk.Builder()
        self.glade.add_from_file('glade\participante.glade')
        self.main_window = self.glade.get_object('ver_participantes')
        self.glade.get_object('button4').connect('clicked', self.volver)
        self.main_window.show_all()
        self.infobar, boton_cerrar, self.cerrar_error, self.mostrar_error = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)

    def volver(self, widget):
        pass
