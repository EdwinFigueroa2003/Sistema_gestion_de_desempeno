from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistaconcertaciondepropositos = Blueprint('idconcertaciondepropositos', __name__, template_folder='templates')
 
@vistaconcertaciondepropositos.route('/concertaciondepropositos', methods=['GET', 'POST'])
def vista_concertacion_de_propositos():
    

    #Fin de lo nuevo
    return render_template('concertaciondepropositos.html')