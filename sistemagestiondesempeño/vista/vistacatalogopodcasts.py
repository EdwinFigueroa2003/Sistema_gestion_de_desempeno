from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL

# Crear un Blueprint
vistacatalogopodcasts = Blueprint('idcatalogopodcasts', __name__, template_folder='templates')

@vistacatalogopodcasts.route('/catalogopodcasts', methods=['GET', 'POST'])
def vista_catalogopodcasts():
    # Obtener el tipo_podcast de los argumentos
    tipo_podcast = request.args.get('tipo_podcast')
    print("Tipo de podcast seleccionado:", tipo_podcast)

    # Hacer la solicitud a la API para obtener las series de podcast
    response_series = requests.get(f"{API_URL}/serie")
    
    if response_series.status_code == 200:
        series_podcast = response_series.json()
        print("Series de podcast obtenidas:", series_podcast)
    else:
        series_podcast = []
        print(f"Error al obtener series de podcast: {response_series.status_code}")

    # Filtrar las series de podcast si hay un tipo_podcast seleccionado
    if tipo_podcast:
        print(f"Filtrando series para el tipo de podcast: {tipo_podcast}")
        tipo_podcast_int = int(tipo_podcast)  # Convertir a entero
        print(f"Tipo de podcast como entero: {tipo_podcast_int}")
        series_podcast_filtradas = [serie for serie in series_podcast if serie['id_tipo_podcast'] == tipo_podcast_int]
        print("Series de podcast filtradas:", series_podcast_filtradas)
    else:
        series_podcast_filtradas = series_podcast

    # Mostrar información de las series filtradas
    for serie in series_podcast_filtradas:
        print(f"ID de serie: {serie['id_serie']}, Nombre: {serie['nombre_serie']}, ID Tipo Podcast: {serie['id_tipo_podcast']}")

    return render_template('catalogopodcasts.html', series_podcast=series_podcast_filtradas)
