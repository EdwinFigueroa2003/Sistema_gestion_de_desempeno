from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests, random
from datetime import datetime
from configBd import API_URL
# Crear un Blueprint
vistaresultadosfactoresclavesdeexito = Blueprint('idresultadosfactoresclavesdeexito', __name__, template_folder='templates')
 
@vistaresultadosfactoresclavesdeexito.route('/resultadosfactoresclavesdeexito', methods=['GET', 'POST'])
def vista_resultados_factores_claves_de_exito():
    return render_template('resultadosfactoresclavesdeexito.html')