from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistareportes = Blueprint('idreportes', __name__, template_folder='templates')
 
@vistareportes.route('/reportes', methods=['GET', 'POST'])
def vista_reportes():
    return render_template('reportes.html')