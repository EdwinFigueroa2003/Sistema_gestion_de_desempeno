from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import random

vistaanalisisorganizacional = Blueprint('idanalisisorganizacional', __name__, template_folder='templates')

@vistaanalisisorganizacional.route('/analisisorganizacional', methods=['GET', 'POST'])
def get_dimensiones():
    dimensiones = requests.get(f"{API_URL}/dimension").json()
    dimensiones_ordenadas = sorted(dimensiones, key=lambda x: int(x['id_dimension']))
    return render_template('analisisorganizacional.html', dimensiones=dimensiones_ordenadas)

@vistaanalisisorganizacional.route('/analisisorganizacional/<int:id_dimension>', methods=['GET', 'POST'])
def get_preguntas_respuestas(id_dimension):
    # Obtener las preguntas de la dimensión
    preguntas = requests.get(f"{API_URL}/dimension_pregunta/id_dimension/{id_dimension}").json()
    total_preguntas = len(preguntas)
    current_index = int(request.args.get('current_index', 0))

    if request.method == 'POST':
        respuesta_seleccionada_id = request.form.get('respuesta')
        print(f"Respuesta seleccionada ID: {respuesta_seleccionada_id}")

        if respuesta_seleccionada_id:
            try:
                # Obtener la respuesta
                respuesta_seleccionada = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_respuesta/{respuesta_seleccionada_id}")
                print(f"Respuesta de la API: {respuesta_seleccionada.status_code}")
                print(f"Contenido de la respuesta: {respuesta_seleccionada.text}")

                respuesta_seleccionada.raise_for_status()
                respuesta_seleccionada_json = respuesta_seleccionada.json()

                # Guardar la respuesta en la base de datos a través de la API
                respuesta_guardada_data = {
                    "id_dimension": id_dimension,
                    "id_dimension_pregunta": preguntas[current_index]['id_dimension_pregunta'],
                    "id_dimension_respuesta": int(respuesta_seleccionada_id)
                }
                
                guardar_respuesta = requests.post(f"{API_URL}/dimension_respuesta_guardada", json=respuesta_guardada_data)
                guardar_respuesta.raise_for_status()

                # Incrementar el índice
                current_index += 1

                if current_index < total_preguntas:
                    return redirect(url_for('idanalisisorganizacional.get_preguntas_respuestas', 
                                          id_dimension=id_dimension, 
                                          current_index=current_index))
                else:
                    return redirect(url_for('idanalisisorganizacional.finalizo'))

            except requests.exceptions.RequestException as e:
                print(f"Error al hacer la solicitud a la API: {e}")
                return render_template('error.html', mensaje="Error al procesar la respuesta")

    # Si todas las preguntas han sido respondidas
    if current_index >= total_preguntas:
        return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Obtener la pregunta actual y las respuestas
    if current_index < len(preguntas):
        pregunta_actual = preguntas[current_index]
        respuestas = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_pregunta/{pregunta_actual['id_dimension_pregunta']}").json()
        random.shuffle(respuestas)
    else:
        return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Obtener la dimensión actual
    dimensiones = requests.get(f"{API_URL}/dimension").json()
    dimension_actual = next((d for d in dimensiones if int(d['id_dimension']) == id_dimension), None)
    
    return render_template(
        'analisisorganizacional.html',
        pregunta_actual=pregunta_actual,
        respuestas=respuestas,
        current_index=current_index,
        total_preguntas=total_preguntas,
        dimension_id=id_dimension,
        dimension_actual=dimension_actual
    )

@vistaanalisisorganizacional.route('/finalizo1', methods=['GET'])
def finalizo():
    return render_template('finalizo1.html')