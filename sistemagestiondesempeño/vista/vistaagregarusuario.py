from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from configBd import API_URL
import requests

# Crear un Blueprint
vistaagregarusuario = Blueprint('idagregarusuario', __name__, template_folder='templates')

@vistaagregarusuario.route('/agregarusuario', methods=['GET', 'POST'])
@login_required # Hace que si no está autenticado, saque error.
def vista_agregar_usuario():

    print("Debug: Atributos de current_user:", vars(current_user))
    # Obtener el ID del usuario autenticado usando current_user
    id_usuario = getattr(current_user, 'id_usuario', None)
    print(f"Debug: ID Usuario desde current_user: {id_usuario}")

    if id_usuario:
        try:
            print("Debug: Iniciando solicitud de datos del usuario autenticado a la API.")
            response = requests.get(f"{API_URL}/usuarios_autenticados/id_usuario/{id_usuario}")
            print(f"Debug: Respuesta de la API para datos del usuario: {response.status_code}")
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                usuario_data = response.json()
                print(f"Debug: Datos del usuario obtenidos de la API: {usuario_data}")

                # Seleccionar el último registro en caso de múltiples autenticaciones
                usuario_actual = usuario_data[-1] if usuario_data else None
                if usuario_actual:
                    print("Debug: Último registro del usuario actual:", usuario_actual)
                    print("Debug: Renderizando plantilla 'agregarusuario.html' con datos del usuario.")
                    return render_template('agregarusuario.html', usuario=usuario_actual)
                else:
                    print("Debug: No se encontraron registros válidos en la respuesta de la API.")
                    flash("No se encontraron registros del usuario en la base de datos.", "error")
            else:
                print(f"Debug: Error en la respuesta de la API. Código de estado: {response.status_code}")
                flash(f"Error al obtener los datos del usuario: {response.status_code}", "error")
        except requests.RequestException as e:
            print(f"Debug: Excepción al realizar la solicitud a la API: {e}")
            flash("Error al conectar con el servidor de autenticación.", "error")
    else:
        print("Debug: ID de usuario no disponible en current_user.")
        flash("Usuario no autenticado o sesión no válida.", "error")

    print("Debug: Renderizando plantilla 'agregarusuario.html' con mensaje de error.")
    return render_template('agregarusuario.html', mensaje="No se pudo obtener la información del usuario")
