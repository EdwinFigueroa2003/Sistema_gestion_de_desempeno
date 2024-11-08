import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistaconfiguracion = Blueprint('idconfiguracion', __name__, template_folder='templates')
 


@vistaconfiguracion.route('/configuracion', methods=['GET', 'POST'])
@login_required
def vista_configuracion():
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return redirect(url_for('idvistalogin.vista_login'))
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        facultad = request.form.get('facultad')
        cargo = request.form.get('cargo')
        foto = request.form.get('foto_usu')

        # Actualizar los datos del usuario en la API
        try:
            update_data = {
                'nombre': nombre,
                'facultad': facultad,
                'fk_cargo_usu': int(cargo),
                'foto_usu': foto if foto else "default.jpg"
            }
            print("Datos a actualizar:", update_data)
            response = requests.put(f"{API_URL}/usuario/id_usuario/{id_usuario}", json=update_data)
            response.raise_for_status()            
        except requests.exceptions.RequestException as e:
            print(f"Error al actualizar los datos del usuario: {e}")

    # Obtener datos del usuario desde la API
    try:
        response = requests.get(f"{API_URL}/usuario/id_usuario/{id_usuario}")
        response.raise_for_status()
        datos_usuario = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los datos del usuario: {e}")
        datos_usuario = {}

    return render_template('configuracion.html', datos_usuario=datos_usuario)