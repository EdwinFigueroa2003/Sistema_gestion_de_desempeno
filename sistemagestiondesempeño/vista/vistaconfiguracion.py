import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, flash
import requests
from configBd import API_URL
from flask_login import login_required

# Crear un Blueprint
vistaconfiguracion = Blueprint('idconfiguracion', __name__, template_folder='templates')

# Configuración para las imágenes
UPLOAD_FOLDER = 'static/uploads'  # Carpeta donde se guardan las imágenes en el servidor
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Asegurarse de que la carpeta de subida exista
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@vistaconfiguracion.route('/configuracion', methods=['GET', 'POST'])
@login_required
def vista_configuracion():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return redirect(url_for('idvistalogin.vista_login'))
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        facultad = request.form.get('facultad')
        cargo = request.form.get('cargo')
        foto = request.form.get('foto_usu')

        # Preparar los datos para la API
        update_data = {
            "procedure": "update_json_entity",
            "parameters": {
                "table_name": "usuario",
                "json_data": {
                    "nombre": nombre,
                    "facultad": facultad,
                    "fk_cargo_usu": int(cargo) if cargo.isdigit() else None,
                    "foto_usu": foto if foto else "default.jpg"
                },
                "where_condition": f"id_usuario = {id_usuario}"
            }
        }

        # Realizar la actualización del usuario
        try:
            print("Datos a enviar:", update_data)
            response = requests.post(f"{API_URL}/procedures/execute", json=update_data)
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            print("Datos actualizados correctamente.")
        except requests.exceptions.HTTPError as http_err:
            print(f"Error al actualizar los datos del usuario: {http_err}")
            return render_template('configuracion.html', error="Error al actualizar los datos. Intente nuevamente.")
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return render_template('configuracion.html', error="Error de conexión. Intente nuevamente.")

    # Obtener los datos del usuario desde la API
    try:
        response = requests.get(f"{API_URL}/usuario/id_usuario/{id_usuario}")
        response.raise_for_status()
        datos_usuario = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos del usuario: {e}")
        datos_usuario = {}

    return render_template('configuracion.html', datos_usuario=datos_usuario)
