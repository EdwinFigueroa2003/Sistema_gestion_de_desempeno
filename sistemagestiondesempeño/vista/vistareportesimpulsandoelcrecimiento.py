from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistareportesimpulsandoelcrecimiento = Blueprint('idreportesimpulsandoelcrecimiento', __name__, template_folder='templates')
 
@vistareportesimpulsandoelcrecimiento.route('/reportesimpulsandoelcrecimiento', methods=['GET', 'POST'])
def vista_reportes_impulsando_el_crecimiento():
    return render_template('reportesimpulsandoelcrecimiento.html')