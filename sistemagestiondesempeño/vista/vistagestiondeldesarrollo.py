from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistagestiondeldesarrollo = Blueprint('idgestiondeldesarrollo', __name__, template_folder='templates')
 
@vistagestiondeldesarrollo.route('/gestiondeldesarrollo', methods=['GET', 'POST'])
def vista_gestion_del_desarrollo():
    return render_template('gestiondeldesarrollo.html')