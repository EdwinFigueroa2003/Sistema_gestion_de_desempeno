from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL 
# Crear un Blueprint
vistavideos = Blueprint('idvideos', __name__)

@vistavideos.route('/videos')
def vista_videos():
    # Obtener el término de búsqueda
    search_query = request.args.get('search', '').lower()

    # Hacer la solicitud a la API
    response = requests.get(f"{API_URL}/tipo_video")
    videos = response.json() if response.status_code == 200 else []
    
    # Filtrar los videos si hay un término de búsqueda
    if search_query:
        filtered_videos = [video for video in videos if search_query in video['nombre'].lower()]
    else:
        filtered_videos = videos
    
    # Imprimir los videos filtrados para depuración
    print("Videos filtrados:", filtered_videos)
    
    return render_template('videos.html', videos=filtered_videos)
