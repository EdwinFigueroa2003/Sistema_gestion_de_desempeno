from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaconcertaciondepropositospersonales = Blueprint('idconcertaciondepropositospersonales', __name__, template_folder='templates')

@vistaconcertaciondepropositospersonales.route('/concertaciondepropositospersonales', methods = ['GET', 'POST'])
def vista_concertaciondepropositospersonales():
    return render_template('concertaciondepropositospersonales.html')