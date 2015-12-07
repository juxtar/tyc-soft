from main import Singleton
from gestorbasededatos import GestorBaseDeDatos


class GestorUsuario(Singleton):
    """Realiza tareas correspondiente al manejo de clases Usuario"""
    def obtener_usuario(self, id_usuario):
        """Obtiene, teniendo un id de usuario, el objeto Usuario correspondiente a este id"""
        user = GestorBaseDeDatos.get_instance().listar_usuario(id_usuario)
        return user

    def agregar_competencia(self, id_usuario, competencia):
        user = GestorBaseDeDatos.get_instance().listar_usuario(id_usuario)
        user.competencias.append(competencia)
        GestorBaseDeDatos.get_instance().modificar_usuario()
