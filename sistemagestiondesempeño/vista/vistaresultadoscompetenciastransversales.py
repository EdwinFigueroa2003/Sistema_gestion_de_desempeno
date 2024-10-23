from pprint import pprint
from flask import Blueprint, render_template, jsonify
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistaresultadoscompetenciastransversales = Blueprint('idresultadoscompetenciastransversales', __name__, template_folder='templates')

@vistaresultadoscompetenciastransversales.route('/resultadoscompetenciastransversales', methods=['GET'])
def resultadoscompetenciastransversales():
    resultados = []
    
    try:
        # Obtener todas las respuestas de usuario
        response_respuestas = requests.get(f'{API_URL}/usuario_respuesta', timeout=10)
        response_respuestas.raise_for_status()
        respuestas_usuario = response_respuestas.json()

        # Obtener todas las preguntas
        response_preguntas = requests.get(f'{API_URL}/pregunta', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = {p['id_pregunta']: p for p in response_preguntas.json()}

        # Obtener todas las respuestas
        response_respuestas_detalle = requests.get(f'{API_URL}/respuesta', timeout=10)
        response_respuestas_detalle.raise_for_status()
        respuestas_detalle = {r['id_respuesta']: r for r in response_respuestas_detalle.json()}

        for respuesta in respuestas_usuario:
            pregunta = preguntas.get(respuesta['id_pregunta'], {})
            detalle_respuesta = respuestas_detalle.get(respuesta['id_respuesta'], {})
            
            resultados.append({
                'id_usuario_respuesta': respuesta['id_usuario_respuesta'],
                'texto_pregunta': pregunta.get('texto_pregunta', 'Pregunta no disponible'),
                'texto_respuesta': detalle_respuesta.get('texto_respuesta', 'Respuesta no disponible'),
                'valor_respuesta': detalle_respuesta.get('valor_respuesta', 'Valor no disponible'),
                'ruta_de_desarrollo': detalle_respuesta.get('ruta_de_desarrollo', 'Ruta de desarrollo no disponible'),
                'ruta_de_autodesarrollo': detalle_respuesta.get('ruta_de_autodesarrollo', 'Ruta de autodesarrollo no disponible'),
                'fecha_respuesta': respuesta.get('fecha_respuesta', 'Fecha no disponible'),
                'competencia': pregunta.get('competencia', 'Competencia no disponible'),
                'iluo': detalle_respuesta.get('iluo', 'Iluo no disponible'),
                'descripcion_iluo': detalle_respuesta.get('descripcion_iluo', 'Descripción de la iluo no disponible')
            })

        #print("Vista de resultados de competencias transversales", detalle_respuesta)

    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return "Error al obtener los resultados", 500

    return render_template('resultadoscompetenciastransversales.html', respuestas=resultados)
