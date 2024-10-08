from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests, random
from datetime import datetime
from control.ControlEntidad import ControlEntidad

vistaanalisisorganizacional = Blueprint('idanalisisorganizacional', __name__, template_folder='templates')

@vistaanalisisorganizacional.route('/analisisorganizacional', methods=['GET', 'POST'])
def get_dimensiones():
    # Obtener las dimensiones
    dimensiones = requests.get(f"{API_URL}/dimension").json()

    # Asegurarte de que todos los 'id_dimension' sean enteros antes de ordenar
    dimensiones_ordenadas = sorted(dimensiones, key=lambda x: int(x['id_dimension']))

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
        print(f"Respuesta seleccionada ID: {respuesta_seleccionada_id}")

        if respuesta_seleccionada_id:
            # Hacer la solicitud a la API usando la URL correcta
            try:
                respuesta_seleccionada = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_respuesta/{respuesta_seleccionada_id}")
                print(f"Respuesta de la API: {respuesta_seleccionada.status_code}")
                print(f"Contenido de la respuesta: {respuesta_seleccionada.text}")

                respuesta_seleccionada.raise_for_status()  # Esto lanzará una excepción para códigos de estado 4xx y 5xx

                respuesta_seleccionada_json = respuesta_seleccionada.json()

                # Verifica si la respuesta es una lista
                if isinstance(respuesta_seleccionada_json, list):
                    if len(respuesta_seleccionada_json) > 0:
                        respuesta_texto = respuesta_seleccionada_json[0].get('respuesta', 'Sin respuesta')
                        semaforizacion = respuesta_seleccionada_json[0].get('semaforizacion', 'No determinado')  # Obtener semaforizacion
                    else:
                        respuesta_texto = 'Sin respuesta'
                        semaforizacion = 'No determinado'
                else:
                    respuesta_texto = respuesta_seleccionada_json.get('respuesta', 'Sin respuesta')
                    semaforizacion = respuesta_seleccionada_json.get('semaforizacion', 'No determinado')

            except requests.exceptions.RequestException as e:
                print(f"Error al hacer la solicitud a la API: {e}")
                respuesta_texto = 'Error al obtener la respuesta'
                semaforizacion = 'No determinado'

            # Convertir id_dimension a cadena
            id_dimension_str = str(id_dimension)

            # Usar la clave correcta de la pregunta, asegurándose de que sea un entero
            id_pregunta = int(preguntas[current_index]['id_dimension_pregunta'])

            # Inicializar el diccionario de respuestas si no existe
            if 'respuestas' not in session:
                session['respuestas'] = {}

            # Inicializar el diccionario de preguntas para la dimensión si no existe
            if id_dimension_str not in session['respuestas']:
                session['respuestas'][id_dimension_str] = {}

            # Guardar la respuesta asociada a la pregunta, incluyendo semaforizacion
            session['respuestas'][id_dimension_str][id_pregunta] = {
                'pregunta': preguntas[current_index]['pregunta'],
                'respuesta_id': respuesta_seleccionada_id,
                'respuesta_texto': respuesta_texto,
                'semaforizacion': semaforizacion  # Guardar semaforizacion aquí
                }
            print(f"Respuesta guardada en la sesión: {session['respuestas'][id_dimension_str][id_pregunta]}")

            # Guardar los cambios en la sesión
            session.modified = True

            # Incrementar el índice después de procesar la respuesta
            current_index += 1

            # Redirigir a la siguiente pregunta o a la página de finalización
            if current_index < total_preguntas:
                return redirect(url_for('idanalisisorganizacional.get_preguntas_respuestas', 
                                        id_dimension=id_dimension, 
                                        current_index=current_index))
            else:
                return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Si todas las preguntas han sido respondidas, redirigir a la pantalla de finalización
    if current_index >= total_preguntas:
        return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Obtener la pregunta actual y las posibles respuestas
    if current_index < len(preguntas):
        pregunta_actual = preguntas[current_index]
        respuestas = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_pregunta/{pregunta_actual['id_dimension_pregunta']}").json()
    
        # Mezclar las respuestas aleatoriamente
        random.shuffle(respuestas)
    else:
        # Manejar el caso cuando no hay más preguntas
        return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Obtener la dimensión actual
    dimensiones = requests.get(f"{API_URL}/dimension").json()
    dimension_actual = next((d for d in dimensiones if d['id_dimension'] == id_dimension), None)
    print("Dimensión actual:", dimension_actual)  # Añade esta línea

    return render_template(
        'analisisorganizacional.html',
        pregunta_actual=pregunta_actual,
        respuestas=respuestas,
        current_index=current_index,
        total_preguntas=total_preguntas,
        dimension_id=id_dimension,
        dimension_actual=dimension_actual
    )


@vistaanalisisorganizacional.route('/finalizo', methods=['GET'])
def finalizo():
    # Mostrar la pantalla de finalización
    return render_template('finalizo1.html')