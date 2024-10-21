from flask import Blueprint, render_template, request
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests

# Crear un Blueprint
vistacursos = Blueprint('idcursos', __name__, template_folder='templates')

@vistacursos.route('/cursos', methods=['GET'])
def vista_cursos():
    try:
        cursos = requests.get(f"{API_URL}/tipo_curso").json()
        #cursos = requests.get(f"{API_URL}/tipo_curso/id_rol/2").json() #esto lo que hace es filtrar por rol de manera manual
        #print(cursos)  # Esto te ayudará a ver qué estructura tiene el objeto que recibes
    except requests.RequestException as e:
        print(f"Error al obtener los cursos: {e}")
        cursos = []
    return render_template('cursos.html', cursos=cursos)


