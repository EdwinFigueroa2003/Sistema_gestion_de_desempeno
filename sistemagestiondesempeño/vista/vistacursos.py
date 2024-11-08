import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistacursos = Blueprint('idcursos', __name__, template_folder='templates')

@vistacursos.route('/cursos', methods=['GET'])
@login_required
def vista_cursos():
    try:
        cursos = requests.get(f"{API_URL}/tipo_curso").json()
    except requests.RequestException as e:
        print(f"Error al obtener los cursos: {e}")
        cursos = []
    return render_template('cursos.html', cursos=cursos)


