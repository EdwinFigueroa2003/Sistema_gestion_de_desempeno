from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaotrascontribuciones = Blueprint('idotrascontribuciones', __name__, template_folder='templates')
 
@vistaotrascontribuciones.route('/otrascontribuciones', methods=['GET', 'POST'])
def vista_otras_contribuciones():
    return render_template('otrascontribuciones.html')