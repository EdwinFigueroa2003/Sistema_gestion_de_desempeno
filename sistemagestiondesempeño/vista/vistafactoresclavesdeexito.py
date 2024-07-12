from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistafactoresclavesdeexito = Blueprint('idfactoresclavesdeexito', __name__, template_folder='templates')
 
@vistafactoresclavesdeexito.route('/factoresclavesdeexito', methods=['GET', 'POST'])
def vista_factores_claves_de_exito():
    return render_template('factoresclavesdeexito.html')