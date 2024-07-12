from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistareportesanalisisorganizacional = Blueprint('idreportesanalisisorganizacional', __name__, template_folder='templates')
 
@vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET', 'POST'])
def vista_reportes_analisis_organizacional():
    return render_template('reportesanalisisorganizacional.html')