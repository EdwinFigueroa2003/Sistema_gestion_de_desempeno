from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistaconcertaciondepropositosparalamejoradeprocesos = Blueprint('idconcertaciondepropositosparalamejoradeprocesos', __name__, template_folder='templates')
 
@vistaconcertaciondepropositosparalamejoradeprocesos.route('/concertaciondepropositosparalamejoradeprocesos', methods=['GET', 'POST'])
def vista_concertaciondepropositosparalamejoradeprocesos():
    return render_template('concertaciondepropositosparalamejoradeprocesos.html')