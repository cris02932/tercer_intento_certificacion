#TODAS LAS CLASES IMPORTAN MYSQLCONNECTION
from flask_app.config.mysqlconnection import connectToMySQL
import re   # Importamos expresiones regulares
from flask import flash

# Objeto de expresión regular que usaremos para validar

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')


class Usuario:

    #metodo constructor
    def __init__(self, data):
        self.id = data.get('id')
        self.nombre = data.get('nombre')
        self.apellido = data.get('apellido')
        self.email = data.get('email')
        self.password = data.get('password')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    #para guardar un registro
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios
            (nombre, apellido, email, password, created_at, updated_at)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL('VoluntaMe').query_db(query, data)

    #Metodo para ver todos los registros
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios"
        usuarios_en_bd = connectToMySQL('VoluntaMe').query_db(query)
        #Lista vacia de usuarios se llena con class usuarios
        usuarios = []
        #por cada usuario que encuentre en usuarios_db
        for usuario in usuarios_en_bd:
            #voy a crear una instancia de la clase Usuario al final de la lista usuarios
            usuarios.append(cls(usuario))
        return usuarios

    #Metodo para ver 1 registro
    @classmethod
    def get_one(cls,datos):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        usuario_en_db = connectToMySQL('VoluntaMe').query_db(query,datos)
        print("USUARIO EN DB",usuario_en_db)
        if not usuario_en_db:
            return None
        return cls(usuario_en_db[0])

    #Metodo para editar registro
    @classmethod
    def update(cls, datos):
        query = "UPDATE usuarios SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s, password=%(password)s WHERE id = %(id)s;"
        return connectToMySQL('VoluntaMe').query_db(query, datos)

    #Metodo para eliminar 1 registro
    @classmethod
    def delete(cls, datos):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL('VoluntaMe').query_db(query, datos)



    @classmethod
    def get_by_email(cls, datos):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        usuario_en_db = connectToMySQL('VoluntaMe').query_db(query, datos)

        if not usuario_en_db:
            return None

        return cls(usuario_en_db[0])
        #Si no tenemos respuestas en la base de datos, va a retornar False


    #Usamos metodo estatico para validar los formularios
    @staticmethod
    def validar_registro(formulario):
        es_valido = True

        if len(formulario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "registro")
            es_valido = False

        if len(formulario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "registro")
            es_valido = False

        if not EMAIL_REGEX.match(formulario['email']):
            flash("El email no tiene un formato válido", "registro")
            es_valido = False
        elif Usuario.get_by_email({'email': formulario['email']}):
            print(Usuario.get_by_email({'email': formulario['email']}))
            flash("Ya existe una cuenta con ese email", "registro")
            es_valido = False

        if formulario['password'] != formulario['password_conf']:
            flash("Las contraseñas no coinciden", "registro")
            es_valido = False

        return es_valido