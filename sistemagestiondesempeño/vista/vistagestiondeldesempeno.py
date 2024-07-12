from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistagestiondeldesempeno= Blueprint('idgestiondeldesempeno', __name__, template_folder='templates')
 
@vistagestiondeldesempeno.route('/gestiondeldesempeno', methods=['GET', 'POST'])
def vista_gestion_del_desempeno():
    return render_template('gestiondeldesempeno.html')