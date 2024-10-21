from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from configBd import API_URL
 
# Crear un Blueprint
vistaidentificaciondelideres= Blueprint('ididentificaciondelideres', __name__, template_folder='templates')
 
@vistaidentificaciondelideres.route('/identificaciondelideres', methods=['GET', 'POST'])
def vista_identificacion_de_lideres():
    
    return render_template('identificaciondelideres.html')