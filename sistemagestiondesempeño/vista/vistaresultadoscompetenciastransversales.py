from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from control.ControlEntidad import ControlEntidad
from vista.vistacompetenciastransversales import API_URL
 
# Crear un Blueprint
vistaresultadoscompetenciastransversales = Blueprint('idresultadoscompetenciastransversales', __name__, template_folder='templates')
 
@vistaresultadoscompetenciastransversales.route('/resultadoscompetenciastransversales', methods=['GET', 'POST'])
def resultadoscompetenciastransversales():
    respuestas = session.get('respuestas', {})
    
    preguntas_respuestas = []
    for id_pregunta, id_respuesta in respuestas.items():
        try:
            # Verifica que el endpoint para obtener preguntas por ID sea correcto
            response_pregunta = requests.get(f'{API_URL}/pregunta/id_pregunta/{id_pregunta}', timeout=10)
            response_pregunta.raise_for_status()
            pregunta = response_pregunta.json()

            # Imprimir la respuesta de la API para depuración
            print(f"Respuesta de pregunta: {pregunta}")

            # Si es una lista, accede al primer elemento
            if isinstance(pregunta, list) and len(pregunta) > 0:
                pregunta = pregunta[0]
            
            # Verifica que el endpoint para obtener respuestas por ID sea correcto
            response_respuesta = requests.get(f'{API_URL}/respuesta/id_respuesta/{id_respuesta}', timeout=10)
            response_respuesta.raise_for_status()
            respuesta = response_respuesta.json()

            # Imprimir la respuesta de la API para depuración
            print(f"Respuesta de respuesta: {respuesta}")

            # Si es una lista, accede al primer elemento
            if isinstance(respuesta, list) and len(respuesta) > 0:
                respuesta = respuesta[0]

            preguntas_respuestas.append({
                'texto_pregunta': pregunta.get('texto_pregunta', 'Pregunta no disponible'),
                'texto_respuesta': respuesta.get('texto_respuesta', 'Respuesta no disponible'),
                'valor_respuesta': respuesta.get('valor_respuesta', 'valor no disponible')
            })

        except requests.RequestException as e:
            print(f"Error al obtener datos: {e}")

    return render_template('resultadoscompetenciastransversales.html', respuestas=preguntas_respuestas)
