from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from configBd import API_URL
 
# Crear un Blueprint
vistadashboard = Blueprint('iddashboard', __name__, template_folder='templates')
 
@vistadashboard.route('/dashboard', methods=['GET', 'POST'])
def vista_dashboard():
    return render_template('dashboard.html')