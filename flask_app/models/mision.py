
#TODAS LAS CLASES IMPORTAN MYSQLCONNECTION
from flask_app.config.mysqlconnection import connectToMySQL

class Mision:

    #metodo constructor
    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.fecha = data.get('fecha')
        self.voluntarios = data.get('voluntarios')
        self.descripcion = data.get('descripcion')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.usuario_id = data.get('usuario_id')
        self.nombre_usuario = data.get('nombre_usuario')
        self.apellido_usuario = data.get('apellido_usuario')

    #para guardar un registro
    @classmethod
    def save(cls, data):
        query = """INSERT INTO misiones(nombre, fecha, voluntarios, descripcion, created_at, updated_at, usuario_id)VALUES(%(nombre)s, %(fecha)s, %(voluntarios)s, %(descripcion)s, NOW(), NOW(), %(usuario_id)s);"""
        return connectToMySQL('VoluntaMe').query_db(query, data)
    
    #Metodo para ver todos los registros
    @classmethod
    def get_all(cls):
        query = """SELECT misiones.*, usuarios.nombre AS nombre_usuario, usuarios.apellido AS apellido_usuario FROM misiones LEFT JOIN usuarios ON misiones.usuario_id = usuarios.id;"""
        misiones_en_bd = connectToMySQL('VoluntaMe').query_db(query)
        misiones = []
        if misiones_en_bd:
            for mision in misiones_en_bd:
                misiones.append(cls(mision))
        return misiones

    #Metodo para ver 1 registro
    @classmethod
    def get_one(cls, datos):
        query = """SELECT misiones.*, usuarios.nombre AS nombre_usuario, usuarios.apellido AS apellido_usuario FROM misiones LEFT JOIN usuarios ON misiones.usuario_id = usuarios.id WHERE misiones.id = %(id)s;"""
        misiones_en_db = connectToMySQL('VoluntaMe').query_db(query, datos)
        if not misiones_en_db:
            return None
        return cls(misiones_en_db[0])


    
    # Método para editar registro
    @classmethod
    def update(cls, datos):
        query = """UPDATE misiones SET nombre = %(nombre)s, fecha = %(fecha)s, voluntarios = %(voluntarios)s, descripcion = %(descripcion)s, updated_at = NOW() WHERE id = %(id)s;"""
        return connectToMySQL('VoluntaMe').query_db(query, datos)



    #Metodo para eliminar 1 registro
    @classmethod
    def delete(cls, datos):
        query = "DELETE FROM misiones WHERE id = %(id)s;"
        return connectToMySQL('VoluntaMe').query_db(query, datos)