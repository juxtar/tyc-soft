import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
from main import agregar_cuadro_error, Interfaz

class ListarMisCompetencias(Interfaz):
    """Interfaz para buscar y listar las competencias de un usuario"""
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.glade = gtk.Builder()
        self.glade.add_from_file('glade\competencia.glade')
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

        parametros = {  'nombre': nombre_box.get_text(),
                        'id_usuario': self.id_usuario,
                        'deporte': deporte_box.get_model()[deporte_box.get_active()][0],
                        'modalidad': modalidad_box.get_model()[modalidad_box.get_active()][0],
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
            modelo.append([competencia.nombre, competencia.deporte, competencia.modalidad, competencia.estado, competencia.nombre_usuario])

    def volver(self, widget):
        self.destroy(None) # Temporal por esta entrega

    def ver_competencia(self, widget):
        pass

    def nueva_competencia(self, widget):
        pass

    def destroy(self, widget):
        gtk.main_quit()

if __name__ == '__main__':
    a = ListarMisCompetencias(0)
    gtk.main()