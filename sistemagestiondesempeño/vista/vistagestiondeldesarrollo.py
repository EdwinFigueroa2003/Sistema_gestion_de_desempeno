from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL
 
# Crear un Blueprint
vistagestiondeldesarrollo = Blueprint('idgestiondeldesarrollo', __name__, template_folder='templates')
 
@vistagestiondeldesarrollo.route('/gestiondeldesarrollo', methods=['GET', 'POST'])
def vista_gestion_del_desarrollo():
    return render_template('gestiondeldesarrollo.html')