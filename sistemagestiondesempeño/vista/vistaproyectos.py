from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
from configBd import API_URL

# Crear un Blueprint
vistaproyectos = Blueprint('idproyectos', __name__, template_folder='templates')

@vistaproyectos.route('/proyectos', methods=['GET', 'POST'])
def vista_proyectos():
    try:
        # Realizar la solicitud a la API para obtener todos los proyectos
        response = requests.get(f'{API_URL}/proyecto', timeout=10)

        # Si la solicitud es exitosa, obtener los proyectos
        if response.status_code == 200:
            proyectos = response.json()  # Obtener proyectos en formato JSON
        else:
            proyectos = []  # Si la solicitud falla, usar una lista vacía
    except Exception as e:
        print(f"Error al obtener los proyectos: {e}")
        proyectos = []  # En caso de error, usar una lista vacía

    # Renderizar la plantilla HTML con los proyectos
    return render_template('proyectos.html', proyectos=proyectos)
