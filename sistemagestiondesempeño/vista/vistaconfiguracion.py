from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaconfiguracion = Blueprint('idconfiguracion', __name__, template_folder='templates')
 
@vistaconfiguracion.route('/configuracion', methods=['GET', 'POST'])
def vista_configuracion():
    return render_template('configuracion.html')