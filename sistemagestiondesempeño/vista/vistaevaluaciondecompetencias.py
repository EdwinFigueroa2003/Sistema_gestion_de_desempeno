from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from configBd import API_URL
 
# Crear un Blueprint
vistaevaluaciondecompetencias = Blueprint('idevaluaciondecompetencias', __name__, template_folder='templates')
 
@vistaevaluaciondecompetencias.route('/evaluaciondecompetencias', methods=['GET', 'POST'])
def vista_evaluacion_de_competencias():
    return render_template('evaluaciondecompetencias.html')