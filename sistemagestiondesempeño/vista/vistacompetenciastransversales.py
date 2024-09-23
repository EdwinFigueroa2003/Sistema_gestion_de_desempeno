import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from datetime import datetime
from control.ControlEntidad import ControlEntidad
from configBd import API_URL

# Crear un Blueprint
vistacompetenciastransversales = Blueprint('idcompetenciastransversales', __name__, template_folder='templates')

@vistacompetenciastransversales.route('/competenciastransversales', methods=['GET', 'POST'])
def vista_competenciastransversales():
    id_apartado = 1  # Cambia este valor si fuera necesario
    user_id = 1  # Cambia esto según sea necesario

    if request.method == 'POST':
        # Manejar los datos del formulario y la navegación entre preguntas
        current_index = int(request.form.get('current_index', 0))
        respuestas = session.get('respuestas', {})

        # Guardar la respuesta seleccionada para la pregunta actual
        if 'respuesta_seleccionada' in request.form:
            pregunta_id = request.form.get('pregunta_id')
            respuestas[pregunta_id] = request.form.get('respuesta_seleccionada')
            session['respuestas'] = respuestas

        if 'next' in request.form:
            current_index += 1
        elif 'prev' in request.form:
            current_index -= 1

        # Obtener la lista de preguntas
        try:
            response_preguntas = requests.get(f'{API_URL}/pregunta/id_apartado/{id_apartado}', timeout=10)
            response_preguntas.raise_for_status()
            preguntas = response_preguntas.json()

            # Asegúrate de que la pregunta actual esté disponible
            if current_index < 0:
                current_index = 0
            if current_index >= len(preguntas):
                return redirect(url_for('finalizo'))

            pregunta_actual = preguntas[current_index]
            id_pregunta = pregunta_actual['id_pregunta']
            response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
            response_respuestas.raise_for_status()
            respuestas_list = response_respuestas.json()

            # Barajar las respuestas
            random.shuffle(respuestas_list)
            pregunta_actual['respuestas'] = respuestas_list

            return render_template('competenciastransversales.html', pregunta=pregunta_actual, preguntas=preguntas,
                                   current_index=current_index, total_preguntas=len(preguntas))
        except requests.RequestException as e:
            print(f"Error al obtener datos: {e}")
            return render_template('competenciastransversales.html', pregunta=None, preguntas=[])

    # Inicializa el índice de la pregunta actual en GET
    current_index = 0
    try:
        response_preguntas = requests.get(f'{API_URL}/pregunta/id_apartado/{id_apartado}', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()

        if preguntas:
            pregunta_actual = preguntas[current_index]
            id_pregunta = pregunta_actual['id_pregunta']
            response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
            response_respuestas.raise_for_status()
            respuestas_list = response_respuestas.json()

            # Barajar las respuestas
            random.shuffle(respuestas_list)
            pregunta_actual['respuestas'] = respuestas_list

            return render_template('competenciastransversales.html', pregunta=pregunta_actual, preguntas=preguntas,
                                   current_index=current_index, total_preguntas=len(preguntas))
    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return render_template('competenciastransversales.html', pregunta=None, preguntas=[])
