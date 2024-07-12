from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistavideos = Blueprint('idvideos', __name__, template_folder='templates')
 
@vistavideos.route('/videos', methods=['GET', 'POST'])
def vista_videos():
    return render_template('videos.html')