from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistainforme = Blueprint('idinforme', __name__, template_folder='templates')
 
@vistainforme.route('/informe', methods=['GET', 'POST'])
def vista_informe():
    return render_template('informe.html')