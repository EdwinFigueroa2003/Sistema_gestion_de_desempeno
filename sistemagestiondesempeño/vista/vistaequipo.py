from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaequipo = Blueprint('idequipo', __name__, template_folder='templates')
 
@vistaequipo.route('/equipo', methods=['GET', 'POST'])
def vista_equipo():
    return render_template('equipo.html')