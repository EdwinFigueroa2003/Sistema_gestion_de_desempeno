from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaanalisisorganizacional = Blueprint('idanalisisorganizacional', __name__, template_folder='templates')
 
@vistaanalisisorganizacional.route('/analisisorganizacional', methods=['GET', 'POST'])
def vista_analisis_organizacional():
    return render_template('analisisorganizacional.html')