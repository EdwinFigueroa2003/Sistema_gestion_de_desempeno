import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistaresultados = Blueprint('idresultados', __name__, template_folder='templates')
 
@vistaresultados.route('/resultados', methods=['GET', 'POST'])
@login_required
def vista_resultados():
    return render_template('resultados.html')