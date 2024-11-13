from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, flash
import requests
from configBd import API_URL
from flask_login import login_required, current_user
import random
 
# Crear un Blueprint
vistacompetenciastransversales = Blueprint('idcompetenciastransversales', __name__, template_folder='templates')
 
@vistacompetenciastransversales.route('/competenciastransversales', methods=['GET', 'POST'])
@login_required
def vista_competenciastransversales():
    # Confirmar que el usuario esté autenticado y tenga el rol adecuado
    print(f"Debug: Usuario autenticado: {current_user.is_authenticated}")
 
    fk_nivel_de_contribucion = session.get('fk_nivel_de_contribucion')
    id_usuario = session.get('id_usuario')
    # Validar la existencia de `id_usuario` y `fk_nivel_de_contribucion`
    if not id_usuario or not fk_nivel_de_contribucion:
        print("Debug: `id_usuario` o `fk_nivel_de_contribucion` no están presentes en la sesión.")
        return redirect(url_for('idvistalogin.vista_login'))
 
    current_index = 0 if request.method == 'GET' else int(request.form.get('current_index', 0))
    respuestas = session.get('respuestas', {})
 
    # Manejar las respuestas enviadas por el usuario
    if request.method == 'POST' and 'respuesta_seleccionada' in request.form:
        pregunta_id = request.form.get('pregunta_id')
        respuesta_id = request.form.get('respuesta_seleccionada')
 
        datos_respuesta = {
            'id_pregunta': int(pregunta_id),
            'id_respuesta': int(respuesta_id),
            'id_usuario': id_usuario
        }
        try:
            response = requests.post(f"{API_URL}/usuario_respuesta", json=datos_respuesta, timeout=10)
            response.raise_for_status()
            respuestas = session.get('respuestas', {})
            respuestas[pregunta_id] = respuesta_id
            session['respuestas'] = respuestas
            session['mensaje_confirmacion'] = "Respuesta guardada correctamente."
        except requests.RequestException as e:
            print(f"Error al guardar la respuesta en la API: {e}")
            session['mensaje_error'] = "Hubo un error al guardar la respuesta. Inténtalo de nuevo."
        if 'next' in request.form:
            current_index += 1
        elif 'prev' in request.form:
            current_index -= 1
 
    try:
        response_preguntas = requests.get(f'{API_URL}/pregunta/fk_nivel_de_contribucion/{fk_nivel_de_contribucion}', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()
        if not isinstance(preguntas, list) or not preguntas:
            raise ValueError("La respuesta de la API no es una lista de preguntas válidas")
 
        if current_index < 0:
            current_index = 0
        if current_index >= len(preguntas):
            return redirect(url_for('finalizo'))
 
        pregunta_actual = preguntas[current_index]
        id_pregunta = pregunta_actual.get('id_pregunta')
 
        response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
        response_respuestas.raise_for_status()
        respuestas_list = response_respuestas.json()
        random.shuffle(respuestas_list)
        pregunta_actual['respuestas'] = respuestas_list
 
        return render_template('competenciastransversales.html',
                               pregunta=pregunta_actual,
                               preguntas=preguntas,
                               current_index=current_index,
                               total_preguntas=len(preguntas),
                               usuario=session.get('usuario'),
                               mensaje_confirmacion=session.pop('mensaje_confirmacion', None),
                               mensaje_error=session.pop('mensaje_error', None))
    except (requests.RequestException, ValueError) as e:
        print(f"Error al obtener o procesar datos: {e}")
        return render_template('competenciastransversales.html',
                               pregunta=None,
                               preguntas=[],
                               current_index=current_index,
                               error_message=str(e),
                               mensaje_error="Hubo un error al obtener los datos. Inténtalo de nuevo.")
 
@vistacompetenciastransversales.route('/competenciastransversales/editar/<int:pregunta_id>', methods=['GET', 'POST'])
@login_required
def editar_pregunta(pregunta_id):
    # Verificar si el usuario es administrador
    if current_user.fk_rol_usu != '1':
        flash("No tienes permiso para acceder a esta función.", "error")
        return redirect(url_for('idcompetenciastransversales.vista_competenciastransversales'))

    if request.method == 'POST':
        # Obtener datos de la pregunta y respuestas desde el formulario
        nuevo_texto_pregunta = request.form.get('texto_pregunta')
        datos_edicion = {
            'id_pregunta': pregunta_id,
            'texto_pregunta': nuevo_texto_pregunta,
            'respuestas': []
        }

        # Obtener respuestas editadas y añadirlas a 'datos_edicion'
        respuestas_ids = request.form.getlist('respuesta_id')
        respuestas_textos = request.form.getlist('texto_respuesta')

        for res_id, texto in zip(respuestas_ids, respuestas_textos):
            datos_edicion['respuestas'].append({
                'id_respuesta': int(res_id),
                'texto_respuesta': texto
            })

        try:
            # Enviar los datos editados a la API
            response = requests.post(f"http://127.0.0.1:5184/api/sgd/editar_pregunta", json=datos_edicion, timeout=10)
            response.raise_for_status()
            flash("Pregunta y respuestas editadas correctamente.", "success")
        except requests.RequestException as e:
            print(f"Error al editar la pregunta o respuestas en la API: {e}")
            flash("Hubo un error al editar la pregunta o respuestas.", "error")
        return redirect(url_for('idcompetenciastransversales.vista_competenciastransversales'))

    # Obtener la pregunta actual para mostrarla en el formulario de edición
    try:
        response_pregunta = requests.get(f"{API_URL}/pregunta/{pregunta_id}", timeout=10)
        response_pregunta.raise_for_status()
        pregunta_actual = response_pregunta.json()

        response_respuestas = requests.get(f"{API_URL}/respuesta/id_pregunta/{pregunta_id}", timeout=10)
        response_respuestas.raise_for_status()
        pregunta_actual['respuestas'] = response_respuestas.json()
    except requests.RequestException as e:
        print(f"Error al obtener la pregunta o respuestas de la API: {e}")
        flash("Hubo un error al cargar la pregunta o respuestas.", "error")
        return redirect(url_for('idcompetenciastransversales.vista_competenciastransversales'))

    return render_template('editar_pregunta.html', pregunta=pregunta_actual)
