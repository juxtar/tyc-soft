import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path
from pyged.gestores.gestorpartida import GestorPartida
from pyged.gestores.dtos import DTOResultado, DTOSet
from main import agregar_cuadro_error, Interfaz
from aviso import Exito


class MostrarFixture(Interfaz):
    """Interfaz que muestra todas las partidas de la competencia"""
    def __init__(self, id_competencia):
        self.id_competencia = id_competencia

class GestionarFinal(Interfaz):
    """Interfaz para gestionar un resultado de tipo final"""
    def __init__(self, id_partida, ventana_padre):
        self.id_partida = id_partida
        self.ventana_padre = ventana_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button6').connect('clicked', self.volver)
        self.glade.get_object('button7').connect('clicked', self.aceptar)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)[0]
        self.glade.get_object('label38').set_text(datos_partida.nombre_local)
        self.glade.get_object('label42').set_text(datos_partida.nombre_visitante)
        self.glade.get_object('label40').set_sensitive(datos_partida.permitir_empate)
        self.glade.get_object('radiobutton2').set_sensitive(datos_partida.permitir_empate)

        self.main_window = self.glade.get_object('gestionar_final')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def destroy(self, widget):
        self.volver(None)

    def aceptar(self, widget):
        local_presente = self.glade.get_object('checkbutton1').get_active()
        visitante_presente = self.glade.get_object('checkbutton2').get_active()

        mensajes_error = []
        if not (local_presente or visitante_presente):
            mensajes_error.append('Debe haber al menos un participante presente.')

        if mensajes_error:
            self.mostrar_error(*mensajes_error)
            return

        local = self.glade.get_object('radiobutton1').get_active()
        empate = self.glade.get_object('radiobutton2').get_active()
        visitante = self.glade.get_object('radiobutton3').get_active()

        arg = tuple()
        if local:
            arg = (1., 0., None)
        elif empate:
            arg = (.5, .5, None)
        elif visitante:
            arg = (0., 1., None)
        dto = DTOResultado(None, self.id_partida, 'porresultadofinal', local_presente, visitante_presente, *arg)
        exito = GestorPartida.get_instance().agregar_resultado(dto)
        if exito is 1:
            Exito(self)

    def volver(self, widget):
        self.main_window.hide()
        self.ventana_padre.show()

class GestionarPuntos(Interfaz):
    """Interfaz para gestionar un resultado de tipo puntos"""
    def __init__(self, id_partida, ventana_padre):
        self.id_partida = id_partida
        self.ventana_padre = ventana_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button10').connect('clicked', self.volver)
        self.glade.get_object('button11').connect('clicked', self.aceptar)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)[0]
        self.glade.get_object('checkbutton5').set_label(datos_partida.nombre_local)
        self.glade.get_object('checkbutton6').set_label(datos_partida.nombre_visitante)
        self.permitir_empate = datos_partida.permitir_empate

        self.main_window = self.glade.get_object('gestionar_puntos')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def destroy(self, widget):
        self.volver(None)

    def volver(self, widget):
        self.main_window.hide()
        self.ventana_padre.show()

    def aceptar(self, widget):
        local = int(self.glade.get_object('spinbutton1').get_value())
        visitante = int(self.glade.get_object('spinbutton2').get_value())

        mensajes_error = []
        if not self.permitir_empate:
            if local == visitante:
                mensajes_error.append('En esta competencia no esta permitido el empate.')

        local_presente = self.glade.get_object('checkbutton5').get_active()
        visitante_presente = self.glade.get_object('checkbutton6').get_active()
        if not (local_presente or visitante_presente):
            mensajes_error.append('Debe haber al menos un participante presente.')

        if mensajes_error:
            self.mostrar_error(*mensajes_error)
            return

        dto = DTOResultado(None, self.id_partida, 'porpuntuacion', local_presente, visitante_presente, local, visitante,
                           None)
        exito = GestorPartida.get_instance().agregar_resultado(dto)
        if exito is 1:
            Exito(self)

class GestionarSets(Interfaz):
    """Interfaz para gestionar un resultado de tipo sets"""
    def __init__(self, id_partida, ventana_padre):
        self.id_partida = id_partida
        self.ventana_padre = ventana_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button8').connect('clicked', self.volver)
        self.glade.get_object('button9').connect('clicked', self.aceptar)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)[0]
        self.glade.get_object('checkbutton4').set_label(datos_partida.nombre_local)
        self.glade.get_object('checkbutton3').set_label(datos_partida.nombre_visitante)
        self.cantidad_de_sets = datos_partida.cantidad_de_sets

        self.lista_widgets = [
            {
             'label': self.glade.get_object('label'+str(index+43)),
             'local': self.glade.get_object('entry'+str(index)),
             'visitante': self.glade.get_object('entry'+str(index+9))
            }
                        for index in range(1, 10)]
        for i, widgets in enumerate(self.lista_widgets):
            for widget in widgets.values():
                widget.set_sensitive(i<datos_partida.cantidad_de_sets)
            widgets['local'].connect('changed', self.dinamizar)
            widgets['visitante'].connect('changed', self.dinamizar)

        self.main_window = self.glade.get_object('gestionar_sets')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def destroy(self, widget):
        self.volver(None)

    def volver(self, widget):
        self.main_window.hide()
        self.ventana_padre.show()

    def aceptar(self, widget):
        mensajes_error = []

        lista_dto_sets = []
        lista_sets = self.lista_widgets[:self.cantidad_de_sets]
        for i, diccionario in enumerate(lista_sets):
            valor_local = diccionario['local'].get_text()
            valor_visitante = diccionario['visitante'].get_text()
            if '' in [valor_local, valor_visitante]:
                if valor_local == '':
                    mensajes_error.append('Debe ingresar un valor para el equipo local en el set {}.'.format(i+1))
                if valor_visitante == '':
                    mensajes_error.append('Debe ingresar un valor para el equipo visitante en el set {}.'.format(i+1))
                continue # Si ocurre un error, salta al proximo elemento de la lista

            puntos_local = int(valor_local)
            puntos_visitante = int(valor_visitante)
            if puntos_local == puntos_visitante:
                mensajes_error.append('Debe haber un ganador en el set {}.'.format(i+1))
                continue # Si ocurre un error, salta al proximo elemento de la lista
            lista_dto_sets.append(DTOSet(None, puntos_local, puntos_visitante, i+1))

        local_presente = self.glade.get_object('checkbutton4').get_active()
        visitante_presente = self.glade.get_object('checkbutton3').get_active()

        if not (local_presente or visitante_presente):
            mensajes_error.append('Debe haber al menos un participante presente.')

        if mensajes_error:
            self.mostrar_error(*mensajes_error)
            return

        dto = DTOResultado(None, self.id_partida, 'porpuntuacion', local_presente, visitante_presente, None, None,
                           lista_dto_sets)
        exito = GestorPartida.get_instance().agregar_resultado(dto)
        if exito is 1:
            Exito(self)

    def dinamizar(self, widget):
        texto = widget.get_text()
        texto = filter(str.isdigit, texto)
        if len(texto) > 2:
            texto = texto[:2]
        widget.set_text(texto)
