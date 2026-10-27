from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.mision import Mision


@app.route('/nueva_mision')
def nueva_mision():
    if 'usuario_id' not in session:
        return redirect('/')

    return render_template('nuevo.html')


@app.route('/crear_mision', methods=['POST'])
def crear_mision():
    if 'usuario_id' not in session:
        return redirect('/')

    nombre = request.form.get('nombre', '').strip()
    fecha = request.form.get('fecha', '').strip()
    voluntarios = request.form.get('voluntarios', '').strip()
    descripcion = request.form.get('descripcion', '').strip()

    if not nombre or not fecha or not voluntarios or not descripcion:
        flash('Todos los campos son obligatorios.', 'mision')
        return redirect('/nueva_mision')

    try:
        voluntarios = int(voluntarios)
    except ValueError:
        flash('El número de voluntarios debe ser válido.', 'mision')
        return redirect('/nueva_mision')

    if voluntarios < 2 or voluntarios > 20:
        flash('Los voluntarios deben ser entre 2 y 20.', 'mision')
        return redirect('/nueva_mision')

    datos_mision = {
        'nombre': nombre,
        'fecha': fecha,
        'voluntarios': voluntarios,
        'descripcion': descripcion,
        'usuario_id': session['usuario_id']
    }

    Mision.save(datos_mision)
    return redirect('/dashboard')


@app.route('/ver_mision/<int:id>')
def ver_mision(id):
    if 'usuario_id' not in session:
        return redirect('/')

    mision = Mision.get_one({'id': id})

    if mision is None:
        return redirect('/dashboard')

    return render_template('ver_mision.html', mision=mision)


@app.route('/editar_mision/<int:id>')
def editar_mision(id):
    if 'usuario_id' not in session:
        return redirect('/')

    mision = Mision.get_one({'id': id})

    if mision is None:
        return redirect('/dashboard')

    if mision.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    return render_template('editar.html', mision=mision)


@app.route('/eliminar_mision/<int:id>', methods=['POST'])
def eliminar_mision(id):
    if 'usuario_id' not in session:
        return redirect('/')

    mision = Mision.get_one({'id': id})

    if mision is None:
        return redirect('/dashboard')

    if mision.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    Mision.delete({'id': id})
    return redirect('/dashboard')


@app.route('/actualizar_mision/<int:id>', methods=['POST'])
def actualizar_mision(id):
    if 'usuario_id' not in session:
        return redirect('/')

    mision = Mision.get_one({'id': id})

    if mision is None:
        return redirect('/dashboard')

    if mision.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    nombre = request.form.get('nombre', '').strip()
    fecha = request.form.get('fecha', '').strip()
    voluntarios = request.form.get('voluntarios', '').strip()
    descripcion = request.form.get('descripcion', '').strip()

    if not nombre or not fecha or not voluntarios or not descripcion:
        flash('Todos los campos son obligatorios.', 'mision')
        return redirect(f'/editar_mision/{id}')

    try:
        voluntarios = int(voluntarios)
    except ValueError:
        flash('El número de voluntarios debe ser válido.', 'mision')
        return redirect(f'/editar_mision/{id}')

    if voluntarios < 2 or voluntarios > 20:
        flash('Los voluntarios deben ser entre 2 y 20.', 'mision')
        return redirect(f'/editar_mision/{id}')

    datos_mision = {
        'id': id,
        'nombre': nombre,
        'fecha': fecha,
        'voluntarios': voluntarios,
        'descripcion': descripcion
    }

    Mision.update(datos_mision)
    return redirect('/dashboard')
