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

@vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET'])
def mostrar_reporte():
    try:
        # Obtener todas las respuestas guardadas a través de la API
        respuestas = requests.get(f"{API_URL}/dimension_respuesta_guardada").json()

        reporte = []
        for respuesta in respuestas:
            # Obtener detalles de la pregunta
            pregunta = requests.get(f"{API_URL}/dimension_pregunta/{respuesta['id_dimension_pregunta']}").json()
            
            # Obtener detalles de la respuesta
            respuesta_detalle = requests.get(f"{API_URL}/dimension_respuesta/{respuesta['id_dimension_respuesta']}").json()

            reporte.append({
                'pregunta': pregunta['pregunta'],
                'respuesta': respuesta_detalle['respuesta'],
                'semaforizacion': respuesta_detalle['semaforizacion']
            })

        return render_template('reportesanalisisorganizacional.html', reporte=reporte)
    
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud a la API: {e}")
        return render_template('error.html', mensaje="Error al obtener el reporte")
    

