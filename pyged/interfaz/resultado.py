import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path
from pyged.gestores.gestorpartida import GestorPartida
from pyged.gestores.gestorcompetencia import GestorCompetencia
from pyged.gestores.dtos import DTOResultado, DTOSet
from pyged.gestores.excepciones import FaltaDeDatos
from main import agregar_cuadro_error, Interfaz
from aviso import Exito


class MostrarFixture(Interfaz):
    """Interfaz que muestra todas las partidas de la competencia"""
    def __init__(self, id_competencia, ventana_padre):
        self.id_competencia = id_competencia
        self.ventana_padre = ventana_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button1').connect('clicked', self.volver)
        self.glade.get_object('button2').connect('clicked', self.ver_detalle)
        self.glade.get_object('button3').connect('clicked', self.gestionar_resultado)

        combo_instancia = self.glade.get_object('combobox1')
        combo_equipo =  self.glade.get_object('combobox2')

        self.lista_partidas = GestorPartida.get_instance().listar_partidas(id_competencia=id_competencia)
        instancias = set()
        equipos = set()
        for dto in self.lista_partidas:
            equipos.add(dto.nombre_local)
            equipos.add(dto.nombre_visitante)
            instancias.add('Fecha '+str(dto.instancia))
            try:
                resultado = GestorPartida.get_instance().listar_resultado(dto.id)
            except FaltaDeDatos:
                dto.ganador = 'Sin jugar'
                continue
            if resultado.tipo == 'porresultadofinal':
                if resultado.resultado_local == 1.0:
                    dto.ganador = dto.nombre_local
                elif resultado.resultado_local == 0.0:
                    dto.ganador = dto.nombre_visitante
                else:
                    dto.ganador = 'Empate'
            elif resultado.tipo == 'porpuntuacion':
                if resultado.resultado_local > resultado.resultado_visitante:
                    dto.ganador = dto.nombre_local
                elif resultado.resultado_local < resultado.resultado_visitante:
                    dto.ganador = dto.nombre_visitante
                else:
                    dto.ganador = 'Empate'
            elif resultado.tipo == 'porsets':
                ganadores = []
                for r_set in resultado.lista_dto_sets:
                    ganadores.append(r_set.puntaje_local>r_set.puntaje_visitante)
                if ganadores.count(True) > (dto.cantidad_de_sets/2):
                    dto.ganador = dto.nombre_local
                else:
                    dto.ganador = dto.nombre_visitante
            dto.ganador = 'Ganador: '+dto.ganador if dto.ganador != 'Empate' else dto.ganador

        self.treeview = self.glade.get_object('treeview1')
        self.treeview.get_model().clear()
        for partida in self.lista_partidas:
            self.treeview.get_model().append(['Fecha '+str(partida.instancia), partida.nombre_local,
                                              partida.nombre_visitante, partida.ganador, partida.id])

        combo_instancia.get_model().clear()
        combo_instancia.append_text('<<Todas>>')
        for x in instancias:
            combo_instancia.append_text(x)
        combo_instancia.set_active(0)
        combo_equipo.get_model().clear()
        combo_equipo.append_text('<<Todos>>')
        for x in equipos:
            combo_equipo.append_text(x)
        combo_equipo.set_active(0)

        self.main_window = self.glade.get_object('fixture')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()
        combo_instancia.connect('changed', self.dinamizar)
        combo_equipo.connect('changed', self.dinamizar)

    def dinamizar(self, widget):
        nombre = gtk.Buildable.get_name(widget)
        if nombre == 'combobox1':
            self.treeview.get_model().clear()
            if widget.get_active():
                for partida in self.lista_partidas:
                    if 'Fecha '+str(partida.instancia) == widget.get_model()[widget.get_active()][0]:
                        self.treeview.get_model().append(['Fecha '+str(partida.instancia), partida.nombre_local,
                                                          partida.nombre_visitante, partida.ganador, partida.id])
            else:
                for partida in self.lista_partidas:
                    self.treeview.get_model().append(['Fecha '+str(partida.instancia), partida.nombre_local,
                                                      partida.nombre_visitante, partida.ganador, partida.id])
        if nombre == 'combobox2':
            self.treeview.get_model().clear()
            if widget.get_active():
                for partida in self.lista_partidas:
                    if widget.get_model()[widget.get_active()][0] in [partida.nombre_local, partida.nombre_visitante]:
                        self.treeview.get_model().append(['Fecha '+str(partida.instancia), partida.nombre_local,
                                                          partida.nombre_visitante, partida.ganador, partida.id])
            else:
                for partida in self.lista_partidas:
                    self.treeview.get_model().append(['Fecha '+str(partida.instancia), partida.nombre_local,
                                                      partida.nombre_visitante, partida.ganador, partida.id])

    def ver_detalle(self, widget):
        pass

    def gestionar_resultado(self, widget):
        opc = {'porresultadofinal': GestionarFinal, 'porpuntuacion': GestionarPuntos, 'porsets': GestionarSets}
        model = self.treeview.get_model()
        cursor, _ = self.treeview.get_cursor()
        id_partida = model.get_value(model.get_iter(cursor), 4)
        dto_partida_seleccionada = filter(lambda x: x.id == id_partida, self.lista_partidas)[0]
        n = opc[dto_partida_seleccionada.tipo_puntuacion](id_partida, self.main_window)
        self.main_window.hide()

    def destroy(self, widget):
        self.volver(None)

    def volver(self, widget):
        self.main_window.hide()
        self.ventana_padre.show()

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

        local_presente = self.glade.get_object('checkbutton5').get_active()
        visitante_presente = self.glade.get_object('checkbutton6').get_active()
        if not (local_presente or visitante_presente):
            mensajes_error.append('Debe haber al menos un participante presente.')

        if not self.permitir_empate:
            if (local == visitante) and local_presente and visitante_presente:
                mensajes_error.append('En esta competencia no esta permitido el empate.')

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
        self.nombre_local = datos_partida.nombre_local
        self.nombre_visitante = datos_partida.nombre_visitante
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
        ganadores = []
        lista_sets = self.lista_widgets[:self.cantidad_de_sets]
        for i, diccionario in enumerate(lista_sets):
            if round(self.cantidad_de_sets/2.) in [ganadores.count(True), ganadores.count(False)]:
                break # Si ya hay un ganador porque el otro no puede darlo vuelta
            valor_local = diccionario['local'].get_text()
            valor_visitante = diccionario['visitante'].get_text()
            if '' in [valor_local, valor_visitante]:
                if valor_local == '':
                    mensajes_error.append('Debe ingresar un valor para {} en el set {}.'.format(self.nombre_local,i+1))
                if valor_visitante == '':
                    mensajes_error.append('Debe ingresar un valor para {} en el set {}.'.format(self.nombre_visitante,i+1))
                continue # Si ocurre un error, salta al proximo elemento de la lista

            puntos_local = int(valor_local)
            puntos_visitante = int(valor_visitante)
            if puntos_local == puntos_visitante:
                mensajes_error.append('Debe haber un ganador en el set {}.'.format(i+1))
                continue # Si ocurre un error, salta al proximo elemento de la lista
            lista_dto_sets.append(DTOSet(None, puntos_local, puntos_visitante, i+1))
            ganadores.append(puntos_local>puntos_visitante)

        local_presente = self.glade.get_object('checkbutton4').get_active()
        visitante_presente = self.glade.get_object('checkbutton3').get_active()

        if not (local_presente or visitante_presente):
            mensajes_error.append('Debe haber al menos un participante presente.')

        if mensajes_error:
            self.mostrar_error(*mensajes_error)
            return

        dto = DTOResultado(None, self.id_partida, 'porsets', local_presente, visitante_presente, None, None,
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

class MostrarResultadoPuntos:
    """Interfaz para mostrar un resultado de tipo puntuacion"""
    def __init__(self, id_partida):
        self.id_partida = id_partida
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button5').connect('clicked', self.volver)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)[0]
        datos_resultado = GestorPartida.get_instance().listar_resultado(id_partida)
        self.glade.get_object('label36').set_text(datos_partida.nombre_local)
        self.glade.get_object('label37').set_text(datos_partida.nombre_visitante)
        self.glade.get_object('label35').set_text(str(datos_resultado.resultado_local))
        self.glade.get_object('label34').set_text(str(datos_resultado.resultado_visitante))

        self.main_window = self.glade.get_object('resultado_puntos')
        self.main_window.connect('destroy', self.destroy)
        self.main_window.show_all()

    def destroy(self, widget):
        self.volver(None)

    def volver(self, widget):
        self.main_window.hide()

class MostrarResultadoSets:
    """Interfaz para mostrar un resultado de tipo sets"""
    def __init__(self, id_partida):
        self.id_partida = id_partida
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button4').connect('clicked', self.volver)

        datos_partida = GestorPartida.get_instance().listar_partidas(id_partida=id_partida)[0]
        datos_resultado = GestorPartida.get_instance().listar_resultado(id_partida)
        self.glade.get_object('label14').set_text(datos_partida.nombre_local)
        self.glade.get_object('label15').set_text(datos_partida.nombre_visitante)

        lista_widgets = [
            {
             'local': self.glade.get_object('label'+str(index)),
             'visitante': self.glade.get_object('label'+str(index+9))
            }
                        for index in range(16, 25)]
        for dto_set in datos_resultado.lista_dto_sets:
            lista_widgets[dto_set.numero_de_set-1]['local'].set_text(str(dto_set.puntaje_local))
            lista_widgets[dto_set.numero_de_set-1]['visitante'].set_text(str(dto_set.puntaje_visitante))

        self.main_window = self.glade.get_object('resultado_sets')
        self.main_window.connect('destroy', self.destroy)
        self.main_window.show_all()

    def destroy(self, widget):
        self.volver(None)

    def volver(self, widget):
        self.main_window.hide()

class MostrarTablaPosiciones:
    """Interfaz para mostrar un resultado de tipo puntuacion"""
    def __init__(self, id_competencia):
        self.id_competencia = id_competencia
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\\resultado.glade')
        self.glade.get_object('button5').connect('clicked', self.volver)

        self.treeview = self.glade.get_object('treeview2')
        self.treeview.get_model().clear()
        datos_tabla = GestorCompetencia.get_instance().generar_tabla_posiciones(id_competencia)
        for dto in datos_tabla:
            datos = [
                dto.nombre, dto.puntos, dto.partidos_ganados, dto.partidos_empatados, dto.partidos_perdidos,
                dto.goles_a_favor, dto.goles_en_contra, dto.goles_a_favor-dto.goles_en_contra,
                dto.partidos_empatados+dto.partidos_ganados+dto.partidos_perdidos
            ]
            for i, dato in enumerate(datos):
                datos[i] = str(dato)
            self.treeview.get_model().append(datos)

        self.main_window = self.glade.get_object('tabla_posiciones')
        self.main_window.connect('destroy', self.destroy)
        self.main_window.show_all()

    def destroy(self, widget):
        self.volver(None)

    def volver(self, widget):
        self.main_window.hide()
