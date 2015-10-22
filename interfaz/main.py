import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

def agregar_cuadro_error(main_window):
    """Dada una ventana pasada como argumento, le agrega un widget para poder
    mostrar mensajes de errores en la parte superior"""

    hijo = main_window.get_child()
    vbox = gtk.VBox()
    glade = gtk.Builder()
    glade.add_from_file('glade\error.glade')
    infobar = glade.get_object('infobar')
    infobar.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color("#ff0000"))

    vbox.pack_start(infobar, False, True, 0)
    vbox.pack_start(hijo, True, True, 0)
    main_window.remove(hijo)
    main_window.add(vbox)

    boton_cerrar = glade.get_object('button1')

    def cerrar_error(self, widget):
        """Oculta el mensaje de error en la ventana correspondiente"""
        self.infobar.hide()

    def mostrar_error(self, *mensajes):
        """Elimina mensajes anteriores y agrega los mensajes pasados como
        argumento al widget de error"""
        contenedor = self.infobar.get_child()
        for widget in contenedor.get_children():
            contenedor.remove(widget)
        for mensaje in mensajes:
            label = gtk.Label(mensaje)
            contenedor.pack_start(label, True, True, 0)
            label.show()
        self.infobar.show()

    return infobar, boton_cerrar, cerrar_error, mostrar_error
