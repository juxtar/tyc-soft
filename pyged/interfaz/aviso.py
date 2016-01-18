import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path


class Exito:
    """Ventana que indica que la operacion fue realizada con exito"""
    def __init__(self, clase_ventana_padre, volver=True):
        self.clase_ventana_padre = clase_ventana_padre
        self.volver = volver
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\aviso.glade')
        self.main_window = self.glade.get_object('exito')
        self.main_window.set_transient_for(clase_ventana_padre.main_window)
        self.main_window.show_all()
        self.main_window.connect('destroy', self.destroy)
        self.glade.get_object('button3').connect('clicked', self.destroy)

    def destroy(self, widget):
        self.main_window.hide()
        if self.volver:
            self.clase_ventana_padre.volver(None)
