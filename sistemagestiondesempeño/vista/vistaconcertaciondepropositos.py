import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistaconcertaciondepropositos = Blueprint('idconcertaciondepropositos', __name__, template_folder='templates')
 
@vistaconcertaciondepropositos.route('/concertaciondepropositos', methods=['GET', 'POST'])
@login_required
def vista_concertacion_de_propositos():
    

    #Fin de lo nuevo
    return render_template('concertaciondepropositos.html')