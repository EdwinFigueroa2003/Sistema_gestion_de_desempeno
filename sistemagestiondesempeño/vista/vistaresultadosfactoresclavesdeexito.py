import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistaresultadosfactoresclavesdeexito = Blueprint('idresultadosfactoresclavesdeexito', __name__, template_folder='templates')
 
@vistaresultadosfactoresclavesdeexito.route('/resultadosfactoresclavesdeexito', methods=['GET', 'POST'])
@login_required
def vista_resultados_factores_claves_de_exito():
    return render_template('resultadosfactoresclavesdeexito.html')