import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from os import path
from pyged.gestores.dtos import DTOCompetencia, DTOLugar
from pyged.gestores.excepciones import NombreExistente, FaltaDeDatos
from pyged.gestores.gestorcompetencia import GestorCompetencia
from pyged.gestores.gestorlugar import GestorLugar
from pyged.gestores.gestorpartida import GestorPartida
from main import agregar_cuadro_error, Interfaz
from aviso import Exito
from resultado import MostrarTablaPosiciones, MostrarFixture
from participante import VerParticipantes
import re

def obtener_descendientes(widget, tipo):
    """Busca descendientes del widget del tipo especificado"""
    descendientes = []
    try:
        for hijo in widget.get_children():
            if type(hijo).__name__ == tipo:
                descendientes.append(hijo)
            else:
                descendientes += obtener_descendientes(hijo, tipo)
    except AttributeError:
        return []
    except TypeError:
        hijo = widget.get_children()
        if type(hijo).__name__ == tipo:
            descendientes.append(hijo)
    finally:
        return descendientes

class VerCompetencia(Interfaz):
    """ Muestra informacion de la competencia y acceso a otras interfaces para el manejo de la misma
    """
    def __init__(self, id_competencia, ventana_padre):
        self.id_competencia = id_competencia
        self.ventana_padre = ventana_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\competencia.glade')
        self.glade.get_object('button10').connect('clicked', self.ver_participantes)
        self.glade.get_object('button9').connect('clicked', self.volver)
        self.glade.get_object('button8').connect('clicked', self.generar_fixture)
        self.glade.get_object('button7').connect('clicked', self.mostrar_tabla)
        self.glade.get_object('button6').connect('clicked', self.mostrar_fixture)

        self.actualizar()

    def actualizar(self):
        datos_competencia = GestorCompetencia.get_instance().listar_competencias(id_competencia=self.id_competencia)[0]
        self.glade.get_object('NombreCompetencia').set_text(datos_competencia.nombre)
        self.glade.get_object('modalidad').set_text(datos_competencia.tipo)
        self.glade.get_object('deporte').set_text(datos_competencia.deporte)
        self.glade.get_object('estado').set_text(datos_competencia.estado)
        self.estado_competencia = datos_competencia.estado
        self.tipo_competencia = datos_competencia.tipo
        if self.tipo_competencia != 'liga':
            self.glade.get_object('button7').set_sensitive(False)

        lista_de_partidas = GestorPartida.get_instance().listar_partidas(id_competencia = self.id_competencia)
        self.glade.get_object("treeview2").get_model().clear()
        for partida in lista_de_partidas:
            if 'Dummy' in partida.nombre_visitante or 'Dummy' in partida.nombre_local:
                lista_de_partidas.remove(partida)
        for partida in lista_de_partidas[:5]:
            if partida.estado != 'Finalizada':
                self.glade.get_object("treeview2").get_model().append([partida.nombre_local, partida.nombre_visitante])

        self.main_window = self.glade.get_object('ver_competencia')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def destroy(self, widget):
        gtk.main_quit()

    def volver(self, widget):
        self.main_window.hide()
        self.ventana_padre.show()

    def ver_participantes(self, widget):
        n = VerParticipantes(self.id_competencia, self.main_window)
        self.main_window.hide()

    def mostrar_tabla(self, widget):
        if self.estado_competencia in ['Creada', 'Planificada']:
            self.mostrar_error('No se han jugado partidos en la competencia.')
            return
        n = MostrarTablaPosiciones(self.id_competencia)

    def generar_fixture(self, widget):
        if self.tipo_competencia != 'liga':
            self.mostrar_error('No esta implementado generar fixture para eliminatorias.')
            return
        try:
            exito = GestorCompetencia.get_instance().generar_fixture(self.id_competencia)
            if exito is 1:
                self.estado_competencia = 'Planificada'
                self.glade.get_object('estado').set_text('Planificada')
                Exito(self)
        except FaltaDeDatos as e:
            self.mostrar_error(e.mensaje)

    def mostrar_fixture(self, widget):
        if self.estado_competencia == 'Creada':
            self.mostrar_error('No se han planificado partidas todavia.')
            return
        n = MostrarFixture(self.id_competencia, self)
        self.main_window.hide()

