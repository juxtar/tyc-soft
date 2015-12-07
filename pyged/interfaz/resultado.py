import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path
from pyged.gestores import GestorPartida
from main import agregar_cuadro_error, Interfaz
from aviso import Exito

class GestionarFinal(Interfaz):
    """Interfaz para gestionar un resultado de tipo final"""
    def __init__(self, id_partida):
        self.id_partida = id_partida
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button6').connect('clicked', self.volver)
        self.glade.get_object('button7').connect('clicked', self.aceptar)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)
        self.glade.get_object('label38').set_text(datos_partida.nombre_local)
        self.glade.get_object('label42').set_text(datos_partida.nombre_visitante)
        self.glade.get_object('label40').set_sensitive(datos_partida.permitir_empate)
        self.glade.get_object('radiobutton2').set_sensitive(not (datos_partida.permitir_empate))

        self.main_window = self.glade.get_object('gestionar_final')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def destroy(self, widget):
        pass

    def aceptar(self, widget):
        pass

    def volver(self, widget):
        pass

class GestionarPuntos(Interfaz):
    """Interfaz para gestionar un resultado de tipo puntos"""
    def __init__(self, id_partida):
        self.id_partida = id_partida
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button10').connect('clicked', self.volver)
        self.glade.get_object('button11').connect('clicked', self.aceptar)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)
        self.glade.get_object('checkbutton5').set_label(datos_partida.nombre_local)
        self.glade.get_object('checkbutton6').set_label(datos_partida.nombre_visitante)

        self.main_window = self.glade.get_object('gestionar_puntos')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def destroy(self, widget):
        pass

    def volver(self, widget):
        pass

    def aceptar(self, widget):
        pass

class GestionarSets(Interfaz):
    """Interfaz para gestionar un resultado de tipo sets"""
    def __init__(self, id_partida):
        self.id_partida = id_partida
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button8').connect('clicked', self.volver)
        self.glade.get_object('button9').connect('clicked', self.aceptar)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)
        self.glade.get_object('checkbutton4').set_label(datos_partida.nombre_local)
        self.glade.get_object('checkbutton3').set_label(datos_partida.nombre_visitante)

        self.lista_widgets = [
            {
             'label': self.glade.get_object('label'+str(index+43)),
             'local': self.glade.get_object('entry'+str(index)),
             'visitante': self.glade.get_object('entry'+str(index+9))
            }
                        for index in range(1, 10)]
        for i, widgets in enumerate(self.lista_widgets):
            for widget in widgets.values():
                widget.set_sensitive(not (i<datos_partida.cantidad_de_sets))
            widgets['local'].connect('changed', self.dinamizar)
            widgets['visitante'].connect('changed', self.dinamizar)



        self.main_window = self.glade.get_object('gestionar_sets')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def destroy(self, widget):
        pass

    def volver(self, widget):
        pass

    def aceptar(self, widget):
        pass

    def dinamizar(self, widget):
        texto = widget.get_text()
        texto = filter(str.isdigit, texto)
        widget.set_text(texto)