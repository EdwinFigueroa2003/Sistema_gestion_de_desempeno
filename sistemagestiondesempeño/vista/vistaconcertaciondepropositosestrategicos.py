from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaconcertaciondepropositosestrategicos = Blueprint('idconcertaciondepropositosestrategicos', __name__, template_folder='templates')
 
@vistaconcertaciondepropositosestrategicos.route('/concertaciondepropositosestrategicos', methods=['GET', 'POST'])
def vista_concertaciondepropositosestrategicos():
    return render_template('concertaciondepropositosestrategicos.html')

