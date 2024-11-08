import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistareportesindividual = Blueprint('idreportesindividual', __name__, template_folder='templates')
 
@vistareportesindividual.route('/reportesindividual', methods=['GET', 'POST'])
@login_required
def vista_reportes_individual():

    return render_template('reportesindividual.html')