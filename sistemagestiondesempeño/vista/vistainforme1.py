from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistainforme1 = Blueprint('idinforme1', __name__, template_folder='templates')
 
@vistainforme1.route('/informe1', methods=['GET', 'POST'])
def vista_informe_1():
    return render_template('informe1.html')