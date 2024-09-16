from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from datetime import datetime
from control.ControlEntidad import ControlEntidad
 
#API_URL = 'http://127.0.0.1:5184/api/sgd'
API_URL = 'http://190.217.58.246:5184/api/sgd'

# Crear un Blueprint
vistacompetenciastransversales = Blueprint('idcompetenciastransversales', __name__, template_folder='templates')

@vistacompetenciastransversales.route('/competenciastransversales', methods=['GET', 'POST'])
def vista_competenciastransversales():
    id_apartado = 1  # Cambia este valor si fuera necesario
    user_id = 1  # Cambia esto según sea necesario

    if request.method == 'POST':
        respuestas = {}
        for id_pregunta, id_respuesta in request.form.items():
            respuestas[id_pregunta] = id_respuesta

        # Guardar las respuestas en la sesión o en una estructura temporal
        session['respuestas'] = respuestas

        return redirect(url_for('finalizo'))

    try:
         # Obtener las preguntas para el apartado
        response_preguntas = requests.get(f'{API_URL}/pregunta/id_apartado/{id_apartado}', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()

        # Obtener respuestas para cada pregunta
        for pregunta in preguntas:
            id_pregunta = pregunta['id_pregunta']
            response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
            response_respuestas.raise_for_status()
            pregunta['respuestas'] = response_respuestas.json()

    except requests.RequestException as e:
        preguntas = []
        print(f"Error al obtener datos: {e}")

    return render_template('competenciastransversales.html', preguntas=preguntas)

""" 
def vista_competenciastransversales():
    id_apartado = 1  # Cambia este valor si fuera necesario

    try:
        # Obtener las preguntas para el apartado
        response_preguntas = requests.get(f'{API_URL}/pregunta/id_apartado/{id_apartado}', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()

        # Obtener respuestas para cada pregunta
        for pregunta in preguntas:
            id_pregunta = pregunta['id_pregunta']
            response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
            response_respuestas.raise_for_status()
            pregunta['respuestas'] = response_respuestas.json()

    except requests.RequestException as e:
        preguntas = []
        print(f"Error al obtener datos: {e}")

    if request.method == 'POST':
        user_id = 1  # Cambia esto según sea necesario
        for id_pregunta, id_respuesta in request.form.items():
            data = {
                'id_usuario': user_id,
                'id_pregunta': id_pregunta,
                'id_respuesta': id_respuesta,
                'fecha_respuesta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Campo corregido
            }
            print("Payload:", data)  # Imprime el payload para depuración

            headers = {
                        'Content-Type': 'application/json'
                        }                   

            try:
                response = requests.post(f'{API_URL}/usuario_respuesta', json=data, headers=headers)
                print("Status Code:", response.status_code)  # Imprime el código de estado HTTP
                print("Response Text:", response.text)  # Imprime el contenido de la respuesta
                response.raise_for_status()  # Levanta una excepción si la respuesta tiene un error HTTP
                response_json = response.json()  # Intenta decodificar la respuesta como JSON
            except requests.RequestException as e:
                print(f"Error al enviar respuesta: {e}")
            except ValueError as e:
                print(f"Error al decodificar JSON: {e}")
        return redirect(url_for('finalizo', usuario_id=user_id))

    return render_template('competenciastransversales.html', preguntas=preguntas) 
 """