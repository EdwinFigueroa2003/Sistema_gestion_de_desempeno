from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistainfoproyectos = Blueprint('idinfoproyectos', __name__, template_folder='templates')
 
@vistainfoproyectos.route('/infoproyectos', methods=['GET', 'POST'])
def get_infoproyectos():
    return render_template('infoproyectos.html')