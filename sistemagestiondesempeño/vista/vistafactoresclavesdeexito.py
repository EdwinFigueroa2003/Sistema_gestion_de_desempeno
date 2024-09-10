from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
import requests

 
# Crear un Blueprint
vistafactoresclavesdeexito = Blueprint('idfactoresclavesdeexito', __name__, template_folder='templates')

@vistafactoresclavesdeexito.route('/factoresclavesdeexito', methods=['GET', 'POST'])
def get_factoresclavesdeexito():
    response = requests.get('http://190.217.58.246:5184/api/sgd/competencia')
    try:
        competencias = response.json()  # Decodificar la respuesta como JSON
    except requests.exceptions.JSONDecodeError:
        return "Error: La respuesta no es un JSON válido.", 500

    current_index = int(request.form.get('current_index', 0))

    # Manejo de índice de la pregunta actual
    if request.method == 'POST':
        if 'next' in request.form:
            current_index += 1
            if current_index >= len(competencias):
                return redirect(url_for('finalizo'))  # Redirigir a finalizo.html cuando se llega al final
        elif 'prev' in request.form:
            if current_index > 0:
                current_index -= 1

    pregunta_actual = competencias[current_index]
    return render_template('factoresclavesdeexito.html', item=pregunta_actual, current_index=current_index)