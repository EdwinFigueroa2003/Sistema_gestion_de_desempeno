from flask import Blueprint, render_template
import requests
from configBd import API_URL
 
# Crear un nuevo Blueprint para los microproyectos asociados a un proyecto
vistainfoproyectos = Blueprint('idinfoproyectos', __name__, template_folder='templates')
 
@vistainfoproyectos.route('/proyecto/<int:id_proyecto>/microproyectos', methods=['GET'])
def get_infoproyectos(id_proyecto):
    try:
        # Realizar la solicitud a la API para obtener los microproyectos asociados a este proyecto
        api_url = f'{API_URL}/micro_proyecto?id_proyecto={id_proyecto}'
        print(f"Haciendo solicitud a la API: {api_url}")  # Depuración: Verificar la URL
        response = requests.get(api_url, timeout=10)
 
        if response.status_code == 200:
            microproyectos = response.json()  # Obtener microproyectos en formato JSON
            print(f"Microproyectos obtenidos: {microproyectos}")  # Depuración: Verificar respuesta
        else:
            print(f"Error en la solicitud: Código {response.status_code}")
            microproyectos = []  # Si la solicitud falla, usar una lista vacía
    except Exception as e:
        print(f"Error al obtener los microproyectos: {e}")
        microproyectos = []  # En caso de error, usar una lista vacía
 
    # Renderizar la plantilla HTML con los microproyectos
    return render_template('infoproyectos.html', microproyectos=microproyectos)