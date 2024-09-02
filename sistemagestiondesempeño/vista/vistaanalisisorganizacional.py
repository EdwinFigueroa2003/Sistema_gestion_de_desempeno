from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
import requests
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaanalisisorganizacional = Blueprint('idanalisisorganizacional', __name__, template_folder='templates')
 
""" @vistareportes.route('/analisisorganizacional', methods=['GET', 'POST'])
def vista_reportes():
    return render_template('reportes.html') """

@vistaanalisisorganizacional.route('/analisisorganizacional', methods = ['GET', 'POST'])
def get_dimensiones():
    
    response = requests.get('http://190.217.58.246:5184/api/sgd/dimension')
    try:
        data = response.json()  # Intenta decodificar la respuesta como JSON
    except requests.exceptions.JSONDecodeError:
        return "Error: La respuesta no es un JSON válido.", 500
    # Aquí puedes pasar 'data' a la plantilla HTML que desees renderizar.
    return render_template('analisisorganizacional.html', data=data)