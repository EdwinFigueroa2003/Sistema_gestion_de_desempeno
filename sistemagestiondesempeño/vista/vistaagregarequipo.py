from flask import Blueprint, render_template, session
from flask_login import login_required
from configBd import API_URL

# Crear un Blueprint
vistaagregarequipo = Blueprint('idagregarequipo', __name__, template_folder='templates')
 
@vistaagregarequipo.route('/agregarequipo', methods=['GET', 'POST'])
#@login_required
def vista_agregar_equipo():
    return render_template('agregarequipo.html')

""" def vista_agregar_equipo():

    user_id = session.get('user_id')
    user_email = session.get('user_email')

    return render_template('agregarequipo.html',
                           user_email=user_email,
                           user_id=user_id) """

