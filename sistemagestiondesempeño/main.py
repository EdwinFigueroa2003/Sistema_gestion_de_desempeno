# main.py
from pprint import pprint
from flask import Flask, render_template, request, url_for, redirect, session, jsonify, flash, send_file
import markupsafe, uuid, psycopg2, os, io, xlsxwriter, openpyxl, pandas
from Entidad import Entidad
from werkzeug.utils import secure_filename
from control.ControlEntidad import ControlEntidad


from menu import menu
from vista.vistaequipo import vistaequipo
from vista.vistacompetenciastransversales import vistacompetenciastransversales
from vista.vistaagregarequipo import vistaagregarequipo
from vista.vistaconfiguracion import vistaconfiguracion
from vista.vistagestiondeldesarrollo import vistagestiondeldesarrollo
from vista.vistainforme import vistainforme
from vista.vistafactoresclavesdeexito import vistafactoresclavesdeexito
from vista.vistaconcertaciondepropositos import vistaconcertaciondepropositos
from vista.vistaconcertaciondepropositospersonales import vistaconcertaciondepropositospersonales
from vista.vistacompetenciasdocentes import vistacompetenciasdocentes
from vista.vistagestiondeldesempeno import vistagestiondeldesempeno
from vista.vistaotrascontribuciones import vistaotrascontribuciones
from vista.vistaareportes import vistareportes
from vista.vistareportesanalisisorganizacional import vistareportesanalisisorganizacional
from vista.vistareportesimpulsandoelcrecimiento import vistareportesimpulsandoelcrecimiento
from vista.vistaproyectos import vistaproyectos
from vista.vistainfoproyectos import vistainfoproyectos
from vista.vistaevaluaciondecompetencias import vistaevaluaciondecompetencias
from vista.vistaresultados import vistaresultados
from vista.vistadashboard import vistadashboard
from vista.vistareportesindividual import vistareportesindividual
from vista.vistareportesgeneral import vistareportesgeneral
from vista.vistavideos import vistavideos
from vista.vistaconcertaciondedisponibilidad import vistaconcertaciondedisponibilidad
from vista.vistaconcertaciondepropositosparalamejoradeprocesos import vistaconcertaciondepropositosparalamejoradeprocesos
from vista.vistacursos import vistacursos
from vista.vistapodcast import vistapodcast
from vista.vistaidentificaciondelideres import vistaidentificaciondelideres
from vista.vistaanalisisorganizacional import vistaanalisisorganizacional



app = Flask(__name__)
app.secret_key = os.urandom(24)


app.register_blueprint(menu)
app.register_blueprint(vistaequipo)
app.register_blueprint(vistaanalisisorganizacional)
app.register_blueprint(vistacompetenciastransversales)
app.register_blueprint(vistaconcertaciondepropositos)
app.register_blueprint(vistafactoresclavesdeexito)
app.register_blueprint(vistaconcertaciondedisponibilidad)
app.register_blueprint(vistacompetenciasdocentes)
app.register_blueprint(vistaconcertaciondepropositosparalamejoradeprocesos)
app.register_blueprint(vistaconcertaciondepropositospersonales)
app.register_blueprint(vistaagregarequipo)
app.register_blueprint(vistaconfiguracion)
app.register_blueprint(vistagestiondeldesarrollo)
app.register_blueprint(vistainforme)
app.register_blueprint(vistagestiondeldesempeno)
app.register_blueprint(vistaotrascontribuciones)
app.register_blueprint(vistareportes)
app.register_blueprint(vistareportesanalisisorganizacional)
app.register_blueprint(vistareportesimpulsandoelcrecimiento)
app.register_blueprint(vistaproyectos)
app.register_blueprint(vistainfoproyectos)
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
    return redirect('inicio.html')

@app.route('/resultadoscompetenciastransversales', methods = ['GET', 'POST'])
def get_resultadoscompetenciastransversales():
    respuestas = session.get('respuestas', [])  # Obtener las respuestas de la sesión
    return render_template('resultadoscompetenciastransversales.html', respuestas=respuestas)

@app.route('/download_excel')
def download_excel():
    # Obtener las respuestas reales almacenadas en la sesión
    respuestas = session.get('respuestas', [])
    
    # Crear un archivo Excel en memoria
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Definir estilos
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'bg_color': '#4AF852',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    cell_format = workbook.add_format({
        'font_size': 12,
        'bg_color': '#EAF2D3',
        'border': 1,
        'align': 'left',
        'valign': 'vcenter'
    })
    
    # Escribir el encabezado con formato
    worksheet.write('A1', 'Resultados', header_format)
    
    # Ajustar el ancho de las columnas
    worksheet.set_column('A:A', 40)  # Ajusta el ancho de la columna A

    # Escribir las respuestas en el archivo Excel
    for i, respuesta in enumerate(respuestas, start=1):
        worksheet.write(f'A{i+1}', respuesta, cell_format)
    
    workbook.close()
    output.seek(0)
    
    return send_file(output, download_name="Resultados.xlsx", as_attachment=True)

@app.route('/resultadoscompetenciasdocentes', methods = ['GET', 'POST'])
def get_resultadoscompetenciasdocentes():
    return render_template('resultadoscompetenciasdocentes.html')

@app.route('/resultadosconcertaciondepropositos', methods = ['GET', 'POST'])
def get_resultadosconcertaciondepropositos():
    return render_template('resultadosconcertaciondepropositos.html')

@app.route('/presentacionGDD', methods = ['GET'])
def get_presentacionGDD():
    return render_template('presentacionGDD.html')

if __name__ == '__main__':
    # Corre la aplicación en el modo debug, lo que permitirá
    # la recarga automática del servidor cuando se detecten cambios en los archivos.
    app.run(debug=True)