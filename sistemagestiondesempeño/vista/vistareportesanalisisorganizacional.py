from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistareportesanalisisorganizacional = Blueprint('idreportesanalisisorganizacional', __name__, template_folder='templates')
 
# Ruta para mostrar los resultados al finalizar el cuestionario
@vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET'])
def vista_reportes_analisis_organizacional():
    # Obtener las respuestas desde la sesión
    respuestas = session.get('respuestas', {})
    
    # Aquí puedes procesar las respuestas si es necesario antes de mostrarlas
    return render_template('reportesanalisisorganizacional.html', respuestas=respuestas)

""" @vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET', 'POST'])
def vista_reportes_analisis_organizacional():
    return render_template('reportesanalisisorganizacional.html') """