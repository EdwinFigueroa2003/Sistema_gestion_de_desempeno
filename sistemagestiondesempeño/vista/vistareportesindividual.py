from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from configBd import API_URL
 
# Crear un Blueprint
vistareportesindividual = Blueprint('idreportesindividual', __name__, template_folder='templates')
 
@vistareportesindividual.route('/reportesindividual', methods=['GET', 'POST'])
def vista_reportes_individual():

    return render_template('reportesindividual.html')