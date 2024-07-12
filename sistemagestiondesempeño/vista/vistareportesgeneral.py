from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistareportesgeneral = Blueprint('idreportesgeneral', __name__, template_folder='templates')
 
@vistareportesgeneral.route('/reportesgeneral', methods=['GET', 'POST'])
def vista_reportes_general():
    return render_template('reportesgeneral.html')