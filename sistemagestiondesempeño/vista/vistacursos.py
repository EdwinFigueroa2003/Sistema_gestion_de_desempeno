from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistacursos = Blueprint('idcursos', __name__, template_folder='templates')
 
@vistacursos.route('/cursos', methods=['GET', 'POST'])
def vista_cursos():
    return render_template('cursos.html')