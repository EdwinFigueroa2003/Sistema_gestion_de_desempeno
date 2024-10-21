from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistacompetenciasdocentes = Blueprint('idcompetenciasdocentes', __name__, template_folder='templates')
 
@vistacompetenciasdocentes.route('/competenciasdocentes', methods=['GET', 'POST'])
def vista_competenciasdocentes():

    return render_template('competenciasdocentes.html')