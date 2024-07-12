from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaagregarequipo = Blueprint('idagregarequipo', __name__, template_folder='templates')
 
@vistaagregarequipo.route('/agregarequipo', methods=['GET', 'POST'])
def vista_agregar_equipo():
    return render_template('agregarequipo.html')