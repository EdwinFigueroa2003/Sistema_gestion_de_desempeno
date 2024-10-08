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
            # Obtener los detalles de la respuesta
            url_respuesta = f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_respuesta/{id_dimension_mp_respuesta}"
            response_respuesta = requests.get(url_respuesta)
            print(f"Solicitando URL: {url_respuesta}")

            if response_respuesta.status_code == 200:
                try:
                    respuesta_detalle = response_respuesta.json()

                    # Verificar si la respuesta es una lista
                    if isinstance(respuesta_detalle, list):
                        respuesta_detalle = respuesta_detalle[0]  # Obtener el primer elemento de la lista

                    # Obtener el id de la pregunta asociada a la respuesta
                    id_dimension_mp_pregunta = respuesta_detalle['id_dimension_mp_pregunta']

                    # Ahora obtener los detalles de la pregunta
                    url_pregunta = f"{API_URL}/dimension_mp_pregunta/id_dimension_mp_pregunta/{id_dimension_mp_pregunta}"
                    response_pregunta = requests.get(url_pregunta)
                    print(f"Solicitando URL de la pregunta: {url_pregunta}")

                    if response_pregunta.status_code == 200:
                        pregunta_detalle = response_pregunta.json()

                        # Verificar si la pregunta es una lista
                        if isinstance(pregunta_detalle, list):
                            pregunta_detalle = pregunta_detalle[0]  # Obtener el primer elemento de la lista

                        # Obtener el id de la dimensión asociada a la pregunta
                        id_dimension_mp = pregunta_detalle['id_dimension_mp']

                        # Ahora obtener los detalles de la dimensión
                        url_dimension = f"{API_URL}/dimension_mp/id_dimension_mp/{id_dimension_mp}"
                        response_dimension = requests.get(url_dimension)
                        print(f"Solicitando URL de la dimensión: {url_dimension}")

                        if response_dimension.status_code == 200:
                            dimension_detalle = response_dimension.json()

                            # Verificar si la dimensión es una lista
                            if isinstance(dimension_detalle, list):
                                dimension_detalle = dimension_detalle[0]  # Obtener el primer elemento de la lista

                            # Crear un nuevo diccionario para cada respuesta
                            detalle = {
                                'pregunta': pregunta_detalle['pregunta'],
                                'respuesta': respuesta_detalle['respuesta_mp'],
                                'dimension': dimension_detalle['nombre']
                            }
                            
                            # Agregar el diccionario a la lista
                            detalles_respuestas.append(detalle)

                        else:
                            print(f"Error al obtener la dimensión: {response_dimension.status_code}")
                    else:
                        print(f"Error al obtener la pregunta: {response_pregunta.status_code}")
                except requests.exceptions.JSONDecodeError:
                    print(f"Error al decodificar la respuesta para ID: {id_dimension_mp_respuesta}")
                    continue
            else:
                print(f"Error en la solicitud para ID: {id_dimension_mp_respuesta}, status code: {response_respuesta.status_code}")
                print(f"Contenido de la respuesta: {response_respuesta.text}")
                continue
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud para ID: {id_dimension_mp_respuesta}: {e}")
            continue

    # Asegurarse de que detalles_respuestas sea una lista antes de pasarlo a render_template
    if not isinstance(detalles_respuestas, list):
        detalles_respuestas = [detalles_respuestas]

    return render_template('resultadosmediciondepotencial.html', respuestas=detalles_respuestas)