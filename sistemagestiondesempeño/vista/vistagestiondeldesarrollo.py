import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistagestiondeldesarrollo = Blueprint('idgestiondeldesarrollo', __name__, template_folder='templates')
 
@vistagestiondeldesarrollo.route('/gestiondeldesarrollo', methods=['GET', 'POST'])
@login_required
def vista_gestion_del_desarrollo():
    return render_template('gestiondeldesarrollo.html')