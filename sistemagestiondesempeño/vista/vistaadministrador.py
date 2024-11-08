import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

# Crear un Blueprint
vistaadministrador = Blueprint('idadministrador', __name__, template_folder='templates')

@vistaadministrador.route('/administrador', methods=['GET', 'POST'])
@login_required
def vista_administrador():

    # Pasar la lista de usuarios a la plantilla
    return render_template('administrador.html')
