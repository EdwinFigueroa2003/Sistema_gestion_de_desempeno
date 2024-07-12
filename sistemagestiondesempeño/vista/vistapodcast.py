from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistapodcast = Blueprint('idpodcast', __name__, template_folder='templates')
 
@vistapodcast.route('/podcast', methods=['GET', 'POST'])
def vista_podcast():
    return render_template('podcast.html')