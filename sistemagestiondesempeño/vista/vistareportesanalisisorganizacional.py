from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistareportesanalisisorganizacional = Blueprint('idreportesanalisisorganizacional', __name__, template_folder='templates')

# Ruta para mostrar los resultados al finalizar el cuestionario
@vistareportesanalisisorganizacional.route('/reportesanalisisorganizacional', methods=['GET', 'POST'])
def vista_reportes_analisis_organizacional():
    
    return render_template('reportesanalisisorganizacional.html')

# ... existing code ...