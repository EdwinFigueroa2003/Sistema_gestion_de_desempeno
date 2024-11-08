import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session, json, jsonify
import requests
from configBd import API_URL
from flask_login import login_required
from datetime import datetime

 
# Crear un Blueprint
vistafactoresclavesdeexito = Blueprint('idfactoresclavesdeexito', __name__, template_folder='templates')

@vistafactoresclavesdeexito.route('/factoresclavesdeexito', methods=['GET', 'POST'])
@login_required
def get_factoresclavesdeexito():
    
    return render_template('factoresclavesdeexito.html')