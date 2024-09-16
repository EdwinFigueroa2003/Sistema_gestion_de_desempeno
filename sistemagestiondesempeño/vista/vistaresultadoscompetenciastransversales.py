from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from control.ControlEntidad import ControlEntidad
from vista.vistacompetenciastransversales import API_URL
 
# Crear un Blueprint
vistaresultadoscompetenciastransversales = Blueprint('idresultadoscompetenciastransversales', __name__, template_folder='templates')
 
@vistaresultadoscompetenciastransversales.route('/resultadoscompetenciastransversales', methods=['GET', 'POST'])
def vista_resultadoscompetenciastransversales():
    respuestas = session.get('respuestas', {})
    
    preguntas_respuestas = []
    for id_pregunta, id_respuesta in respuestas.items():
        try:
            # Verifica que el endpoint para obtener preguntas por ID sea correcto
            response_pregunta = requests.get(f'{API_URL}/pregunta/id_pregunta/{id_pregunta}', timeout=10)
            response_pregunta.raise_for_status()
            pregunta = response_pregunta.json()
            
            # Verifica que el endpoint para obtener respuestas por ID sea correcto
            response_respuesta = requests.get(f'{API_URL}/respuesta/id_respuesta/{id_respuesta}', timeout=10)
            response_respuesta.raise_for_status()
            respuesta = response_respuesta.json()

            preguntas_respuestas.append({
                'texto_pregunta': pregunta['texto_pregunta'],
                'texto_respuesta': respuesta['texto_respuesta'],
                'valor_respuesta': respuesta['valor_respuesta']
            })

        except requests.RequestException as e:
            print(f"Error al obtener datos: {e}")

    return render_template('resultadoscompetenciastransversales.html', respuestas=preguntas_respuestas)



""" @app.route('/resultadoscompetenciastransversales', methods = ['GET', 'POST'])
def get_resultadoscompetenciastransversales():
    respuestas = session.get('respuestas', [])  # Obtener las respuestas de la sesión
    return render_template('resultadoscompetenciastransversales.html', respuestas=respuestas) """