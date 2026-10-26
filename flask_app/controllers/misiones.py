from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.usuario import Usuario
from flask_app.models.mision import Mision


@app.route('/nueva_mision')
def nueva_mision():
    if 'usuario_id' not in session:
        return redirect('/')
    usuario_en_sesion = Usuario.get_one({'id': session['usuario_id']})
    return render_template('nuevo.html', usuario=usuario_en_sesion)


@app.route('/viaje/<int:id>')
def ver_viaje(id):
    if 'usuario_id' not in session:
        return redirect('/')
    viaje = Viaje.get_one({'id': id})
    if viaje is None:
        return redirect('/dashboard')
    return render_template('ver_viaje.html', viaje=viaje)


@app.route('/editar_viaje/<int:id>')
def editar_viaje(id):
    if 'usuario_id' not in session:
        return redirect('/')
    viaje = Viaje.get_one({'id': id})
    if viaje is None:
        return redirect('/dashboard')
    return render_template('editar.html', viaje=viaje)


@app.route('/crear_viaje', methods=['POST'])
def crear_viaje():
    if 'usuario_id' not in session:
        return redirect('/')
    destino = request.form.get('destino', '').strip()
    fecha_inicio = request.form.get('fecha_inicio', '').strip()
    fecha_termino = request.form.get('fecha_termino', '').strip()
    itinerario = request.form.get('itinerario', '').strip()
    if not destino or not fecha_inicio or not fecha_termino or not itinerario:
        flash('Todos los campos son obligatorios.', 'viaje')
        return redirect('/nuevo_viaje')
    if len(itinerario) > 40:
        flash('El itinerario no puede superar los 40 caracteres.', 'viaje')
        return redirect('/nuevo_viaje')
    datos_viaje = {
        'destino': destino,
        'fecha_inicio': fecha_inicio,
        'fecha_termino': fecha_termino,
        'itinerario': itinerario,
        'usuarios_id': session['usuario_id']
    }
    Viaje.save(datos_viaje)
    return redirect('/dashboard')

@app.route('/eliminar_viaje/<int:id>')
def eliminar_viaje(id):
    if 'usuario_id' not in session:
        return redirect('/')

    Viaje.delete({'id': id})

    return redirect('/dashboard')

@app.route('/actualizar_viaje/<int:id>', methods=['POST'])
def actualizar_viaje(id):
    if 'usuario_id' not in session:
        return redirect('/')

    destino = request.form.get('destino', '').strip()
    fecha_inicio = request.form.get('fecha_inicio', '').strip()
    fecha_termino = request.form.get('fecha_termino', '').strip()
    itinerario = request.form.get('itinerario', '').strip()

    if not destino or not fecha_inicio or not fecha_termino or not itinerario:
        flash('Todos los campos son obligatorios.', 'viaje')
        return redirect(f'/editar_viaje/{id}')

    if len(itinerario) > 40:
        flash('El itinerario no puede superar los 40 caracteres.', 'viaje')
        return redirect(f'/editar_viaje/{id}')

    datos_viaje = {
        'id': id,
        'destino': destino,
        'fecha_inicio': fecha_inicio,
        'fecha_termino': fecha_termino,
        'itinerario': itinerario
    }

    Viaje.update(datos_viaje)
    return redirect('/dashboard')