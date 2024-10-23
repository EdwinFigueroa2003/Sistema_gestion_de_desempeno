import random
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
from configBd import API_URL

# Crear un Blueprint
vistainforme = Blueprint('idinforme', __name__, template_folder='templates')


@vistainforme.route('/informe/<string:email>', methods=['GET'])
def vista_informe(email):
    usuario = None  # Inicializa usuario

    try:
        response = requests.get(f'{API_URL}/usuario/email/{email}', timeout=10)

        if response.status_code == 200:
            usuario = response.json()
            print("Datos del usuario:", usuario)  # Debug: muestra los datos del usuario

            # Maneja el caso donde usuario es una lista
            if isinstance(usuario, list) and len(usuario) > 0:
                usuario = usuario[0]  # Accede al primer elemento de la lista

            # Verifica si usuario es un diccionario después de potencialmente acceder al primer elemento
            if isinstance(usuario, dict):
                print("Claves en el diccionario usuario:", usuario.keys())  # Debug: claves
                # Guarda fk_nivel_de_contribucion en la sesión
                session['fk_nivel_de_contribucion'] = usuario.get('fk_nivel_de_contribucion')
                print("fk_nivel_de_contribucion guardado en la sesión:", session['fk_nivel_de_contribucion'])  # Debug: muestra el valor guardado
        else:
            usuario = None
            print(f"Error en la solicitud: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Excepción en la solicitud: {e}")

    return render_template('informe.html', usuario=usuario)


#No filtra pero muestra los datos en el rectangulo de la izquierda
""" @vistainforme.route('/informe/<string:email>', methods=['GET'])
def vista_informe(email):
    usuario = None  # Inicializa usuario

    try:
        response = requests.get(f'{API_URL}/usuario/email/{email}', timeout=10)

        if response.status_code == 200:
            usuario = response.json()
            print("Datos del usuario:", usuario)  # Debug: muestra los datos del usuario
            print("Datos del usuario antes de renderizar:", usuario)
            if isinstance(usuario, dict):
                print("Claves en el diccionario usuario:", usuario.keys())  # Debug: claves
        else:
            usuario = None
            print(f"Error en la solicitud: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Excepción en la solicitud: {e}")

    return render_template('informe.html', usuario=usuario) """

#No filtra pero muestra los datos en el rectangulo de la izquierda
""" @vistainforme.route('/informe/<string:email>', methods=['GET'])
def vista_informe(email):
    usuario = None  # Inicializa usuario

    try:
        response = requests.get(f'{API_URL}/usuario/email/{email}', timeout=10)

        if response.status_code == 200:
            usuario = response.json()
            print("Datos del usuario:", usuario)  # Debug: muestra los datos del usuario
            if isinstance(usuario, list) and len(usuario) > 0:
                usuario = usuario[0]  # Accede al primer elemento de la lista
                print("Claves en el diccionario usuario:", usuario.keys())  # Debug: claves
                # Guarda fk_nivel_de_contribucion en la sesión
                session['fk_nivel_de_contribucion'] = usuario.get('fk_nivel_de_contribucion')
                print("fk_nivel_de_contribucion guardado en la sesión:", session['fk_nivel_de_contribucion'])  # Debug: muestra el valor guardado
        else:
            usuario = None
            print(f"Error en la solicitud: {response.status_code}")
        #print("Datos de la sesión:", session)  # Debug: muestra los datos de la sesión

    except requests.exceptions.RequestException as e:
        print(f"Excepción en la solicitud: {e}")

    return render_template('informe.html', usuario=usuario) """