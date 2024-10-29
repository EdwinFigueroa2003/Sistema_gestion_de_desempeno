from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session
import requests
from datetime import datetime
from configBd import API_URL
 
# Crear un Blueprint
vistaconcertaciondedisponibilidad = Blueprint('idconcertaciondedisponibilidad', __name__, template_folder='templates')
 
@vistaconcertaciondedisponibilidad.route('/concertaciondedisponibilidad', methods=['GET', 'POST'])
def vista_concertaciondedisponibilidad():
    # Obtener el id_usuario desde la sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return redirect(url_for('idvistalogin.vista_login'))  # Redirigir al login si no hay un usuario en sesión
    print(f"ID de usuario obtenido de la sesión: {id_usuario}")  # Debug

    if request.method == 'POST':
        data = request.get_json()

        # Imprime los datos para verificar qué se está enviando
        print("Datos enviados a la API:", data)

        proposito_data = {
            'id_usuario': id_usuario,  # Asegúrate de incluir id_usuario aquí
            'id_categoria': data.get('id_categoria', 4),
            'id_cargo': data.get('id_cargo', 1),
            'proposito': data.get('proposito', ''),
            'nuevo_prposito': data.get('nuevo_prposito', ''),
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d')
        }

        print("Datos que se enviarán a la API:", proposito_data)  # Debug

        try:
            response = requests.post(f'{API_URL}/proposito', json=proposito_data)
            response.raise_for_status()
            return jsonify({'success': True}), 200
        except requests.RequestException as e:
            print(f"Error al enviar los datos a la API: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    # Si es GET, solo muestra la plantilla
    return render_template('concertaciondedisponibilidad.html')
