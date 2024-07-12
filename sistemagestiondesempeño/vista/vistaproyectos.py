from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaproyectos = Blueprint('idproyectos', __name__, template_folder='templates')
 
@vistaproyectos.route('/proyectos', methods=['GET', 'POST'])
def vista_proyectos():
    return render_template('proyectos.html')