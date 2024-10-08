from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests, random
from datetime import datetime
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaresultadosmediciondepotencial = Blueprint('idresultadosmediciondepotencial', __name__, template_folder='templates')

@vistaresultadosmediciondepotencial.route('/resultadosmediciondepotencial', methods=['GET', 'POST'])
def vista_resultados_medicion_de_potencial():
    # Acceder a las respuestas almacenadas en la sesión
    respuestas = session.get('respuestas', [])

    # Inicializar una lista para almacenar los detalles de las respuestas
    detalles_respuestas = []

    for id_dimension_mp_respuesta in respuestas:
        try:
            url = f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_respuesta/{id_dimension_mp_respuesta}"
            response = requests.get(url)
            print(f"Solicitando URL: {url}")  # Agregar información de la URL

            if response.status_code == 200:
                try:
                    respuesta_detalle = response.json()
                    detalles_respuestas.append(respuesta_detalle)
                except requests.exceptions.JSONDecodeError:
                    print(f"Error al decodificar la respuesta para ID: {id_dimension_mp_respuesta}")
                    continue
            else:
                print(f"Error en la solicitud para ID: {id_dimension_mp_respuesta}, status code: {response.status_code}")
                print(f"Contenido de la respuesta: {response.text}")  # Mostrar el contenido de la respuesta si no es 200
                continue
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud para ID: {id_dimension_mp_respuesta}: {e}")
            continue


    return render_template('resultadosmediciondepotencial.html', respuestas=detalles_respuestas)