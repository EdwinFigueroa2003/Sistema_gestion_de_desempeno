from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from datetime import datetime
from control.ControlEntidad import ControlEntidad

vistaanalisisorganizacional = Blueprint('idanalisisorganizacional', __name__, template_folder='templates')

@vistaanalisisorganizacional.route('/analisisorganizacional', methods=['GET', 'POST'])
def get_dimensiones():
    # Obtener las dimensiones
    dimensiones = requests.get(f"{API_URL}/dimension").json()

    # Ordenar las dimensiones por el campo 'id_dimension'
    dimensiones_ordenadas = sorted(dimensiones, key=lambda x: x['id_dimension'])

    return render_template('analisisorganizacional.html', dimensiones=dimensiones_ordenadas)

@vistaanalisisorganizacional.route('/analisisorganizacional/<int:id_dimension>', methods=['GET', 'POST'])
def get_preguntas_respuestas(id_dimension):
    # Obtener las preguntas de la dimensión
    preguntas = requests.get(f"{API_URL}/dimension_pregunta/id_dimension/{id_dimension}").json()
    total_preguntas = len(preguntas)

    # Obtener el índice actual de la pregunta
    current_index = int(request.args.get('current_index', 0))

    if request.method == 'POST':
        respuesta_seleccionada_id = request.form.get('respuesta')

        if respuesta_seleccionada_id:
            # Hacer la solicitud a la API usando la URL correcta
            respuesta_seleccionada = requests.get(f"http://190.217.58.246:5184/api/sgd/dimension_respuesta/id_dimension_respuesta/{respuesta_seleccionada_id}")

            # Verificar si la respuesta es válida y si tiene contenido
            if respuesta_seleccionada.status_code == 200 and respuesta_seleccionada.text:
                try:
                    respuesta_seleccionada_json = respuesta_seleccionada.json()

                    # Verifica si la respuesta es una lista
                    if isinstance(respuesta_seleccionada_json, list):
                        # Accede al primer elemento de la lista si existe
                        if len(respuesta_seleccionada_json) > 0:
                            respuesta_texto = respuesta_seleccionada_json[0].get('respuesta', 'Sin respuesta')
                        else:
                            respuesta_texto = 'Sin respuesta'
                    else:
                        # Si no es una lista, trata como un diccionario
                        respuesta_texto = respuesta_seleccionada_json.get('respuesta', 'Sin respuesta')

                except ValueError:
                    print("Error: La respuesta de la API no es un JSON válido")
                    respuesta_texto = 'Error al obtener la respuesta'
            else:
                print(f"Error: La API devolvió el estado {respuesta_seleccionada.status_code} o no tiene contenido")
                respuesta_texto = 'Sin respuesta'

            # Convertir id_dimension a cadena
            id_dimension_str = str(id_dimension)

            # Usar la clave correcta de la pregunta
            id_pregunta_str = str(preguntas[current_index]['id_dimension_pregunta'])

            # Inicializar el diccionario de respuestas si no existe
            if 'respuestas' not in session:
                session['respuestas'] = {}

            # Inicializar el diccionario de preguntas para la dimensión si no existe
            if id_dimension_str not in session['respuestas']:
                session['respuestas'][id_dimension_str] = {}

            # Guardar la respuesta asociada a la pregunta
            session['respuestas'][id_dimension_str][id_pregunta_str] = {
                'pregunta': preguntas[current_index]['pregunta'],
                'respuesta_id': respuesta_seleccionada_id,
                'respuesta_texto': respuesta_texto
            }

            # Guardar los cambios en la sesión
            session.modified = True

            # Incrementar el índice actual
            current_index += 1

            # Redirigir a la siguiente pregunta o a la pantalla de finalización
            if current_index < total_preguntas:
                return redirect(url_for('idanalisisorganizacional.get_preguntas_respuestas', id_dimension=id_dimension, current_index=current_index))
            else:
                return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Si todas las preguntas han sido respondidas, redirigir a la pantalla de finalización
    if current_index >= total_preguntas:
        return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Obtener la pregunta actual y las posibles respuestas
    pregunta_actual = preguntas[current_index]
    respuestas = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_pregunta/{pregunta_actual['id_dimension_pregunta']}").json()

    return render_template(
        'analisisorganizacional.html',
        preguntas=preguntas,
        pregunta_actual=pregunta_actual,
        respuestas=respuestas,
        current_index=current_index,
        total_preguntas=total_preguntas,
        dimension_id=id_dimension
    )


@vistaanalisisorganizacional.route('/finalizo', methods=['GET'])
def finalizo():
    # Mostrar la pantalla de finalización
    return render_template('finalizo1.html')