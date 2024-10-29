from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
from configBd import API_URL
 
vistaresultadosconcertaciondepropositos = Blueprint('idresultadosconcertaciondepropositos', __name__, template_folder='templates')
 
@vistaresultadosconcertaciondepropositos.route('/resultadosconcertaciondepropositos', methods=['GET'])
def vista_resultadosconcertaciondepropositos():
    # Obtener el id_usuario desde la sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return redirect(url_for('idvistalogin.vista_login'))  # Redirigir al login si no hay un usuario en sesión

    # Obtener el parámetro de categoría desde la URL
    categoria = request.args.get('categoria', None)
    try:
        # Construir la URL de la API con el filtro de id_usuario
        if categoria:
            response = requests.get(f'{API_URL}/proposito/id_categoria/{categoria}?id_usuario={id_usuario}')
        else:
            response = requests.get(f'{API_URL}/proposito?id_usuario={id_usuario}')
 
        response.raise_for_status()  # Lanza una excepción si hay un error
        propositos = response.json()  # Parsear la respuesta JSON
    except requests.RequestException as e:
        print(f"Error al obtener los datos de la API: {e}")
        propositos = []
 
    # Renderizar la plantilla y pasar los propósitos obtenidos
    return render_template('resultadosconcertaciondepropositos.html', propositos=propositos)