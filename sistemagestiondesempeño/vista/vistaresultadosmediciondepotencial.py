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

@vistaresultadosmediciondepotencial.route('/resultadosmediciondepotencial', methods=['GET'])
def vista_resultados_medicion_de_potencial():
    try:
        # Obtener todas las respuestas guardadas
        url_respuestas_guardadas = f"{API_URL}/dimension_mp_respuesta_guardada"
        response_respuestas = requests.get(url_respuestas_guardadas)
        response_respuestas.raise_for_status()
        respuestas_guardadas = response_respuestas.json()

        # Inicializar una lista para almacenar los detalles de las respuestas
        detalles_respuestas = []

        for respuesta_guardada in respuestas_guardadas:
            try:
                # Obtener detalles de la dimensión
                url_dimension = f"{API_URL}/dimension_mp/id_dimension_mp/{respuesta_guardada['id_dimension_mp']}"
                print(f"Solicitando dimensión: {url_dimension}")
                response_dimension = requests.get(url_dimension)
                response_dimension.raise_for_status()
                dimension_detalle = response_dimension.json()[0]  # Tomar el primer elemento de la lista
                print(f"Respuesta dimensión: {dimension_detalle}")

                # Obtener detalles de la pregunta
                url_pregunta = f"{API_URL}/dimension_mp_pregunta/id_dimension_mp_pregunta/{respuesta_guardada['id_dimension_mp_pregunta']}"
                print(f"Solicitando pregunta: {url_pregunta}")
                response_pregunta = requests.get(url_pregunta)
                response_pregunta.raise_for_status()
                pregunta_detalle = response_pregunta.json()[0]  # Tomar el primer elemento de la lista
                print(f"Respuesta pregunta: {pregunta_detalle}")

                # Obtener detalles de la respuesta
                url_respuesta = f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_respuesta/{respuesta_guardada['id_dimension_mp_respuesta']}"
                print(f"Solicitando respuesta: {url_respuesta}")
                response_respuesta = requests.get(url_respuesta)
                response_respuesta.raise_for_status()
                respuesta_detalle = response_respuesta.json()[0]  # Tomar el primer elemento de la lista
                print(f"Respuesta respuesta: {respuesta_detalle}")

                # Crear un diccionario con los detalles
                detalle = {
                    'dimension': dimension_detalle['nombre'],
                    'pregunta': pregunta_detalle['pregunta'],
                    'respuesta': respuesta_detalle['respuesta_mp'],
                    'fecha_respuesta': respuesta_guardada['fecha_respuesta']
                }
                
                detalles_respuestas.append(detalle)
            except Exception as e:
                print(f"Error al procesar una respuesta: {e}")
                detalles_respuestas.append({
                    'dimension': 'Error',
                    'pregunta': 'Error al obtener detalles',
                    'respuesta': str(e),
                    'fecha_respuesta': respuesta_guardada['fecha_respuesta']
                })

        return render_template('resultadosmediciondepotencial.html', respuestas=detalles_respuestas)

    except requests.RequestException as e:
        print(f"Error al obtener los datos: {e}")
        return render_template('resultadosmediciondepotencial.html', respuestas=[])

""" @vistaresultadosmediciondepotencial.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    try:
        # Obtener todas las respuestas guardadas
        url_respuestas_guardadas = f"{API_URL}/dimension_mp_respuesta_guardada"
        response_respuestas = requests.get(url_respuestas_guardadas)
        response_respuestas.raise_for_status()
        respuestas_guardadas = response_respuestas.json()

        # Crear un nuevo libro de trabajo de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Resultados Medición de Potencial"

        # Agregar encabezados
        ws.append(["Dimensión", "Pregunta", "Respuesta", "Fecha de Respuesta"])

        # Agregar datos
        for respuesta_guardada in respuestas_guardadas:
            try:
                # Obtener detalles de la dimensión
                url_dimension = f"{API_URL}/dimension_mp/id_dimension_mp/{respuesta_guardada['id_dimension_mp']}"
                response_dimension = requests.get(url_dimension)
                response_dimension.raise_for_status()
                dimension_detalle = response_dimension.json()[0]

                # Obtener detalles de la pregunta
                url_pregunta = f"{API_URL}/dimension_mp_pregunta/id_dimension_mp_pregunta/{respuesta_guardada['id_dimension_mp_pregunta']}"
                response_pregunta = requests.get(url_pregunta)
                response_pregunta.raise_for_status()
                pregunta_detalle = response_pregunta.json()[0]

                # Obtener detalles de la respuesta
                url_respuesta = f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_respuesta/{respuesta_guardada['id_dimension_mp_respuesta']}"
                response_respuesta = requests.get(url_respuesta)
                response_respuesta.raise_for_status()
                respuesta_detalle = response_respuesta.json()[0]

                # Agregar fila al Excel
                ws.append([
                    dimension_detalle['nombre'],
                    pregunta_detalle['pregunta'],
                    respuesta_detalle['respuesta_mp'],
                    respuesta_guardada['fecha_respuesta']
                ])
            except Exception as e:
                print(f"Error al procesar una respuesta para Excel: {e}")
                ws.append(["Error", "Error al obtener detalles", str(e), respuesta_guardada['fecha_respuesta']])

        # Guardar el archivo Excel en memoria
        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        # Generar un nombre de archivo con la fecha actual
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Resultados_Medicion_Potencial_{fecha_actual}.xlsx"

        # Enviar el archivo Excel como respuesta
        return send_file(
            excel_file,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        print(f"Error al generar el archivo Excel: {e}")
        return "Error al generar el archivo Excel", 500
 """