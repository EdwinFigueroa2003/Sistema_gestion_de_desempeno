import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistadashboard = Blueprint('iddashboard', __name__, template_folder='templates')
 
@vistadashboard.route('/dashboard', methods=['GET', 'POST'])
@login_required
def vista_dashboard():
    return render_template('dashboard.html')