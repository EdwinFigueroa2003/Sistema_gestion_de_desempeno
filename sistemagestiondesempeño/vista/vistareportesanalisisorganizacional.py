from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from datetime import datetime
from control.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistareportesanalisisorganizacional = Blueprint('idreportesanalisisorganizacional', __name__, template_folder='templates')

# Ruta para mostrar los resultados al finalizar el cuestionario
@vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET', 'POST'])
def mostrar_reporte():
    # Obtener todas las dimensiones
    dimensiones = requests.get(f"{API_URL}/dimension").json()
    dimensiones_ordenadas = sorted(dimensiones, key=lambda x: x['id_dimension'])

    # Obtener las respuestas guardadas en la sesión
    respuestas_guardadas = session.get('respuestas', {})

    print("Respuestas guardadas en la sesión:", respuestas_guardadas)

    reporte = []
    for dimension in dimensiones_ordenadas:
        id_dimension_str = str(dimension['id_dimension'])
        
        if id_dimension_str in respuestas_guardadas:
            preguntas_respuestas = respuestas_guardadas[id_dimension_str]
            
            for pr in preguntas_respuestas.values():
                reporte.append({
                    'pregunta': pr['pregunta'],
                    'respuesta': pr['respuesta_texto'],
                    'semaforizacion': pr.get('semaforizacion', 'No disponible')
                })

    print("Reporte generado:", reporte)

    return render_template('reportesanalisisorganizacional.html', reporte=reporte)