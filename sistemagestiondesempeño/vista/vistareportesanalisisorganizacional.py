from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import logging

# Crear un Blueprint|   
vistareportesanalisisorganizacional = Blueprint('idreportesanalisisorganizacional', __name__, template_folder='templates')

@vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET'])
def mostrar_reporte():
    try:
        # Obtener todas las respuestas guardadas a través de la API
        respuestas_guardadas = requests.get(f"{API_URL}/dimension_respuesta_guardada")

        # Agregar la obtención de dimensiones si es necesario
        dimensiones = requests.get(f"{API_URL}/dimension").json() 

        # Filtrar solo el nombre de la dimensión
        nombres_dimensiones = [{'nombre_dimension': d['nombre_dimension']} for d in dimensiones]

        
        if respuestas_guardadas.status_code != 200:
            raise ValueError(f"Error en la solicitud a la API: {respuestas_guardadas.status_code}")
        
        respuestas_guardadas_json = respuestas_guardadas.json()

        reporte = []
        preguntas_no_encontradas = []
        for respuesta_guardada in respuestas_guardadas_json:
            if not isinstance(respuesta_guardada, dict) or 'id_dimension_pregunta' not in respuesta_guardada:
                logging.warning(f"Formato incorrecto de respuesta guardada: {respuesta_guardada}")
                continue

            # Obtener detalles de la pregunta
            pregunta_response = requests.get(f"{API_URL}/dimension_pregunta/id_dimension_pregunta/{respuesta_guardada['id_dimension_pregunta']}")
            
            if pregunta_response.status_code == 404:
                preguntas_no_encontradas.append(respuesta_guardada['id_dimension_pregunta'])
                continue
            elif pregunta_response.status_code != 200:
                raise ValueError(f"Error en la solicitud de pregunta: {pregunta_response.status_code}")
            
            pregunta_data = pregunta_response.json()
            
            # Manejar el caso en que pregunta_data es una lista
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
            if 'id_dimension_respuesta' not in respuesta_guardada:
                logging.warning(f"Falta id_dimension_respuesta en: {respuesta_guardada}")
                continue

            respuesta_response = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_respuesta/{respuesta_guardada['id_dimension_respuesta']}")
            
            if respuesta_response.status_code != 200:
                raise ValueError(f"Error en la solicitud de respuesta: {respuesta_response.status_code}")
            
            respuesta_detalle_data = respuesta_response.json()

            # Manejar el caso en que respuesta_detalle_data es una lista
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

            # Agregar los datos al reporte
            reporte.append({
                'dimension': dimensiones[respuesta_guardada['id_dimension'] - 1]['nombre_dimension'],  # Cargar solo la dimensión asociada
                'pregunta': pregunta['pregunta'],
                'respuesta': respuesta_detalle['respuesta'],
                'semaforizacion': respuesta_detalle['semaforizacion']
            })
            print("respuesta_guardada", respuesta_guardada)

        mensaje = None
        if preguntas_no_encontradas:
            mensaje = f"Algunas preguntas no fueron encontradas (IDs: {', '.join(map(str, preguntas_no_encontradas))}). "
        
        if not reporte:
            mensaje = (mensaje or "") + "No se encontraron datos válidos para el reporte."
            return render_template('reportesanalisisorganizacional.html', reporte=reporte, mensaje=mensaje, dimensiones=nombres_dimensiones)  # Pasar dimensiones a la plantilla

        return render_template('reportesanalisisorganizacional.html', reporte=reporte, mensaje=mensaje, dimensiones=nombres_dimensiones)  # Pasar solo nombres a la plantilla
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al hacer la solicitud a la API: {e}")
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error al obtener el reporte: {e}")
    
    except ValueError as e:
        logging.error(f"Error en los datos obtenidos: {e}")
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error al procesar los datos: {e}")
    
    except Exception as e:
        logging.error(f"Error inesperado: {e}", exc_info=True)
        return render_template('reportesanalisisorganizacional.html', reporte=[], mensaje=f"Error inesperado: {e}")
