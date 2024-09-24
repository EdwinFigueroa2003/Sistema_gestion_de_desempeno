import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from datetime import datetime
from control.ControlEntidad import ControlEntidad
from configBd import API_URL
 
# Crear un Blueprint
vistaequipo = Blueprint('idequipo', __name__, template_folder='templates')
 
@vistaequipo.route('/equipo', methods=['GET', 'POST'])
def vista_equipo():
    # Hacer una solicitud GET a la API para obtener los usuarios
    try:
        response = requests.get(f'{API_URL}/usuario', timeout=10)

        #response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)

        if response.status_code == 200:
            usuarios = response.json()  # Parsear la respuesta en JSON
        else:
            usuarios = []  # En caso de que haya un error
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        usuarios = []

    # Renderizar la plantilla 'equipo.html' con los usuarios obtenidos
    return render_template('equipo.html', usuarios=usuarios)