from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
from Entidad import Entidad
import requests
from control.ControlEntidad import ControlEntidad
from configBd import API_URL
 
# Crear un Blueprint
vistaresultadosconcertaciondepropositos = Blueprint('idresultadosconcertaciondepropositos', __name__, template_folder='templates')
 
@vistaresultadosconcertaciondepropositos.route('/resultadosconcertaciondepropositos', methods=['GET', 'POST'])
def vista_resultadosconcertaciondepropositos():
    

    return render_template('resultadosconcertaciondepropositos.html')