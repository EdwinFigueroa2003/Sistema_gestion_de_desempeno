from flask import Blueprint, render_template, request, session, redirect, url_for, flash, Flask
from configBd import API_URL
import markupsafe, requests, bcrypt
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Crear un Blueprint
vistalogin = Blueprint('idvistalogin', __name__, template_folder='templates')

@vistalogin.route('/login', methods=['GET', 'POST'])
def vista_login():
    try:
        from main import User
        if request.method == 'POST':
            email = markupsafe.escape(request.form['txtEmail'])
            contrasena = markupsafe.escape(request.form['txtContrasena']).encode('utf-8')
            
            # Solicitud a la API para obtener los usuarios
            response = requests.get(f"{API_URL}/usuario")
            
            if response.status_code == 200:
                usuarios = response.json()
                usuario = next((u for u in usuarios if u['email'] == email), None)
                
                if usuario and bcrypt.checkpw(contrasena, usuario['contrasena'].encode('utf-8')):
                    user = User(usuario['id_usuario'], usuario['email'])
                    login_user(user)  # Autenticar al usuario
                    
                    # Guardar los datos del usuario en la sesión
                    session['usuario'] = {'id_usuario': usuario['id_usuario'], 'fk_rol_usu': usuario['fk_rol_usu']}
                    
                    pprint(usuario)
                    pprint(usuario['fk_rol_usu'])
                    pprint(user)

                    # Redirigir según el rol
                    if usuario['fk_rol_usu'] == 1:  # Admin
                        return render_template('adminprueba.html')
                    elif usuario['fk_rol_usu'] == 2:  # Líder
                        return render_template('menu.html', ema=email)
                    elif usuario['fk_rol_usu'] == 3:  # Colaborador
                        return render_template('colaboradorprueba.html')
                    elif usuario['fk_rol_usu'] == 4:  # Estudiante
                        return render_template('estudianteprueba.html')
                else:
                    return render_template('login.html', mensaje="Usuario o contraseña incorrectos")
            else:
                return render_template('login.html', mensaje="Error al conectar con la API")
    except Exception as e:
        print(f"Error en login: {e}")
        return render_template('login.html', mensaje="Error interno")
    
    return render_template('login.html')
