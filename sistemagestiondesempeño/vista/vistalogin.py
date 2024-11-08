from flask import Blueprint, render_template, request, session, flash
from configBd import API_URL
import markupsafe, requests, bcrypt
from flask_login import login_user, current_user
from pprint import pprint

# Crear un Blueprint
vistalogin = Blueprint('idvistalogin', __name__, template_folder='templates')

@vistalogin.route('/login', methods=['GET', 'POST'])
def vista_login():
    try:
        from main import User
        if request.method == 'POST':
            email = markupsafe.escape(request.form['txtEmail'])
            contrasena = markupsafe.escape(request.form['txtContrasena']).encode('utf-8')
            
            print("Debug: Iniciando proceso de autenticación.")
            print(f"Debug: Email ingresado: {email}")

            # Solicitud a la API para obtener los usuarios
            response = requests.get(f"{API_URL}/usuario")
            print("Debug: Llamada a la API de usuarios realizada.")
            
            if response.status_code == 200:
                usuarios = response.json()
                print("Debug: Usuarios recibidos de la API.")
                
                # Buscar el usuario en la lista de usuarios
                usuario = next((u for u in usuarios if u['email'] == email), None)
                print(f"Debug: Usuario encontrado en la API: {usuario}")

                if usuario and bcrypt.checkpw(contrasena, usuario['contrasena'].encode('utf-8')):
                    # Crear la instancia de User con id_usuario
                    user = User(
                        id_usuario=usuario['id_usuario'],
                        email=usuario['email'],
                        fk_rol_usu=usuario.get('fk_rol_usu'),
                        nombre=usuario.get('nombre')
                    )
                    login_user(user)  # Autenticar al usuario
                    session['user_id'] = user.id_usuario  # Asegúrate de que el ID de usuario se guarde en la sesión
                    print("Debug: Usuario autenticado con login_user.")
                    print("Debug: current_user después de login_user:", vars(current_user))

                    
                    # Guardar los datos del usuario en la sesión
                    session['usuario'] = {'id_usuario': usuario['id_usuario'], 'fk_rol_usu': usuario['fk_rol_usu']}
                    print(f"Debug: Datos del usuario almacenados en sesión: {session['usuario']}")

                    print("Debug: Información de current_user:")
                    pprint(vars(current_user))

                    # Hacer la sesión permanente
                    session.permanent = True
                    print("Debug: Sesión marcada como permanente.")

                    # Guardar el usuario autenticado en la base de datos a través de la API
                    post_data = {
                        'id_usuario': usuario['id_usuario'],
                        'email': usuario['email'],
                        'nombre': usuario.get('nombre', ''),
                        'rol_usu': usuario['fk_rol_usu'],
                        'user_repr': repr(user),
                        'contrasena': usuario['contrasena']
                    }
                    post_response = requests.post(f"{API_URL}/usuarios_autenticados", json=post_data)
                    print(f"Debug: Respuesta de la API al guardar usuario autenticado: {post_response.status_code}")

                    if post_response.status_code != 201:
                        flash("Error al guardar el usuario autenticado en la base de datos", "error")
                    
                    # Redirigir según el rol del usuario
                    print("Debug: Redirigiendo según el rol del usuario.")
                    if usuario['fk_rol_usu'] == 1:
                        return render_template('administrador.html')
                    elif usuario['fk_rol_usu'] == 2:
                        return render_template('menu.html')
                    elif usuario['fk_rol_usu'] == 3:
                        return render_template('colaboradorprueba.html')
                    elif usuario['fk_rol_usu'] == 4:
                        return render_template('estudianteprueba.html')
                else:
                    print("Debug: Usuario o contraseña incorrectos.")
                    return render_template('login.html', mensaje="Usuario o contraseña incorrectos")
            else:
                print("Debug: Error al conectar con la API.")
                return render_template('login.html', mensaje="Error al conectar con la API")
    except Exception as e:
        print(f"Error en login: {e}")
        return render_template('login.html', mensaje="Error interno")
    
    return render_template('login.html')
