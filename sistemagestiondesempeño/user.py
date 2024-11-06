# main.py
from flask import Flask, render_template, request, url_for, redirect, session, flash, send_file
import os, io, xlsxwriter, requests, datetime, wraps
from matplotlib.figure import Figure
from PIL import Image
from configBd import API_URL
from flask_login import LoginManager, UserMixin
from main import app


# Configurar el gestor de inicio de sesión
login_manager = LoginManager()
login_manager.init_app(app)

#Inicio de rutas seguras

class User(UserMixin):
    def __init__(self, id_usuario, email):
        self.id = id_usuario  # Esto es necesario para que Flask-Login pueda identificar al usuario
        self.email = email

    def get_id(self):
        return str(self.id)

def get_user_by_id(id_usuario):
    try:
        response = requests.get(f"{API_URL}/usuario/{id_usuario}")  # Cambia la ruta si es necesario
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

@login_manager.user_loader
def load_user(id_usuario):
    # Obtener los datos del usuario a partir del ID
    user_data = get_user_by_id(id_usuario)
    if user_data:
        # Suponiendo que `User` es una clase que representa al usuario
        return User(user_data['id_usuario'], user_data['email'])  # Ajusta campos según los que tienes en `user_data`
    return None

#Fin de rutas seguras