import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistaotrascontribuciones = Blueprint('idotrascontribuciones', __name__, template_folder='templates')
 
@vistaotrascontribuciones.route('/otrascontribuciones', methods=['GET', 'POST'])
@login_required
def vista_otras_contribuciones():
    return render_template('otrascontribuciones.html')