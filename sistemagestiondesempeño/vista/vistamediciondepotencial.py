from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistamediciondepotencial = Blueprint('idmediciondepotencial', __name__, template_folder='templates')
 
@vistamediciondepotencial.route('/mediciondepotencial', methods=['GET', 'POST'])
def vista_medicion_de_potencial():
    return render_template('mediciondepotencial.html')