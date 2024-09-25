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

@vistainforme.route('/informe/<string:email>', methods=['GET'])
def vista_informe(email):
    usuario = None  # Inicializa usuario

    try:
        response = requests.get(f'{API_URL}/usuario/email/{email}', timeout=10)

        if response.status_code == 200:
            usuario = response.json()
            print("Datos del usuario:", usuario)  # Debug: muestra los datos del usuario
            print("Datos del usuario antes de renderizar:", usuario)
            if isinstance(usuario, dict):
                print("Claves en el diccionario usuario:", usuario.keys())  # Debug: claves
        else:
            usuario = None
            print(f"Error en la solicitud: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Excepción en la solicitud: {e}")

    return render_template('informe.html', usuario=usuario)