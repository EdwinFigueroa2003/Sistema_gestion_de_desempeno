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
        #print(cursos)
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


@vistacursos.route('/cursos/eliminar/<int:id_tipo_curso>', methods=['GET'])
@login_required
def eliminar_curso(id_tipo_curso):
    if session['usuario']['fk_rol_usu'] != 1:
        return redirect(url_for('idcursos.vista_cursos'))

    print(f"Intentando eliminar el curso con ID: {id_tipo_curso}")  # Print para verificar el ID del curso

    try:
        payload = {
            "procedure": "delete_json_entity",
            "parameters": {
                "table_name": "tipo_curso",
                "where_condition": f"id_tipo_curso = {id_tipo_curso}"
            }
        }
        print('Payload para eliminar:', payload)  # Print para verificar el payload

        response = requests.post(f"{API_URL}/procedures/execute", json=payload)
        print('Respuesta de la API:', response.status_code, response.text)  # Print para verificar la respuesta de la API

        return redirect(url_for('idcursos.vista_cursos'))
    except requests.RequestException as e:
        print(f"Error al eliminar el curso: {e}")
        return redirect(url_for('idcursos.vista_cursos'))

