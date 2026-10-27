from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.usuario import Usuario
from flask_app.models.mision import Mision
from flask_bcrypt import Bcrypt #Importamos bycrpt

bcrypt = Bcrypt(app) #Generamos un objeto llamado bcrypt

@app.route("/")
def inicio():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    misiones = Mision.get_all()
    return render_template('dashboard.html', todas_las_misiones=misiones)


#registro crear usuario
@app.route("/crear_usuario", methods=["POST"])
def crear_usuario():

     #para agregar un usuario lo primero que debo hacer es
    #recuperar la informacion desde el formulario
    #para hacer eso necesitamos el request.form
    #%(nombre)s, %(apellido)s, %(email)s,%(password)s

    #--- IMPORTANTE: TEORICAMENTE ANTES DE REGISTRAR UN NUEVO DATO
    #--- YO DEBERÍA VALIDAR QUE LOS DATOS INGRESADOS
    #--- SEAN VALIDOS

    if not Usuario.validar_registro(request.form):
        return redirect('/')

    #--- VALIDACIONES ---
    #Hasheamos la contraseña

    pass_hasheado = bcrypt.generate_password_hash(
        request.form['password']
    ).decode('utf-8')

    datos_usuario_registro = {
        "nombre": request.form ['nombre'],
        "apellido": request.form ['apellido'],
        "email": request.form ['email'],
        "password": pass_hasheado
        
    }

    nuevo_id = Usuario.save(datos_usuario_registro) #Recibiendo el ID del nuevo Usuario

    session['usuario_id'] = nuevo_id
    session['nombre'] = datos_usuario_registro['nombre']

    return redirect('/dashboard')




#inicio sesión 
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    #buscamos al usuario por su email
    email = request.form.get('email_inicio_sesion', '').strip()
    password = request.form.get('password_inicio_sesion', '')

    usuario = Usuario.get_by_email({'email': email})

    #si no existe o la contraseña no coincide, mostramos el mismo mensaje
    if not usuario or not bcrypt.check_password_hash(usuario.password, password):
        flash("E-mail o contraseña incorrectos", "inicio_sesion")
        return redirect('/')

    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    return redirect('/dashboard')



#cerrar sesión
@app.route('/cerrar_sesion')
def cerrar_sesion():

    session.clear()
    return redirect('/')