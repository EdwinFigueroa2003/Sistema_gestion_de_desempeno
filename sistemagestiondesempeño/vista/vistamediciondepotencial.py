from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests, random
from datetime import datetime
from control.ControlEntidad import ControlEntidad


# Crear un Blueprint
vistamediciondepotencial = Blueprint('idmediciondepotencial', __name__, template_folder='templates')

@vistamediciondepotencial.route('/mediciondepotencial', methods=['GET', 'POST'])
def vista_medicion_potencial():
    # Limpiar la sesión para empezar de nuevo
    #session.pop('respuestas', None)  # Eliminar respuestas anteriores, si existen

    # Obtener las preguntas de la dimensión
    preguntas = requests.get(f"{API_URL}/dimension_mp_pregunta").json()
    
    # Obtener el índice actual de la pregunta
    current_index = int(request.args.get('current_index', 0))
    
    if request.method == 'POST':
        respuesta_seleccionada_id = request.form.get('respuesta')
        print(f"Respuesta seleccionada: {respuesta_seleccionada_id}")  # Depuración
        
        if respuesta_seleccionada_id:
            respuesta_seleccionada_id = int(respuesta_seleccionada_id)  # Asegúrate de que es un entero
            
            if 'respuestas' not in session:
                session['respuestas'] = []  # Inicializa como lista
            session['respuestas'].append(respuesta_seleccionada_id)  # Usa .append()
            print(f"Respuestas en la sesión: {session['respuestas']}")  # Depuración
            session.modified = True
            
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
    
    # Obtener la pregunta actual
    pregunta_actual = preguntas[current_index]
    
    # Obtener las respuestas de la pregunta actual
    respuestas = requests.get(f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_pregunta/{pregunta_actual['id_dimension_mp_pregunta']}").json()

    # Mezclar las respuestas aleatoriamente
    random.shuffle(respuestas)
    
    return render_template(
        'mediciondepotencial.html',
        pregunta_actual=pregunta_actual,
        respuestas=respuestas,
        current_index=current_index,
        total_preguntas=len(preguntas)
    )



@vistamediciondepotencial.route('/finalizo', methods=['GET'])
def finalizo():
    # Aquí se mostrará un mensaje de finalización
    return render_template('finalizo.html')