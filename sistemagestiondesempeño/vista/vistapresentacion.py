from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistapresentacion = Blueprint('idpresentacion', __name__, template_folder='templates')
 
@vistapresentacion.route('/presentacion', methods=['GET', 'POST'])
def vista_presentacion():
    return render_template('presentacion.html')