# main.py
from pprint import pprint
from flask import Flask, render_template, request, url_for, redirect, session, jsonify
import markupsafe, uuid, psycopg2, os
import requests
from Entidad import Entidad
from werkzeug.utils import secure_filename
from control.ControlEntidad import ControlEntidad


 
from menu import menu
from vista.vistaequipo import vistaequipo
from vista.vistaagregarequipo import vistaagregarequipo
from vista.vistaconfiguracion import vistaconfiguracion
from vista.vistagestiondeldesarrollo import vistagestiondeldesarrollo
from vista.vistainforme import vistainforme
from vista.vistacompetenciastransversales import vistacompetenciastransversales
from vista.vistacompetenciasdocentes import vistacompetenciasdocentes
from vista.vistaconcertaciondepropositos import vistaconcertaciondepropositos
from vista.vistafactoresclavesdeexito import vistafactoresclavesdeexito
""" from vista.vistapresentacion import vistapresentacion """
from vista.vistagestiondeldesempeno import vistagestiondeldesempeno
from vista.vistaotrascontribuciones import vistaotrascontribuciones
from vista.vistaareportes import vistareportes
from vista.vistareportesanalisisorganizacional import vistareportesanalisisorganizacional
from vista.vistareportesimpulsandoelcrecimiento import vistareportesimpulsandoelcrecimiento
""" from vista.vistaanalisisorganizacional import vistaanalisisorganizacional """
from vista.vistaproyectos import vistaproyectos
from vista.vistaevaluaciondecompetencias import vistaevaluaciondecompetencias
from vista.vistaresultados import vistaresultados
from vista.vistadashboard import vistadashboard
from vista.vistareportesindividual import vistareportesindividual
from vista.vistareportesgeneral import vistareportesgeneral
from vista.vistavideos import vistavideos
from vista.vistacursos import vistacursos
from vista.vistapodcast import vistapodcast
from vista.vistaidentificaciondelideres import vistaidentificaciondelideres



app = Flask(__name__)

app.register_blueprint(menu)
app.register_blueprint(vistaequipo)
app.register_blueprint(vistaagregarequipo)
app.register_blueprint(vistaconfiguracion)
app.register_blueprint(vistagestiondeldesarrollo)
app.register_blueprint(vistainforme)
app.register_blueprint(vistacompetenciastransversales)
app.register_blueprint(vistacompetenciasdocentes)
app.register_blueprint(vistaconcertaciondepropositos)
app.register_blueprint(vistafactoresclavesdeexito)
""" app.register_blueprint(vistapresentacion) """
app.register_blueprint(vistagestiondeldesempeno)
app.register_blueprint(vistaotrascontribuciones)
app.register_blueprint(vistareportes)
app.register_blueprint(vistareportesanalisisorganizacional)
app.register_blueprint(vistareportesimpulsandoelcrecimiento)
""" app.register_blueprint(vistaanalisisorganizacional) """
app.register_blueprint(vistaproyectos)
app.register_blueprint(vistaevaluaciondecompetencias)
app.register_blueprint(vistaresultados)
app.register_blueprint(vistadashboard)
app.register_blueprint(vistareportesindividual)
app.register_blueprint(vistareportesgeneral)
app.register_blueprint(vistavideos)
app.register_blueprint(vistacursos)
app.register_blueprint(vistapodcast)
app.register_blueprint(vistaidentificaciondelideres)
 
# Establecer la ruta base si es necesario, por defecto es '/'
#breakpoint();

@app.route('/', methods = ['GET', 'POST'])
@app.route('/inicio', methods = ['GET', 'POST'])
def inicio():
    email=""
    contrasena=""
    bot=""
    if request.method == 'GET':
        pass
    
    if request.method == 'POST':
        email=markupsafe.escape(request.form['txtEmail'])
        contrasena=markupsafe.escape(request.form['txtContrasena'])
        bot=markupsafe.escape(request.form['btnLogin'])
        datosEntidad = {'email': email, 'contrasena': contrasena}
        
        if bot=='Login':
            validar=False
            objEntidad= Entidad(datosEntidad)
            objControlEntidad=ControlEntidad('usuario')
            validar=objControlEntidad.validarIngreso('email',email,'contrasena',contrasena)

            if validar:
                return render_template('/menu.html',ema=email)
            else:
                return render_template('/inicio.html', mensaje_error='Credenciales incorrectas')
        else:
            return render_template('/inicio.html')
    else:
        return render_template('/inicio.html')


@app.route('/cerrarSesion')
def cerrarSesion():
    #session.clear()
    return redirect('inicio')

#Prueba

@app.route('/data', methods = ['GET'])
def get_data():
    response = requests.get('http://190.217.58.246:5184/api/sgd/cargo')
    try:
        data = response.json()  # Intenta decodificar la respuesta como JSON
    except requests.exceptions.JSONDecodeError:
        return "Error: La respuesta no es un JSON válido.", 500
    # Aquí puedes pasar 'data' a la plantilla HTML que desees renderizar.
    return render_template('data.html', data=data)

#Prueba


@app.route('/analisisorganizacional', methods = ['GET'])
def get_dimensiones():
    response = requests.get('http://190.217.58.246:5184/api/sgd/dimension')
    try:
        data = response.json()  # Intenta decodificar la respuesta como JSON
    except requests.exceptions.JSONDecodeError:
        return "Error: La respuesta no es un JSON válido.", 500
    # Aquí puedes pasar 'data' a la plantilla HTML que desees renderizar.
    return render_template('analisisorganizacional.html', data=data)


@app.route('/presentacion', methods = ['GET'])
def get_presentacion():
    return render_template('presentacion.html')

@app.route('/presentacionGDD', methods = ['GET'])
def get_presentacionGDD():
    return render_template('presentacionGDD.html')

if __name__ == '__main__':
    # Corre la aplicación en el modo debug, lo que permitirá
    # la recarga automática del servidor cuando se detecten cambios en los archivos.
    app.run(debug=True)