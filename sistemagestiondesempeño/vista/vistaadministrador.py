import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistaadministrador = Blueprint('idadministrador', __name__, template_folder='templates')

@vistaadministrador.route('/administrador', methods=['GET', 'POST'])
@login_required
def vista_administrador():
    # Hacer una solicitud GET a la API para obtener los usuarios
    try:
        response = requests.get(f'{API_URL}/usuario', timeout=10)
        if response.status_code == 200:
            usuarios = response.json()  # Parsear la respuesta en JSON
            print("Usuarios obtenidos de la API:", usuarios)  # Agregar mensaje de depuración
        else:
            print(f"Error en la solicitud a la API: {response.status_code}")
            usuarios = []  # En caso de que haya un error
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        usuarios = []

    # Si se ha enviado un formulario de búsqueda
    if request.method == 'POST':
        nombre_colaborador = request.form.get('nombre_colaborador', '').strip().lower()
        # Filtrar los usuarios según el nombre ingresado
        usuarios = [usuario for usuario in usuarios if nombre_colaborador in usuario['nombre'].lower()]
        print(f"Usuarios filtrados: {usuarios}")  # Imprimir usuarios filtrados en consola

    return render_template('administrador.html', usuarios=usuarios)
