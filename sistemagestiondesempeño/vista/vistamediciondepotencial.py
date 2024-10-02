import random
from flask import Flask, Blueprint, request, render_template, redirect, url_for, session, jsonify
import requests
from datetime import datetime

# Configuración
API_URL = 'http://190.217.58.246:5184/api/sgd'

# Crear un Blueprint
vistamediciondepotencial = Blueprint('idmediciondepotencial', __name__, template_folder='templates')

@vistamediciondepotencial.route('/mediciondepotencial', methods=['GET', 'POST'])
def vista_medicion_potencial():
    # Inicializar el índice de la pregunta
    current_index = 0 if request.method == 'GET' else int(request.form.get('current_index', 0))
    respuestas_usuario = session.get('respuestas_usuario', {})

    # Manejar las respuestas enviadas por el usuario
    if request.method == 'POST' and 'respuesta_seleccionada' in request.form:
        pregunta_id = request.form.get('pregunta_id')
        respuestas_usuario[pregunta_id] = request.form.get('respuesta_seleccionada')
        session['respuestas_usuario'] = respuestas_usuario

        if 'next' in request.form:
            current_index += 1
        elif 'prev' in request.form:
            current_index -= 1

    try:
        # Obtener dimensiones
        response_dimensiones = requests.get(f'{API_URL}/dimension_mp', timeout=10)
        response_dimensiones.raise_for_status()
        dimensiones = response_dimensiones.json()

        # Obtener preguntas
        response_preguntas = requests.get(f'{API_URL}/dimension_mp_pregunta', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()

        if current_index < 0:
            current_index = 0
        if current_index >= len(preguntas):
            return redirect(url_for('finalizo'))

        pregunta_actual = preguntas[current_index]
        id_pregunta = pregunta_actual['id_pregunta']

        # Obtener respuestas para la pregunta actual
        response_respuestas = requests.get(f'{API_URL}/dimension_mp_respuesta', timeout=10)
        response_respuestas.raise_for_status()
        respuestas_list = response_respuestas.json()

        # Filtrar respuestas para la pregunta actual
        respuestas_pregunta_actual = [r for r in respuestas_list if r['id_pregunta'] == id_pregunta]

        # Mezclar las respuestas aleatoriamente
        random.shuffle(respuestas_pregunta_actual)
        pregunta_actual['respuestas'] = respuestas_pregunta_actual

        return render_template('mediciondepotencial.html', 
                               pregunta=pregunta_actual, 
                               preguntas=preguntas,
                               dimensiones=dimensiones,
                               current_index=current_index,
                               total_preguntas=len(preguntas), 
                               usuario=session.get('usuario'))
    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return render_template('mediciondepotencial.html', 
                               pregunta=None, 
                               preguntas=[], 
                               dimensiones=[],
                               current_index=current_index)

