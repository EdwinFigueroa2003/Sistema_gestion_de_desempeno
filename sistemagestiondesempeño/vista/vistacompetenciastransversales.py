from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistacompetenciastransversales = Blueprint('idcompetenciastransversales', __name__, template_folder='templates')
 
@vistacompetenciastransversales.route('/competenciastransversales', methods=['GET', 'POST'])
def vista_competencias_transversales():
    return render_template('competenciastransversales.html')