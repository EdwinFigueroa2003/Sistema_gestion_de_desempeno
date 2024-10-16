from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistapodcast = Blueprint('idpodcast', __name__, template_folder='templates')

@vistapodcast.route('/podcast', methods=['GET', 'POST'])
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