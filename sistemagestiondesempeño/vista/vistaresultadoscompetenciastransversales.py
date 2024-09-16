from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaresultadoscompetenciastransversales = Blueprint('idresultadoscompetenciastransversales', __name__, template_folder='templates')
 
@vistaresultadoscompetenciastransversales.route('/resultadoscompetenciastransversales', methods=['GET', 'POST'])
def vista_resultadoscompetenciastransversales():
    return render_template('resultadoscompetenciastransversales.html')



""" @app.route('/resultadoscompetenciastransversales', methods = ['GET', 'POST'])
def get_resultadoscompetenciastransversales():
    respuestas = session.get('respuestas', [])  # Obtener las respuestas de la sesión
    return render_template('resultadoscompetenciastransversales.html', respuestas=respuestas) """