import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path

main = gtk.main


class Interfaz:
    """Clase abstracta de interfaz que contiene metodos comunes a todas las interfaces"""
    def cerrar_error(self, widget):
        """Oculta el mensaje de error en la ventana correspondiente"""
        self.infobar.hide()

    def mostrar_error(self, *mensajes):
        """Elimina mensajes anteriores y agrega los mensajes pasados como
        argumento al widget de error"""
        contenedor = self.infobar.get_child().get_children()[1]
        for widget in contenedor.get_children():
            contenedor.remove(widget)
        for mensaje in mensajes:
            label = gtk.Label(mensaje)
            contenedor.pack_start(label, True, True, 0)
            label.show()
        self.infobar.show()
        print '\a',

    def agregar_cuadro_error(self):
        """Dada una ventana pasada como argumento, le agrega un widget para poder
        mostrar mensajes de errores en la parte superior"""

        hijo = self.main_window.get_child()
        vbox = gtk.VBox()
        glade = gtk.Builder()
        glade.add_from_file(path.dirname( path.abspath(__file__) )+'/glade/error.glade')
        infobar = glade.get_object('infobar')
        infobar.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#ff0000"))

        vbox.pack_start(infobar, False, True, 0)
        if hijo is not None:
            self.main_window.remove(hijo)
            vbox.pack_start(hijo, True, True, 0)
        self.main_window.add(vbox)

        color = gtk.gdk.Color('#8BB1C5')
        self.main_window.modify_bg(gtk.STATE_NORMAL, color)

        boton_cerrar = glade.get_object('button1')

        return infobar, boton_cerrar

    def obtener_descendientes(self, widget, tipo):
        """Busca descendientes del widget del tipo especificado"""
        descendientes = []
        try:
            for hijo in widget.get_children():
                if type(hijo).__name__ == tipo:
                    descendientes.append(hijo)
                else:
                    descendientes += self.obtener_descendientes(hijo, tipo)
        except AttributeError:
            return []
        except TypeError:
            hijo = widget.get_children()
            if type(hijo).__name__ == tipo:
                descendientes.append(hijo)
        finally:
            return descendientes