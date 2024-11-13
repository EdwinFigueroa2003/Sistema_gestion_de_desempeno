from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, flash,session
import requests
from configBd import API_URL
from flask_login import login_required

# Crear un Blueprint
vistavervideo = Blueprint('idvervideo', __name__, template_folder='templates')
 
@vistavervideo.route('/vervideo', methods=['GET'])
@login_required
def vista_ver_video():
    tipo_video_id = request.args.get('tipo_video_id')
    #print(f"tipo_video_id recibido: {tipo_video_id}")
    
    if not tipo_video_id:
        return redirect(url_for('idvideos.vista_videos'))

    # Obtener videos relacionados al tipo de video
    response = requests.get(f"{API_URL}/videos")
    if response.status_code != 200:
        return "Error al obtener los videos", 500

    todos_videos = response.json()
    videos = [v for v in todos_videos if v['id_tipo_video'] == int(tipo_video_id)]
    #print(f"Videos filtrados: {videos}")

    # Si se seleccionó un video específico
    video_id = request.args.get('video_id')
    video_seleccionado = None
    if video_id:
        video_seleccionado = next((v for v in videos if v['id'] == int(video_id)), None)
    elif videos:
        video_seleccionado = videos[0]

    return render_template('vervideo.html', videos=videos, video_seleccionado=video_seleccionado, tipo_video_id=tipo_video_id)

@vistavervideo.route('/vervideo/editar/<int:video_id>', methods=['GET', 'POST'])
@login_required
def editar_video(video_id):
    if session['usuario']['fk_rol_usu'] != 1:
        flash("No tienes permiso para editar videos", "error")
        return redirect(url_for('idvervideo.vista_ver_video'))

    if request.method == 'POST':
        # Obtener datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        url = request.form['url']
        
        # Enviar solicitud de actualización a la API
        try:
            response = requests.put(f"{API_URL}/videos/{video_id}", json={'titulo': titulo, 'descripcion': descripcion, 'url': url})
            response.raise_for_status()
            flash("Video actualizado con éxito", "success")
            return redirect(url_for('idvervideo.vista_ver_video', video_id=video_id))
        except requests.RequestException as e:
            flash(f"Error al actualizar el video: {e}", "error")
            return redirect(url_for('idvervideo.vista_ver_video', video_id=video_id))

    # Obtener datos del video para prellenar el formulario
    video = requests.get(f"{API_URL}/videos/{video_id}").json()
    return render_template('editar_video.html', video=video)