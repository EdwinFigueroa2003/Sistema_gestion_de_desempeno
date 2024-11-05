import random
from flask import Blueprint, request, render_template, redirect, url_for, session, json
import requests
from configBd import API_URL

# Crear un Blueprint
vistacompetenciasdocentes = Blueprint('idcompetenciasdocentes', __name__, template_folder='templates')

@vistacompetenciasdocentes.route('/competenciasdocentes', methods=['GET', 'POST'])
def vista_competenciasdocentes():
    # Obtener id_usuario desde la sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return redirect(url_for('idvistalogin.vista_login'))  # Redirigir al login si no hay un usuario en sesión

    # Inicializar el índice de la pregunta
    current_index = 0 if request.method == 'GET' else int(request.form.get('current_index', 0))
    respuestas = session.get('respuestas', {})

    # Manejar las respuestas enviadas por el usuario
    if request.method == 'POST' and 'respuesta_seleccionada' in request.form:
        pregunta_id = request.form.get('pregunta_id')
        respuesta_id = request.form.get('respuesta_seleccionada')

        if not pregunta_id:
            session['mensaje_error'] = "ID de pregunta no válido."
            return redirect(url_for('finalizo'))  # O redirigir a donde sea apropiado

        datos_respuesta = {
            'id_seccion_pregunta': int(pregunta_id),
            'id_seccion_respuesta': int(respuesta_id),
            'id_usuario': id_usuario
        }

        # Agregar print para depurar
        print(f"Datos enviados a la API: {datos_respuesta}")

        try:
            response = requests.post(f"{API_URL}/seccion_respuesta_guardada", json=datos_respuesta, timeout=10)
            print(f"Respuesta de la API: {response.status_code}, {response.text}")
            response.raise_for_status()  # Levanta excepción si hay un error en la API

            # Agregar un try-except para manejar errores específicos de la base de datos
            try:
                response.json()  # Intentar convertir la respuesta en JSON
            except json.JSONDecodeError:  # Asegúrate de que esto esté usando el módulo json correcto
                # Manejar el caso en el que la respuesta no sea JSON válido
                print("La respuesta de la API no es JSON válido")
                session['mensaje_error'] = "Hubo un error al procesar la respuesta del servidor."
            else:
                # Si la respuesta es JSON válido, verificar si hay un mensaje de error en la respuesta
                if 'error' in response.json():
                    error_message = response.json()['error']
                    print(f"Error en la API: {error_message}")
                    session['mensaje_error'] = f"Error del servidor: {error_message}"
                else:
                    # Guardar respuesta en la sesión
                    respuestas = session.get('respuestas', {})
                    respuestas[pregunta_id] = respuesta_id
                    session['respuestas'] = respuestas
                    session['mensaje_confirmacion'] = "Respuesta guardada correctamente."
                    print(respuestas)

        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e}")
            session['mensaje_error'] = "Error de conexión al servidor."
        except Exception as e:
            print(f"Error inesperado: {e}")
            session['mensaje_error'] = "Ocurrió un error inesperado."

        if 'next' in request.form:
            current_index += 1
        elif 'prev' in request.form:
            current_index -= 1

    try:
        # Obtener solo las preguntas
        response_preguntas = requests.get(f'{API_URL}/seccion_pregunta', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()

        # Obtener respuestas asociadas a cada pregunta
        response_respuestas = requests.get(f'{API_URL}/seccion_respuesta', timeout=10)
        response_respuestas.raise_for_status()
        todas_respuestas = response_respuestas.json()

        # Asociar las respuestas a sus respectivas preguntas
        for pregunta in preguntas:
            pregunta_id = pregunta['id_seccion_pregunta']
            pregunta['respuestas'] = [r for r in todas_respuestas if r['id_seccion_pregunta'] == pregunta_id]

        # Verificar el índice actual
        if current_index < 0:
            current_index = 0
        if current_index >= len(preguntas):
            return redirect(url_for('finalizo'))

        pregunta_actual = preguntas[current_index]  # Solo obtenemos la pregunta actual

        # Mezclar las respuestas aleatoriamente
        random.shuffle(pregunta_actual['respuestas'])

        print(f"Índice actual: {current_index}")  # Verifica el índice actual
        print(f"Pregunta actual: {pregunta_actual}")  # Verifica la pregunta actual
        print(f"las respuestas son: {preguntas[current_index]['respuestas']}")  # Muestra las respuestas asociadas

        return render_template('competenciasdocentes.html', 
                               pregunta=pregunta_actual, 
                               preguntas=preguntas,
                               current_index=current_index,
                               total_preguntas=len(preguntas), 
                               usuario=session.get('usuario'),
                               mensaje_confirmacion=session.pop('mensaje_confirmacion', None),  
                               mensaje_error=session.pop('mensaje_error', None))  
    except (requests.RequestException, ValueError) as e:
        print(f"Error al obtener o procesar datos: {e}")

    return render_template('competenciasdocentes.html', 
                           pregunta=None, 
                           preguntas=[],
                           current_index=current_index,
                           error_message=str(e),
                           mensaje_error="Hubo un error al obtener los datos. Inténtalo de nuevo.")  # Añadir esta línea