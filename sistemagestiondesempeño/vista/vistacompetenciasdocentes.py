from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistacompetenciasdocentes = Blueprint('idcompetenciasdocentes', __name__, template_folder='templates')
 
@vistacompetenciasdocentes.route('/competenciasdocentes', methods=['GET', 'POST'])
def vista_competencias_docentes():
    return render_template('competenciasdocentes.html')