import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime
 
# Crear un Blueprint
vistagestiondeldesempeno= Blueprint('idgestiondeldesempeno', __name__, template_folder='templates')
 
@vistagestiondeldesempeno.route('/gestiondeldesempeno', methods=['GET', 'POST'])
@login_required
def vista_gestion_del_desempeno():
    return render_template('gestiondeldesempeno.html')