import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
# Crear un Blueprint
vistapodcast = Blueprint('idpodcast', __name__, template_folder='templates')

@vistapodcast.route('/podcast', methods=['GET', 'POST'])
@login_required
def vista_podcast():
    # Hacer la solicitud a la API
    response = requests.get(f"{API_URL}/tipo_podcast")
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        podcasts = response.json()
        # Agregar una descripción de ejemplo si no existe y asegurarse de que id_tipo esté presente
        for podcast in podcasts:
            if 'descripcion' not in podcast:
                podcast['descripcion'] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            if 'id_tipo' not in podcast:
                podcast['id_tipo'] = podcast.get('id', '')  # Usar 'id' si existe, o cadena vacía si no
    else:
        podcasts = []
        print(f"Error al obtener datos de la API: {response.status_code}")

    # Obtener el término de búsqueda si existe
    search_query = request.args.get('search', '').lower()

    # Filtrar los podcasts si hay un término de búsqueda
    if search_query:
        podcasts = [podcast for podcast in podcasts if search_query in podcast['nombre_tipo'].lower()]

    # Imprimir los podcasts que se van a renderizar
    print("Podcasts a renderizar:", podcasts)

    return render_template('podcast.html', podcasts=podcasts)

def eliminar_podcast_por_id(id_tipo_podcast):
    print(f"Eliminando podcast con ID: {id_tipo_podcast}")
    
    # Aquí puedes agregar un print para mostrar el ID que se va a eliminar
    print(f"ID del podcast a eliminar: {id_tipo_podcast}")
    
    payload = {
        "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "tipo_podcast",
            "where_condition": f"id_tipo_podcast = {id_tipo_podcast}"
        }
    }
    
    # Imprimir el payload que se enviará a la API
    print("Payload enviado:", payload)
    
    try:
        print("Enviando solicitud de eliminación a la API con payload:", payload)
        response = requests.post(f"{API_URL}/procedures/execute", json=payload)
        response.raise_for_status()
        print("El podcast fue eliminado exitosamente.")
        return True
    except requests.RequestException as e:
        print(f"Error al eliminar el podcast: {e}")
        if e.response is not None:
            print("Respuesta del servidor:", e.response.text)
        return False

@vistapodcast.route('/podcast', methods=['POST'])
@login_required
def eliminar_podcast():
    data = request.json
    print("Datos recibidos para eliminar podcast:", data)
    id_tipo_podcast = data.get('id_tipo_podcast')
    if not id_tipo_podcast:
        print("Error: ID de podcast no proporcionado.")
        return jsonify({"error": "ID de podcast no proporcionado"}), 400

    if eliminar_podcast_por_id(id_tipo_podcast):
        return jsonify({"message": "Podcast eliminado exitosamente"}), 200
    else:
        return jsonify({"error": "Error al eliminar el podcast"}), 500

