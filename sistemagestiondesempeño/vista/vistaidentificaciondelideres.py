import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistaidentificaciondelideres= Blueprint('ididentificaciondelideres', __name__, template_folder='templates')
 
@vistaidentificaciondelideres.route('/identificaciondelideres', methods=['GET', 'POST'])
@login_required
def vista_identificacion_de_lideres():
    
    return render_template('identificaciondelideres.html')