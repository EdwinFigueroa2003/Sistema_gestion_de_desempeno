from flask import Blueprint, render_template, request
from configBd import API_URL
import requests

vistaverpodcast = Blueprint('idverpodcast', __name__, template_folder='templates')

""" @vistaverpodcast.route('/verpodcast/<int:serie_id>', methods=['GET'])
def vista_ver_podcast(serie_id):
    print(f"Request received for serie_id: {serie_id}")  # Añadido para depuración
    # Obtener información de la serie
    serie_response = requests.get(f"{API_URL}/series/{serie_id}")
    print(f"Serie response status: {serie_response.status_code}")  # Añadido para depuración
    
    serie = serie_response.json()

    # Obtener episodios de la serie
    episodios_response = requests.get(f"{API_URL}/podcasts?serie_id={serie_id}")
    print(f"Episodios response status: {episodios_response.status_code}")  # Añadido para depuración
    episodios = episodios_response.json() if episodios_response.status_code == 200 else []

    return render_template('verpodcast.html', serie=serie, episodios=episodios) """

@vistaverpodcast.route('/verpodcast/<int:serie_id>', methods=['GET'])
def vista_ver_podcast(serie_id):
    print(f"Request received for serie_id: {serie_id}")  # Añadido para depuración
    # Obtener información de la serie
    serie_response = requests.get(f"{API_URL}/series/{serie_id}")
    print(f"Serie response status: {serie_response.status_code}")  # Añadido para depuración
    serie = serie_response.json() if serie_response.status_code == 200 else None

    # Obtener episodios de la serie
    episodios_response = requests.get(f"{API_URL}/podcasts?serie_id={serie_id}")  # Asegúrate de que la API soporte este endpoint
    print(f"Episodios response status: {episodios_response.status_code}")  # Añadido para depuración
    episodios = episodios_response.json() if episodios_response.status_code == 200 else []

    return render_template('verpodcast.html', serie=serie, episodios=episodios)
