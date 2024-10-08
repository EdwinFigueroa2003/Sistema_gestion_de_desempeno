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
                respuesta_seleccionada = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_respuesta/{respuesta_seleccionada_id}")
                print(f"Respuesta de la API: {respuesta_seleccionada.status_code}")
                print(f"Contenido de la respuesta: {respuesta_seleccionada.text}")

                respuesta_seleccionada.raise_for_status()
                respuesta_seleccionada_json = respuesta_seleccionada.json()

                # Procesar la respuesta
                if isinstance(respuesta_seleccionada_json, list):
                    if len(respuesta_seleccionada_json) > 0:
                        respuesta_texto = respuesta_seleccionada_json[0].get('respuesta', 'Sin respuesta')
                        semaforizacion = respuesta_seleccionada_json[0].get('semaforizacion', 'No determinado')
                    else:
                        respuesta_texto = 'Sin respuesta'
                        semaforizacion = 'No determinado'
                else:
                    respuesta_texto = respuesta_seleccionada_json.get('respuesta', 'Sin respuesta')
                    semaforizacion = respuesta_seleccionada_json.get('semaforizacion', 'No determinado')

                # Asegurarse de que todas las claves sean strings
                id_dimension_str = str(id_dimension)
                id_pregunta_str = str(preguntas[current_index]['id_dimension_pregunta'])

                # Inicializar la estructura de la sesión si no existe
                if 'respuestas' not in session:
                    session['respuestas'] = {}

                if id_dimension_str not in session['respuestas']:
                    session['respuestas'][id_dimension_str] = {}

                # Guardar la respuesta usando strings como claves
                session['respuestas'][id_dimension_str][id_pregunta_str] = {
                    'pregunta': preguntas[current_index]['pregunta'],
                    'respuesta_id': str(respuesta_seleccionada_id),  # Convertir a string
                    'respuesta_texto': respuesta_texto,
                    'semaforizacion': semaforizacion
                }

                # Asegurarse de que los cambios se guarden
                session.modified = True

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

@vistaanalisisorganizacional.route('/finalizo', methods=['GET'])
def finalizo():
    return render_template('finalizo1.html')