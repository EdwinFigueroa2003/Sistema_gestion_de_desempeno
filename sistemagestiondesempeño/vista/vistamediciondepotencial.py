import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistamediciondepotencial = Blueprint('idmediciondepotencial', __name__, template_folder='templates')

@vistamediciondepotencial.route('/mediciondepotencial', methods=['GET', 'POST'])
@login_required
def vista_medicion_potencial():
    # Obtener el id_usuario desde la sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return redirect(url_for('idvistalogin.vista_login'))  # Redirigir al login si no hay un usuario en sesión

    # Obtener las preguntas de la dimensión
    preguntas = requests.get(f"{API_URL}/dimension_mp_pregunta").json()
    
    # Obtener el índice actual de la pregunta
    current_index = int(request.args.get('current_index', 0))

    # Verificar que el índice actual esté dentro de los límites
    if current_index < len(preguntas):
        # Obtener la pregunta actual
        pregunta_actual = preguntas[current_index]

        # Obtener la dimensión de la pregunta actual
        response = requests.get(f"{API_URL}/dimension_mp/id_dimension_mp/{pregunta_actual['id_dimension_mp']}")
        print(f"ID de dimensión: {pregunta_actual['id_dimension_mp']}")
        
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            dimension_actual = response.json()
            print(f"Dimensión actual: {dimension_actual}")
        else:
            print(f"Error al obtener la dimensión: {response.status_code} - {response.text}")
            
            dimension_actual = None  # O maneja el error de otra manera

        if request.method == 'POST':
            respuesta_seleccionada_id = request.form.get('respuesta')
            
            if respuesta_seleccionada_id:
                respuesta_seleccionada_id = int(respuesta_seleccionada_id)
                
                # Guardar la respuesta a través de la API
                guardar_respuesta(
                    id_usuario,  # Añadir id_usuario al guardar la respuesta
                    pregunta_actual['id_dimension_mp'],
                    pregunta_actual['id_dimension_mp_pregunta'],
                    respuesta_seleccionada_id
                )
                
                # Incrementar el índice actual para la siguiente pregunta
                current_index += 1
                
                # Redirigir a la siguiente pregunta o terminar
                if current_index < len(preguntas):
                    return redirect(url_for('idmediciondepotencial.vista_medicion_potencial', current_index=current_index))
                else:
                    return redirect(url_for('idmediciondepotencial.finalizo'))

        # Si el índice excede el número de preguntas, finalizar
        if current_index >= len(preguntas):
            return redirect(url_for('idmediciondepotencial.finalizo'))
        
        # Obtener las respuestas de la pregunta actual
        respuestas = requests.get(f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_pregunta/{pregunta_actual['id_dimension_mp_pregunta']}").json()

        # Mezclar las respuestas aleatoriamente
        random.shuffle(respuestas)
    
        return render_template(
            'mediciondepotencial.html',
            pregunta_actual=pregunta_actual,
            respuestas=respuestas,
            current_index=current_index,
            total_preguntas=len(preguntas),
            dimension_actual=dimension_actual  # Agregar dimensión actual
        )
    else:
        return redirect(url_for('idmediciondepotencial.finalizo'))
    
# Función para guardar la respuesta a través de la API
@login_required
def guardar_respuesta(id_usuario, id_dimension_mp, id_dimension_mp_pregunta, id_dimension_mp_respuesta):
    try:
        data = {
            "id_usuario": id_usuario,  # Incluir id_usuario en los datos
            "id_dimension_mp": id_dimension_mp,
            "id_dimension_mp_pregunta": id_dimension_mp_pregunta,
            "id_dimension_mp_respuesta": id_dimension_mp_respuesta
        }
        response = requests.post(f"{API_URL}/dimension_mp_respuesta_guardada", json=data)
        response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP no exitosos
        print("Respuesta guardada exitosamente")
    except requests.RequestException as e:
        print(f"Error al guardar la respuesta: {e}")

@vistamediciondepotencial.route('/finalizo', methods=['GET'])
def finalizo():
    # Aquí se mostrará un mensaje de finalización
    return render_template('finalizo.html')
