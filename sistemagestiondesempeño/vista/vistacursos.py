import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistacursos = Blueprint('idcursos', __name__, template_folder='templates')

@vistacursos.route('/cursos', methods=['GET'])
@login_required
def vista_cursos():
    try:
        cursos = requests.get(f"{API_URL}/tipo_curso").json()
    except requests.RequestException as e:
        print(f"Error al obtener los cursos: {e}")
        cursos = []
    return render_template('cursos.html', cursos=cursos)

@vistacursos.route('/cursos/crear', methods=['POST'])
@login_required
def crear_curso():
    if session['usuario']['fk_rol_usu'] != 1:
        return redirect(url_for('idcursos.vista_cursos'))  # Solo admin puede agregar

    nombre_tipo = request.form['nombre_tipo']
    imagen = request.files['imagen']

    # Lógica para guardar el curso en la base de datos, por ejemplo, usando una API
    try:
        # Aquí puedes subir la imagen a un servidor de archivos o almacenarla localmente
        #imagen_url = subir_imagen(imagen)  # Función ficticia para subir la imagen
        payload = {
            "nombre_tipo": nombre_tipo,
            #"imagen": imagen_url,
            "id_rol": 1  # El rol puede ser 1 si es administrado por el admin
        }
        requests.post(f"{API_URL}/tipo_curso", json=payload)
        return redirect(url_for('idcursos.vista_cursos'))
    except Exception as e:
        print(f"Error al crear el curso: {e}")
        return redirect(url_for('idcursos.vista_cursos'))
    
    # Establecer un directorio donde se almacenarán las imágenes
UPLOAD_FOLDER = 'static/img'  # Puedes cambiar esta ruta según tu estructura de proyecto

# Definir los tipos de archivo permitidos (por ejemplo, imágenes JPEG, PNG)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@vistacursos.route('/cursos/editar/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def editar_curso(curso_id):
    if session['usuario']['fk_rol_usu'] != 1:
        return redirect(url_for('idcursos.vista_cursos'))

    if request.method == 'POST':
        nombre_tipo = request.form['nombre_tipo']
        imagen = request.files['imagen']

        # Aquí actualizaríamos el curso en la base de datos
        try:
            #imagen_url = subir_imagen(imagen)  # Función ficticia para subir la imagen
            payload = {
                "nombre_tipo": nombre_tipo,
                #"imagen": imagen_url,
            }
            requests.put(f"{API_URL}/tipo_curso/{curso_id}", json=payload)
            return redirect(url_for('idcursos.vista_cursos'))
        except Exception as e:
            print(f"Error al editar el curso: {e}")
            return redirect(url_for('idcursos.vista_cursos'))
    
    # Obtener datos del curso para mostrar en el formulario
    try:
        curso = requests.get(f"{API_URL}/tipo_curso/{curso_id}").json()
    except requests.RequestException as e:
        print(f"Error al obtener el curso: {e}")
        curso = {}

    return render_template('vercurso.html', curso=curso)

@vistacursos.route('/cursos/eliminar/<int:curso_id>', methods=['GET'])
@login_required
def eliminar_curso(curso_id):
    if session['usuario']['fk_rol_usu'] != 1:
        return redirect(url_for('idcursos.vista_cursos'))

    # Lógica para eliminar el curso
    try:
        requests.delete(f"{API_URL}/tipo_curso/{curso_id}")
        return redirect(url_for('idcursos.vista_cursos'))
    except requests.RequestException as e:
        print(f"Error al eliminar el curso: {e}")
        return redirect(url_for('idcursos.vista_cursos'))

