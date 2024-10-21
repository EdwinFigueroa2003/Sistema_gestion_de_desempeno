from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
from configBd import API_URL
 
vistaresultadosconcertaciondepropositos = Blueprint('idresultadosconcertaciondepropositos', __name__, template_folder='templates')
 
@vistaresultadosconcertaciondepropositos.route('/resultadosconcertaciondepropositos', methods=['GET'])
def vista_resultadosconcertaciondepropositos():
    # Obtener el parámetro de categoría desde la URL
    categoria = request.args.get('categoria', None)
    try:
        # Usar la URL correcta con el formato especificado
        if categoria:
            response = requests.get(f'{API_URL}/proposito/id_categoria/{categoria}')
        else:
            response = requests.get(f'{API_URL}/proposito')
 
        response.raise_for_status()  # Lanza una excepción si hay un error
        propositos = response.json()  # Parsear la respuesta JSON
    except requests.RequestException as e:
        print(f"Error al obtener los datos de la API: {e}")
        propositos = []
 
    # Renderizar la plantilla y pasar los propósitos obtenidos
    return render_template('resultadosconcertaciondepropositos.html', propositos=propositos)