import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from datetime import datetime
from control.ControlEntidad import ControlEntidad
from configBd import API_URL

# Crear un Blueprint
vistainforme = Blueprint('idinforme', __name__, template_folder='templates')

@vistainforme.route('/informe/<int:id_usuario>', methods=['GET'])
def vista_informe(id_usuario):
    try:
        response = requests.get(f'{API_URL}/usuario/id_usuario/{id_usuario}', timeout=10)

        if response.status_code == 200:
            usuario = response.json()
            print("Datos del usuario:", usuario)
            print("Tipo de datos del usuario:", type(usuario))
            if isinstance(usuario, dict):
                print("Claves en el diccionario usuario:", usuario.keys())
        else:
            usuario = None
            print(f"Error en la solicitud: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        usuario = None
        print(f"Excepción en la solicitud: {e}")
    
    return render_template('informe.html', usuario=usuario)
