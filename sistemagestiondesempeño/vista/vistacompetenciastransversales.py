import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
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
        respuesta_id = request.form.get('respuesta_seleccionada')
        
        # Crear un diccionario con los datos de la respuesta
        datos_respuesta = {
            'id_pregunta': int(pregunta_id),
            'id_respuesta': int(respuesta_id),
            #'iluo': request.form.get('iluo', 'Iluo no disponible'),  # Asegúrate de obtener este dato si es necesario
            #'descripcion_iluo': request.form.get('descripcion_iluo', 'Descripción de la iluo no disponible')  # Asegúrate de obtener este dato si es necesario
        }
        
        print("Datos a enviar a la API: ", pregunta_id)  # Añadir esta línea
        print("Datos a enviar a la API: ", respuesta_id)  # Añadir esta línea
        print(f"Datos a enviar a la API: {datos_respuesta}")  # Añadir esta línea
        
        # Enviar la respuesta a la API
        try:
            response = requests.post(f"{API_URL}/usuario_respuesta", json=datos_respuesta, timeout=10)
            print(f"Respuesta de la API: {response.status_code}, {response.text}")  # Añadir esta línea
            response.raise_for_status()
            # Si la respuesta se guardó correctamente, actualizar la sesión
            respuestas = session.get('respuestas', {})
            respuestas[pregunta_id] = respuesta_id
            session['respuestas'] = respuestas
            session['mensaje_confirmacion'] = "Respuesta guardada correctamente."  # Añadir esta línea
        except requests.RequestException as e:
            print(f"Error al guardar la respuesta en la API: {e}")
            print(f"Detalles de la respuesta: {e.response.text if e.response else 'No hay detalles'}")  # Añadir esta línea
            session['mensaje_error'] = "Hubo un error al guardar la respuesta. Inténtalo de nuevo."  # Añadir esta línea

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
                               usuario=session.get('usuario'),
                               mensaje_confirmacion=session.pop('mensaje_confirmacion', None),  # Añadir esta línea
                               mensaje_error=session.pop('mensaje_error', None))  # Añadir esta línea
    except (requests.RequestException, ValueError) as e:
        print(f"Error al obtener o procesar datos: {e}")
        return render_template('competenciastransversales.html', 
                               pregunta=None, 
                               preguntas=[], 
                               current_index=current_index,
                               error_message=str(e),
                               mensaje_error="Hubo un error al obtener los datos. Inténtalo de nuevo.")  # Añadir esta línea
