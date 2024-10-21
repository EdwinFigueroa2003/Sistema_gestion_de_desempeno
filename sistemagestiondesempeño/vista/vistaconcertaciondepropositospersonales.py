from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
import requests
from datetime import datetime
from configBd import API_URL

# Crear un Blueprint
vistaconcertaciondepropositospersonales = Blueprint('idconcertaciondepropositospersonales', __name__, template_folder='templates')

@vistaconcertaciondepropositospersonales.route('/concertaciondepropositospersonales', methods = ['GET', 'POST'])
def vista_concertaciondepropositospersonales():
    if request.method == 'POST':
        data = request.get_json()

        # Imprime los datos para verificar qué se está enviando
        print("Datos enviados a la API:", data)

        proposito_data = {
            'id_categoria': data.get('id_categoria', 2),  # Default values can be adjusted
            'id_cargo': data.get('id_cargo', 1),
            'proposito': data.get('proposito', ''),
            'nuevo_proposito': data.get('nuevo_proposito', ''),
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d')
        }

        try:
            response = requests.post(f'{API_URL}/proposito', json=proposito_data)
            response.raise_for_status()
            return jsonify({'success': True}), 200
        except requests.RequestException as e:
            print(f"Error al enviar los datos a la API: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    # Si es GET, solo muestra la plantilla
    return render_template('concertaciondepropositospersonales.html')