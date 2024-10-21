from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistaresultadoscompetenciasdocentes = Blueprint('idresultadoscompetenciasdocentes', __name__, template_folder='templates')
 
@vistaresultadoscompetenciasdocentes.route('/resultadoscompetenciasdocentes', methods=['GET', 'POST'])
def vista_resultadoscompetenciasdocentes():

    return render_template('resultadoscompetenciasdocentes.html')
