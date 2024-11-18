import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistavercurso = Blueprint('idvercurso', __name__, template_folder='templates')
@login_required
def format_date_safely(date_string):
    if date_string:
        try:
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return "Fecha inválida"
    return "No disponible"

@vistavercurso.route('/vercurso/<int:curso_id>', methods=['GET'])
@login_required
def vista_ver_curso(curso_id):
    try:
        response = requests.get(f"{API_URL}/cursos/id_tipo_curso/{curso_id}")
        response.raise_for_status()
        cursos = response.json()  # Cambié 'curso' a 'cursos'
        
        if cursos:  # Verifica si la lista no está vacía
            curso = cursos[0]  # Accede al primer curso de la lista
        else:
            curso = None
        
        # Formatear las fechas de manera segura
        curso['fecha_limite_inscripcion'] = format_date_safely(curso.get('fecha_limite_inscripcion'))
        curso['fecha_inicio'] = format_date_safely(curso.get('fecha_inicio'))
        curso['fecha_fin'] = format_date_safely(curso.get('fecha_fin'))
        curso['fecha_creacion'] = format_date_safely(curso.get('fecha_creacion'))
        curso['fecha_actualizacion'] = format_date_safely(curso.get('fecha_actualizacion'))
        
        print(f"Datos del curso recibidos: {curso}")
        
    except requests.RequestException as e:
        print(f"Error al obtener el curso: {e}")
        print(f"Respuesta del servidor: {e.response.text if e.response else 'No hay respuesta'}")
        curso = None
    return render_template('vercurso.html', curso=curso)

@vistavercurso.route('/cursos/actualizar/<int:id>', methods=['POST'])
@login_required
def actualizar_curso(id):
    if session['usuario']['fk_rol_usu'] != 1:
        return redirect(url_for('idcursos.vista_cursos'))

    # Obtener los datos del formulario o JSON
    data = request.json or request.form
    titulo = data.get('titulo')

    # Lógica para actualizar el curso usando la nueva estructura
    try:
        payload = {
            "procedure": "update_json_entity",
            "parameters": {
                "table_name": "cursos",
                "json_data": {
                    "titulo": titulo
                },
                "where_condition": f"id = {id}"
            }
        }
        response = requests.post(f"{API_URL}/procedures/execute", json=payload)
        print('Respuesta de la API:', response.status_code, response.text)  # Print para verificar la respuesta de la API

        return redirect(url_for('idcursos.vista_cursos'))
    except requests.RequestException as e:
        print(f"Error al actualizar el curso: {e}")
        return redirect(url_for('idcursos.vista_cursos'))