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

    # Inicialmente no cargamos preguntas ni respuestas, solo las dimensiones
    return render_template('analisisorganizacional.html', dimensiones=dimensiones_ordenadas)

@vistaanalisisorganizacional.route('/analisisorganizacional/<int:id_dimension>', methods=['GET', 'POST'])
def get_preguntas_respuestas(id_dimension):
    preguntas = requests.get(f"{API_URL}/dimension_pregunta/id_dimension/{id_dimension}").json()
    current_index = int(request.form.get('current_index', 0))
    total_preguntas = len(preguntas)

    # Guardar la respuesta seleccionada en la sesión
    if request.method == 'POST':
        respuesta_seleccionada = request.form.get('respuesta')
        if 'respuestas' not in session:
            session['respuestas'] = {}
        if id_dimension not in session['respuestas']:
            session['respuestas'][id_dimension] = []
        session['respuestas'][id_dimension].append({
            'pregunta': preguntas[current_index]['pregunta'],
            'respuesta_id': respuesta_seleccionada
        })

    # Si el índice excede el número de preguntas, redirigir a la pantalla final
    if current_index >= total_preguntas - 1:
        return redirect(url_for('idanalisisorganizacional.finalizo'))

    # Obtener la pregunta actual
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