from flask import Blueprint, render_template
from configBd import API_URL
from pprint import pprint
from flask import request, redirect, url_for, session
import markupsafe
import requests

# Crear un Blueprint
vistalogin = Blueprint('idvistalogin', __name__, template_folder='templates')

@vistalogin.route('/login', methods=['GET', 'POST'])
def vista_login():
    email = ""
    contrasena = ""
    
    if request.method == 'POST':
        email = markupsafe.escape(request.form['txtEmail'])
        contrasena = markupsafe.escape(request.form['txtContrasena'])
        
        # Realizar la solicitud a la API para validar las credenciales
        response = requests.get(f"{API_URL}/usuario")
        
        if response.status_code == 200:
            usuarios = response.json()
            # Verificar si el usuario existe y las credenciales son correctas
            for usuario in usuarios:
                if usuario['email'] == email and usuario['contrasena'] == contrasena:
                    # Guardar información del usuario en la sesión
                    session['usuario'] = usuario
                    return render_template('/menu.html', ema=email)
            
            # Si las credenciales son incorrectas
            return render_template('/login.html', mensaje_error='Credenciales incorrectas')
        else:
            return render_template('/login.html', mensaje_error='Error al conectar con la API')
    
    return render_template('/login.html')

""" @vistalogin.route('/login', methods=['GET', 'POST'])
def vista_login():
    email = ""
    contrasena = ""
    bot = ""
    
    if request.method == 'GET':
        pass
    
    if request.method == 'POST':
        email = markupsafe.escape(request.form['txtEmail'])
        contrasena = markupsafe.escape(request.form['txtContrasena'])
        bot = markupsafe.escape(request.form['btnLogin'])
        datosEntidad = {'email': email, 'contrasena': contrasena}
        
        if bot == 'Login':
            validar = False
            objEntidad = Entidad(datosEntidad)
            objControlEntidad = ControlEntidad('usuario')
            validar = objControlEntidad.validarIngreso('email', email, 'contrasena', contrasena)

            if validar:
                return render_template('/menu.html', ema=email)
            else:
                # Cambiado de 'inicio.html' a 'login.html'
                return render_template('/login.html', mensaje_error='Credenciales incorrectas')
        else:
            # Cambiado de 'inicio.html' a 'login.html'
            return render_template('/login.html')
    else:
        # Cambiado de 'inicio.html' a 'login.html'
        return render_template('/login.html') """
