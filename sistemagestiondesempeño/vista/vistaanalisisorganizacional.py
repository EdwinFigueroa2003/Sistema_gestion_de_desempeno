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

    # Inicialmente no cargamos preguntas ni respuestas, solo las dimensiones
    return render_template('analisisorganizacional.html', dimensiones=dimensiones)

@vistaanalisisorganizacional.route('/analisisorganizacional/<int:id_dimension>', methods=['GET', 'POST'])
def get_preguntas_respuestas(id_dimension):
    # Obtener todas las preguntas para la dimensión seleccionada
    preguntas = requests.get(f"{API_URL}/dimension_pregunta/id_dimension/{id_dimension}").json()

    # Controlar el índice de la pregunta actual
    current_index = int(request.form.get('current_index', 0))  # Índice de la pregunta actual, por defecto la primera

    total_preguntas = len(preguntas)

    # Si el índice excede el número de preguntas, redirigimos a la pantalla de finalización
    if current_index >= total_preguntas:
        return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Obtener la pregunta actual
    pregunta_actual = preguntas[current_index]

    # Obtener las respuestas para la pregunta actual
    respuestas = requests.get(f"{API_URL}/dimension_respuesta/id_dimension_pregunta/{pregunta_actual['id_dimension_pregunta']}").json()

    # Renderizar la plantilla con la pregunta actual y las respuestas
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