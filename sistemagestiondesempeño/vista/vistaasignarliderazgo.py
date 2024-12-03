import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistaasignarliderazgo = Blueprint('idasignarliderazgo', __name__, template_folder='templates')

@vistaasignarliderazgo.route('/asignarliderazgo', methods=['GET', 'POST'])
@login_required
def vista_asignarliderazgo():

    # Hacer una solicitud GET a la API para obtener los usuarios
    try:
        response = requests.get(f'{API_URL}/usuario', timeout=10)

        if response.status_code == 200:
            usuarios = response.json()  # Parsear la respuesta en JSON
            print('usuarios')
        else:
            usuarios = []  # En caso de que haya un error
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        usuarios = []

    # Pasar la lista de usuarios a la plantilla
    return render_template('asignarliderazgo.html', usuarios= usuarios)