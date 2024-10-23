from flask import Blueprint, render_template
from configBd import API_URL
import requests
import logging

# Crear un Blueprint
vistareportesanalisisorganizacional = Blueprint('idreportesanalisisorganizacional', __name__, template_folder='templates')


@vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET'])
def mostrar_reporte():
    try:
        respuestas_guardadas = requests.get(f"{API_URL}/dimension_respuesta_guardada").json()
        dimensiones = requests.get(f"{API_URL}/dimension").json()
        dimensiones_ordenadas = sorted(dimensiones, key=lambda x: int(x['id_dimension']))

        reporte = []
        promedios = {}

        for respuesta in respuestas_guardadas:
            pregunta_response = requests.get(f"{API_URL}/dimension_pregunta/id_dimension_pregunta/{respuesta['id_dimension_pregunta']}")
            pregunta_data = pregunta_response.json()

            if isinstance(pregunta_data, list) and len(pregunta_data) > 0:
                pregunta = pregunta_data[0]
            elif isinstance(pregunta_data, dict):
                pregunta = pregunta_data
            else:
                logging.warning(f"Formato inesperado de pregunta: {pregunta_data}")
                continue

            respuesta_response = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_respuesta/{respuesta['id_dimension_respuesta']}")
            respuesta_detalle_data = respuesta_response.json()

            if isinstance(respuesta_detalle_data, list) and len(respuesta_detalle_data) > 0:
                respuesta_detalle = respuesta_detalle_data[0]
            elif isinstance(respuesta_detalle_data, dict):
                respuesta_detalle = respuesta_detalle_data
            else:
                logging.warning(f"Formato inesperado de respuesta_detalle: {respuesta_detalle_data}")
                continue

            dimension = next((d for d in dimensiones_ordenadas if d['id_dimension'] == respuesta['id_dimension']), None)
            if dimension:
                reporte.append({
                    'dimension': dimension['nombre_dimension'],
                    'pregunta': pregunta['pregunta'],
                    'respuesta': respuesta_detalle['respuesta'],
                    'semaforizacion': respuesta_detalle['semaforizacion']
                })

                # Calcular el promedio de semaforización
                if dimension['nombre_dimension'] not in promedios:
                    promedios[dimension['nombre_dimension']] = []
                promedios[dimension['nombre_dimension']].append(respuesta_detalle['semaforizacion'])

        # Calcular el promedio para cada dimensión
        for dimension, valores in promedios.items():
            promedios[dimension] = sum(valores) / len(valores)

        return render_template('reportesanalisisorganizacional.html', reporte=reporte, promedios=promedios)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al hacer la solicitud a la API: {e}")
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error al obtener el reporte: {e}")
    
    except ValueError as e:
        logging.error(f"Error en los datos obtenidos: {e}")
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error al procesar los datos: {e}")
    
    except Exception as e:
        logging.error(f"Error inesperado: {e}", exc_info=True)
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error inesperado: {e}")
    

""" @vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET'])
def mostrar_reporte():
    try:
        # Obtener todas las respuestas guardadas a través de la API
        respuestas_guardadas = requests.get(f"{API_URL}/dimension_respuesta_guardada").json()

        # Obtener las dimensiones
        dimensiones = requests.get(f"{API_URL}/dimension").json()
        dimensiones_ordenadas = sorted(dimensiones, key=lambda x: int(x['id_dimension']))

        # Crear un diccionario para asociar respuestas con dimensiones
        reporte = []
        for respuesta in respuestas_guardadas:
            # Obtener la pregunta correspondiente
            pregunta_response = requests.get(f"{API_URL}/dimension_pregunta/id_dimension_pregunta/{respuesta['id_dimension_pregunta']}")
            pregunta_data = pregunta_response.json()

            if isinstance(pregunta_data, list) and len(pregunta_data) > 0:
                pregunta = pregunta_data[0]
            elif isinstance(pregunta_data, dict):
                pregunta = pregunta_data
            else:
                logging.warning(f"Formato inesperado de pregunta: {pregunta_data}")
                continue

            if 'pregunta' not in pregunta:
                logging.warning(f"Falta la clave 'pregunta' en: {pregunta}")
                continue

            # Obtener detalles de la respuesta
            respuesta_response = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_respuesta/{respuesta['id_dimension_respuesta']}")
            respuesta_detalle_data = respuesta_response.json()

            if isinstance(respuesta_detalle_data, list) and len(respuesta_detalle_data) > 0:
                respuesta_detalle = respuesta_detalle_data[0]
            elif isinstance(respuesta_detalle_data, dict):
                respuesta_detalle = respuesta_detalle_data
            else:
                logging.warning(f"Formato inesperado de respuesta_detalle: {respuesta_detalle_data}")
                continue

            if 'respuesta' not in respuesta_detalle or 'semaforizacion' not in respuesta_detalle:
                logging.warning(f"Faltan claves en respuesta_detalle: {respuesta_detalle}")
                continue

            dimension = next((d for d in dimensiones_ordenadas if d['id_dimension'] == respuesta['id_dimension']), None)
            if dimension:
                reporte.append({
                    'dimension': dimension['nombre_dimension'],
                    'pregunta': pregunta['pregunta'],
                    'respuesta': respuesta_detalle['respuesta'],
                    'semaforizacion': respuesta_detalle['semaforizacion']
                })

        return render_template('reportesanalisisorganizacional.html', reporte=reporte)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error al hacer la solicitud a la API: {e}")
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error al obtener el reporte: {e}")
    
    except ValueError as e:
        logging.error(f"Error en los datos obtenidos: {e}")
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error al procesar los datos: {e}")
    
    except Exception as e:
        logging.error(f"Error inesperado: {e}", exc_info=True)
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error inesperado: {e}") """