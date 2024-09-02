from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistacompetenciastransversales = Blueprint('idcompetenciastransversales', __name__, template_folder='templates')

@vistacompetenciastransversales.route('/competenciastransversales', methods=['GET', 'POST'])
def get_competencias():
    response = requests.get('http://190.217.58.246:5184/api/sgd/competencia')
    try:
        competencias = response.json()  # Decodificar la respuesta como JSON
    except requests.exceptions.JSONDecodeError:
        return "Error: La respuesta no es un JSON válido.", 500

    current_index = int(request.form.get('current_index', 0))

    # Manejo de índice de la pregunta actual
    if request.method == 'POST':
        respuesta_seleccionada = request.form.get('respuesta', None)
        print(f"Respuesta seleccionada: {respuesta_seleccionada}")  # Debugging
        if respuesta_seleccionada:
            # Guardar respuesta en la sesión
            if 'respuestas' not in session:
                session['respuestas'] = []
            session['respuestas'].append(respuesta_seleccionada)
            session.modified = True

            """ print("Respuesta seleccionada:", respuesta_seleccionada)
            print("Respuestas hasta ahora:", session['respuestas']) """

        if 'next' in request.form:
            current_index += 1
            if current_index >= len(competencias):
                return redirect(url_for('finalizo'))  # Redirigir a resultados1.html cuando se llega al final
        elif 'prev' in request.form:
            if current_index > 0:
                current_index -= 1

    pregunta_actual = competencias[current_index]
    return render_template('competenciastransversales.html', item=pregunta_actual, current_index=current_index)
