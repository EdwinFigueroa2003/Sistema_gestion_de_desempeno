from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
import requests
from configBd import API_URL

 
# Crear un Blueprint
vistafactoresclavesdeexito = Blueprint('idfactoresclavesdeexito', __name__, template_folder='templates')

@vistafactoresclavesdeexito.route('/factoresclavesdeexito', methods=['GET', 'POST'])
def get_factoresclavesdeexito():
    
    return render_template('factoresclavesdeexito.html')