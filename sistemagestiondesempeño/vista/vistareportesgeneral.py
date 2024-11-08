import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistareportesgeneral = Blueprint('idreportesgeneral', __name__, template_folder='templates')
 
@vistareportesgeneral.route('/reportesgeneral', methods=['GET', 'POST'])
@login_required
def vista_reportes_general():
     
    return render_template('reportesgeneral.html')