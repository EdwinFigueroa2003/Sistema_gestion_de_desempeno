from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaresultados = Blueprint('idresultados', __name__, template_folder='templates')
 
@vistaresultados.route('/resultados', methods=['GET', 'POST'])
def vista_resultados():
    return render_template('resultados.html')