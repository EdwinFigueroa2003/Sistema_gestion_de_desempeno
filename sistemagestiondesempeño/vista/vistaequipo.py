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

        if response.status_code == 200:
            usuarios = response.json()  # Parsear la respuesta en JSON
        else:
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

    else:
        print(f"Usuarios: {usuarios}")  # Imprimir usuarios en consola


    # Renderizar la plantilla 'equipo.html' con los usuarios obtenidos
    return render_template('equipo.html', usuarios=usuarios)

def get_fk_nivel_contribucion_by_usuario(id_usuario, niveles):
    # Aquí debes tener tu lógica para determinar el fk_nivel_de_contribucion
    # Esto es solo un ejemplo y debe ser reemplazado con tu lógica real
    for nivel in niveles:
        if nivel['id_nivel'] == id_usuario:  # Asumiendo que el id_usuario se puede relacionar con el id_nivel
            return nivel['id_nivel']
    return None  # O un valor por defecto si no se encuentra

def seleccionar_usuario_equipo():
    id_usuario = request.form.get('id_usuario')
    
    # Obtener el nivel de contribución del usuario
    try:
        response_nivel = requests.get(f'{API_URL}/sgd/nivel_contrib', timeout=10)
        response_nivel.raise_for_status()
        niveles = response_nivel.json()
        
        # Suponiendo que tienes un método para obtener el fk_nivel_de_contribucion por id_usuario
        fk_nivel_de_contribucion = get_fk_nivel_contribucion_by_usuario(id_usuario, niveles)
        
        session['fk_nivel_de_contribucion'] = fk_nivel_de_contribucion
    except requests.RequestException as e:
        print(f"Error al obtener niveles de contribución: {e}")
    
    session['id_usuario_seleccionado'] = id_usuario
    return redirect(url_for('idcompetenciastransversales.vista_competenciastransversales'))