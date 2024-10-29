from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import request, redirect, url_for, session
import markupsafe, requests, bcrypt

# Crear un Blueprint
vistalogin = Blueprint('idvistalogin', __name__, template_folder='templates')


@vistalogin.route('/login', methods=['GET', 'POST'])
def vista_login():
    if request.method == 'POST':
        email = markupsafe.escape(request.form['txtEmail'])
        contrasena = markupsafe.escape(request.form['txtContrasena']).encode('utf-8')
        
        # Realizar la solicitud a la API para obtener los usuarios
        response = requests.get(f"{API_URL}/usuario")
        
        if response.status_code == 200:
            usuarios = response.json()
            for usuario in usuarios:
                if usuario['email'] == email:
                    # Comparar la contraseña hasheada almacenada con la ingresada
                    hashed_contrasena = usuario['contrasena'].encode('utf-8')
                    if bcrypt.checkpw(contrasena, hashed_contrasena):
                        session['usuario'] = usuario
                        return render_template('/menu.html', ema=email)
            
            # Credenciales incorrectas
            return render_template('/login.html', mensaje_error='Credenciales incorrectas')
        else:
            return render_template('/login.html', mensaje_error='Error al conectar con la API')
    
    return render_template('/login.html')