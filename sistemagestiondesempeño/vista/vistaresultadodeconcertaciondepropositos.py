from flask import Blueprint, request, render_template
import requests
 
vistaresultadosconcertaciondepropositos = Blueprint('idresultadosconcertaciondepropositos', __name__, template_folder='templates')
 
@vistaresultadosconcertaciondepropositos.route('/resultadosconcertaciondepropositos', methods=['GET'])
def vista_resultadosconcertaciondepropositos():
    # Obtener el parámetro de categoría desde la URL
    categoria = request.args.get('categoria', None)
    try:
        # Usar la URL correcta con el formato especificado
        if categoria:
            response = requests.get(f'http://127.0.0.1:5184/api/sgd/proposito/id_categoria/{categoria}')
        else:
            response = requests.get(f'http://127.0.0.1:5184/api/sgd/proposito')
 
        response.raise_for_status()  # Lanza una excepción si hay un error
        propositos = response.json()  # Parsear la respuesta JSON
    except requests.RequestException as e:
        print(f"Error al obtener los datos de la API: {e}")
        propositos = []
 
    # Renderizar la plantilla y pasar los propósitos obtenidos
    return render_template('resultadosconcertaciondepropositos.html', propositos=propositos)