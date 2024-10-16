from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistavervideo = Blueprint('idvervideo', __name__, template_folder='templates')
 
@vistavervideo.route('/vervideo', methods=['GET'])
def vista_ver_video():
    tipo_video_id = request.args.get('tipo_video_id')
    print(f"tipo_video_id recibido: {tipo_video_id}")
    
    if not tipo_video_id:
        return redirect(url_for('idvideos.vista_videos'))

    # Obtener videos relacionados al tipo de video
    response = requests.get(f"{API_URL}/videos")
    if response.status_code != 200:
        return "Error al obtener los videos", 500

    todos_videos = response.json()
    videos = [v for v in todos_videos if v['id_tipo_video'] == int(tipo_video_id)]
    print(f"Videos filtrados: {videos}")

    # Si se seleccionó un video específico
    video_id = request.args.get('video_id')
    video_seleccionado = None
    if video_id:
        video_seleccionado = next((v for v in videos if v['id'] == int(video_id)), None)
    elif videos:
        video_seleccionado = videos[0]

    return render_template('vervideo.html', videos=videos, video_seleccionado=video_seleccionado, tipo_video_id=tipo_video_id)


""" @vistavervideo.route('/vervideo', methods=['GET'])
def vista_ver_video():
    tipo_video_id = request.args.get('tipo_video_id')
    video_id = request.args.get('video_id')
    search_query = request.args.get('search', '').lower()

    print(f"tipo_video_id recibido: {tipo_video_id}")
    
    if not tipo_video_id:
        return redirect(url_for('idvideos.vista_videos'))

    # Obtener videos relacionados al tipo de video
    response = requests.get(f"{API_URL}/videos")
    if response.status_code != 200:
        return "Error al obtener los videos", 500

    todos_videos = response.json()
    videos = [v for v in todos_videos if v['id_tipo_video'] == int(tipo_video_id)]
    
    # Aplicar filtro de búsqueda si existe
    if search_query:
        videos = [v for v in videos if search_query in v['titulo'].lower()]

    print(f"Videos filtrados: {videos}")

    # Si se seleccionó un video específico
    video_seleccionado = None
    if video_id:
        video_seleccionado = next((v for v in videos if v['id'] == int(video_id)), None)
    elif videos:
        video_seleccionado = videos[0]

    return render_template('vervideo.html', 
                           videos=videos, 
                           video_seleccionado=video_seleccionado, 
                           tipo_video_id=tipo_video_id,
                           search_query=search_query) """
