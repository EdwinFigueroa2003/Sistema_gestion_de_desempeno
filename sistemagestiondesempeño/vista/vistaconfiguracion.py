from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistaconfiguracion = Blueprint('idconfiguracion', __name__, template_folder='templates')
 
@vistaconfiguracion.route('/configuracion', methods=['GET', 'POST'])
def vista_configuracion():
    return render_template('configuracion.html')