class ListarMisCompetencias(Interfaz):
    """Interfaz para buscar y listar las competencias de un usuario"""
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\competencia.glade')
        self.glade.get_object('botonBuscar').connect('clicked', self.buscar)
        self.glade.get_object('button1').connect('clicked', self.volver)
        self.glade.get_object('button2').connect('clicked', self.ver_competencia)
        self.glade.get_object('button3').connect('clicked', self.nueva_competencia)

        self.main_window = self.glade.get_object('listar_competencia')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def buscar(self, widget):
        nombre_box = self.glade.get_object('entry1')
        deporte_box = self.glade.get_object('comboDeporte')
        modalidad_box = self.glade.get_object('comboModal')
        estado_box = self.glade.get_object('comboEstado')

        modalidad = modalidad_box.get_model()[modalidad_box.get_active()][0]
        if modalidad == 'Eliminatoria Simple':
            modalidad = 'eliminatoriasimple'
        elif modalidad == 'Eliminatoria Doble':
            modalidad = 'eliminatoriadoble'
        elif modalidad == 'Liga':
            modalidad = 'liga'

        parametros = {  'nombre': nombre_box.get_text(),
                        'id_usuario': self.id_usuario,
                        'deporte': deporte_box.get_model()[deporte_box.get_active()][0],
                        'modalidad': modalidad,
                        'estado': estado_box.get_model()[estado_box.get_active()][0]
                    }

        # Reemplazar los valores vacios por None
        for key, value in parametros.items():
            if value == '':
                parametros[key] = None

        lista_competencias = GestorCompetencia.get_instance().listar_competencias(id_competencia=None, **parametros)

        modelo = self.glade.get_object('treeview1').get_model()
        modelo.clear()
        for competencia in lista_competencias:
            modelo.append([competencia.nombre, competencia.deporte, competencia.tipo, competencia.estado,
                           competencia.nombre_usuario, competencia.id])

    def volver(self, widget):
        self.destroy(None) # Temporal por esta entrega

    def ver_competencia(self, widget):
        model = self.glade.get_object('treeview1').get_model()
        cursor, _ = self.glade.get_object('treeview1').get_cursor()
        try:
            id_competencia = model.get_value(model.get_iter(cursor), 5)
            n = VerCompetencia(id_competencia, self.main_window)
            self.main_window.hide()
        except TypeError:
            self.mostrar_error('Debe seleccionar una competencia.')

    def nueva_competencia(self, widget):
        self.main_window.hide()
        n = NuevaCompetencia(self.id_usuario, self.main_window)

    def destroy(self, widget):
        gtk.main_quit()


