import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path


class Exito:
    """Ventana que indica que la operacion fue realizada con exito"""
    def __init__(self, clase_ventana_padre, volver=True, mensaje=None):
        self.clase_ventana_padre = clase_ventana_padre
        self.volver = volver
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'/glade/aviso.glade')
        self.main_window = self.glade.get_object('exito')
        self.main_window.set_transient_for(clase_ventana_padre.main_window)

        if mensaje is not None:
            label_mensaje = gtk.Label(mensaje)
            self.glade.get_object('vbox1').pack_end(label_mensaje, True, True, 0)

        self.main_window.show_all()
        self.main_window.connect('destroy', self.destroy)
        self.glade.get_object('button3').connect('clicked', self.destroy)

    def destroy(self, widget):
        self.main_window.hide()
        if self.volver:
            self.clase_ventana_padre.volver(None)

class Advertencia:
    """Ventana que pregunta al usuario sobre la accion que va a realizar"""
    def __init__(self, mensaje, clase_ventana_padre, generar_fixture, volver=True):
        self.clase_ventana_padre = clase_ventana_padre
        self.generar_fixture = generar_fixture
        self.volver = volver
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'/glade/aviso.glade')
        self.main_window = self.glade.get_object('advertencia')
        self.main_window.set_transient_for(clase_ventana_padre.main_window)

        self.glade.get_object('mensaje').set_label(mensaje)
        self.glade.get_object('button1').connect('clicked', self.continuar)
        self.glade.get_object('button2').connect('clicked', self.continuar)

        self.main_window.show_all()
        self.main_window.connect('destroy', self.destroy)

    def continuar(self, widget):
        nombre = gtk.Buildable.get_name(widget)
        if nombre == 'button1':
            if self.generar_fixture:
                self.clase_ventana_padre.main_window.show()
                self.clase_ventana_padre.generar_fixture()
        self.destroy(None)

    def destroy(self, widget):
        self.main_window.hide()
        if self.volver:
            self.clase_ventana_padre.volver(None)
