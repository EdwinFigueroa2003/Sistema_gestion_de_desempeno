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
    # Obtener fk_nivel_de_contribucion desde la sesión
    fk_nivel_de_contribucion = session.get('fk_nivel_de_contribucion')

    # Inicializar el índice de la pregunta
    current_index = 0 if request.method == 'GET' else int(request.form.get('current_index', 0))
    respuestas = session.get('respuestas', {})

    # Manejar las respuestas enviadas por el usuario
    if request.method == 'POST' and 'respuesta_seleccionada' in request.form:
        pregunta_id = request.form.get('pregunta_id')
        respuestas[pregunta_id] = request.form.get('respuesta_seleccionada')
        session['respuestas'] = respuestas

        if 'next' in request.form:
            current_index += 1
        elif 'prev' in request.form:
            current_index -= 1

    # Obtener preguntas filtradas por fk_nivel_de_contribucion
    try:
        response_preguntas = requests.get(f'{API_URL}/pregunta/fk_nivel_de_contribucion/1', timeout=10)
        #response_preguntas = requests.get(f'{API_URL}/pregunta?fk_nivel_de_contribucion={fk_nivel_de_contribucion}', timeout=10) #Todas las preguntas sin filtro
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()

        if not isinstance(preguntas, list):
            raise ValueError("La respuesta de la API no es una lista de preguntas")

        if current_index < 0:
            current_index = 0
        if current_index >= len(preguntas):
            return redirect(url_for('finalizo'))

        pregunta_actual = preguntas[current_index]
        if not isinstance(pregunta_actual, dict):
            raise ValueError(f"La pregunta en el índice {current_index} no es un diccionario")

        id_pregunta = pregunta_actual.get('id_pregunta')
        if id_pregunta is None:
            raise ValueError(f"La pregunta en el índice {current_index} no tiene 'id_pregunta'")

        # Obtener respuestas para la pregunta actual
        response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
        response_respuestas.raise_for_status()
        respuestas_list = response_respuestas.json()

        if not isinstance(respuestas_list, list):
            raise ValueError("La respuesta de la API para las respuestas no es una lista")

        # Mezclar las respuestas aleatoriamente
        random.shuffle(respuestas_list)
        pregunta_actual['respuestas'] = respuestas_list

        return render_template('competenciastransversales.html', 
                               pregunta=pregunta_actual, 
                               preguntas=preguntas,
                               current_index=current_index,
                               total_preguntas=len(preguntas), 
                               usuario=session.get('usuario'))
    except (requests.RequestException, ValueError) as e:
        print(f"Error al obtener o procesar datos: {e}")
        return render_template('competenciastransversales.html', 
                               pregunta=None, 
                               preguntas=[], 
                               current_index=current_index,
                               error_message=str(e))  # current_index se sigue enviando