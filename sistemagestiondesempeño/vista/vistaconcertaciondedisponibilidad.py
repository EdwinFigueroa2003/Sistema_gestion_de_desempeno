from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaconcertaciondedisponibilidad = Blueprint('idconcertaciondedisponibilidad', __name__, template_folder='templates')
 
@vistaconcertaciondedisponibilidad.route('/concertaciondedisponibilidad', methods=['GET', 'POST'])
def vista_concertaciondedisponibilidad():
    return render_template('concertaciondedisponibilidad.html')