class NuevaCompetencia(Interfaz):
    """Interfaz para crear una nueva competencia"""
    def __init__(self, id_usuario, ventana_padre):
        self.id_usuario = id_usuario
        self.ventana_padre = ventana_padre
        self.glade = gtk.Builder()
        self.glade.add_from_file(path.dirname( path.abspath(__file__) )+'\glade\competencia.glade')
        self.glade.get_object('button4').connect('clicked', self.volver)
        self.glade.get_object('button5').connect('clicked', self.aceptar)

        deportes_cargados = GestorCompetencia.get_instance().listar_deportes()
        self.glade.get_object('comboDeporte1').get_model().clear()
        for deporte in deportes_cargados:
            self.glade.get_object('comboDeporte1').append_text(deporte)

        botones = obtener_descendientes(self.glade.get_object('vbox1'), 'RadioButton')
        botones.append(self.glade.get_object('empate'))
        for b in botones:
            b.connect('toggled', self.dinamizar)
        self.glade.get_object('entry2').connect('changed', self.dinamizar)

        lista_lugares = GestorLugar.get_instance().listar_lugar(id_usuario)
        for lugar in lista_lugares:
            cuadrolugar = CuadroLugar(lugar.id, lugar.nombre)
            cuadrolugar.disponibilidad.connect('changed', self.dinamizar)
            self.glade.get_object('lugares').pack_start(cuadrolugar, False, True, 2)
            cuadrolugar.show_all()

        self.main_window = self.glade.get_object('nueva_modificar_competencia')
        self.main_window.connect('destroy', self.destroy)
        self.infobar, boton_cerrar = agregar_cuadro_error(self.main_window)
        boton_cerrar.connect('clicked', self.cerrar_error)
        self.main_window.show_all()

    def volver(self, widget):
        self.main_window.hide()
        self.ventana_padre.show()

    def dinamizar(self, widget):
        nombre = gtk.Buildable.get_name(widget)
        if nombre == 'empate':
            self.glade.get_object('viewport4').set_sensitive(widget.get_active())
        elif nombre in ['liga', 'eliminatoriasimple', 'eliminatoriadoble']:
            self.glade.get_object('label14').set_text('Modalidad {}'.format(widget.get_label()))
            if nombre == 'liga':
                tabla = self.glade.get_object('table1')
                if widget.get_active():
                    tabla.show()
                else:
                    tabla.hide()
        elif nombre == 'porsets':
            cantidad_sets = self.glade.get_object('cantSets0')
            if widget.get_active():
                self.glade.get_object('viewport4').set_sensitive(False)
                cantidad_sets.show()
            else:
                cantidad_sets.hide()
                self.glade.get_object('viewport4').set_sensitive(self.glade.get_object('empate').get_active())
            self.glade.get_object('empate').set_sensitive(not widget.get_active())

        elif nombre == 'porpuntuacion':
            presentismo = self.glade.get_object('cantPunt0')
            if widget.get_active():
                presentismo.show()
            else:
                presentismo.hide()
        elif nombre == 'entry2':
            texto = widget.get_text().upper()
            widget.set_text(texto[:100])
        elif nombre is None:
            texto = widget.get_text()
            texto = filter(str.isdigit, texto)
            if len(texto) > 2:
                texto = texto[:2]
            widget.set_text(texto)

    def aceptar(self, widget):
        deporte_box = self.glade.get_object('comboDeporte1')
        deporte = deporte_box.get_model()[deporte_box.get_active()][0]

        nombre = self.glade.get_object('entry2').get_text()

        mensaje_errores = []
        if nombre == '':
            mensaje_errores.append('Debe ingresar un nombre para la competencia.')
        if not re.match(r"^[A-Z0-9]+( [A-Z0-9]+)*$", nombre):
            mensaje_errores.append('Nombre invalido. Solo puede contener letras, numeros y espacios.')
        if deporte_box.get_active() == -1:
            mensaje_errores.append('Debe ingresar un deporte para la competencia.')

        for lugar in self.glade.get_object('lugares').get_children():
            if lugar.get_active():
                if lugar.get_disponibilidad() == '':
                    mensaje_errores.append('Debe ingresar la disponibilidad para {}.'.format(lugar.get_label()))
                    continue
                if int(lugar.get_disponibilidad()) == 0:
                    mensaje_errores.append('La disponibilidad de {} no puede ser 0.'.format(lugar.get_label()))

        puntos_empate = self.glade.get_object('spinEmpate').get_value()
        puntos_victoria = self.glade.get_object('spinbutton4').get_value()
        puntos_presentarse = self.glade.get_object('spinbutton5').get_value()
        permitir_empate = self.glade.get_object('empate').get_active()

        if puntos_empate >= puntos_victoria and permitir_empate:
            mensaje_errores.append('La cantidad de puntos por ganar debe ser mayor que la cantidad de puntos por empate.')
        if puntos_presentarse > puntos_victoria:
            mensaje_errores.append('La cantidad de puntos por presentarse no puede superar la de un partido ganado.')
        if not puntos_victoria:
            mensaje_errores.append('La cantidad de puntos por ganar no puede ser 0.')

        datos_lugares = [
            {'id_lugar':lugar.id, 'nombre':lugar.nombre, 'disponibilidad':lugar.get_disponibilidad(),
             'descripcion':None}
            for lugar in self.glade.get_object('lugares').get_children() if lugar.get_active()
            ]
        if not datos_lugares:
            mensaje_errores.append('Debe seleccionar al menos un lugar para la competencia.')

        if mensaje_errores:
            self.mostrar_error(*mensaje_errores)
            return

        modalidades = self.glade.get_object('liga').get_group()
        modalidad = None
        for boton in modalidades:
            if boton.get_active():
                modalidad = gtk.Buildable.get_name(boton)
                break

        puntuaciones = self.glade.get_object('porsets').get_group()
        puntuacion = None
        for boton in puntuaciones:
            if boton.get_active():
                puntuacion = gtk.Buildable.get_name(boton)

        cantidad_sets = self.glade.get_object('spinbutton1').get_value()
        tantos_presentismo = self.glade.get_object('spinbutton2').get_value()
        text_buffer = self.glade.get_object("textview1").get_buffer()
        reglamento = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())

        lugares = [DTOLugar(**datos) for datos in datos_lugares]

        dto = DTOCompetencia(None, nombre, puntuacion, 'Creada', reglamento, self.id_usuario, None, modalidad,
                             cantidad_sets, puntos_presentarse, puntos_victoria, puntos_empate, deporte,
                             lugares, tantos_presentismo, permitir_empate)

        try:
            exito = GestorCompetencia.get_instance().nueva_competencia(dto)
            if exito is 1:
                Exito(self)
        except NombreExistente:
            self.mostrar_error('Ya existe una competencia con ese nombre.')

    def destroy(self, widget):
        gtk.main_quit()


class CuadroLugar(gtk.HBox):
    """Muestra el nombre de un lugar con su cuadro para disponibilidad"""
    def __init__(self, id_lugar, nombre):
        super(CuadroLugar, self).__init__()
        self.nombre = nombre
        self.id = id_lugar
        
        self.check = gtk.CheckButton(nombre)
        self.disponibilidad = gtk.Entry()
        self.disponibilidad.set_width_chars(3)
        self.pack_start(self.check, True, True, 15)
        self.pack_start(self.disponibilidad, False, True, 0)

    def get_disponibilidad(self):
        return self.disponibilidad.get_text()

    def get_active(self):
        return self.check.get_active()

    def get_label(self):
        return self.check.get_label()

    def set_label(self, text):
        self.check.set_label(text)

if __name__ == '__main__':
    a = NuevaCompetencia(0)
    gtk.main()