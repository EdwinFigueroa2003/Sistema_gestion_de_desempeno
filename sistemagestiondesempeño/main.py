# main.py
from pprint import pprint
from flask import Flask, render_template, request, url_for, redirect, session, jsonify, flash, send_file, send_file
import markupsafe, uuid, psycopg2, os, io, xlsxwriter, openpyxl, pandas, requests, base64 
from Entidad import Entidad
from matplotlib.figure import Figure
from werkzeug.utils import secure_filename

from PIL import Image
from control.ControlEntidad import ControlEntidad
from configBd import API_URL


from menu import menu
from vista.vistaequipo import vistaequipo
from vista.vistaagregarequipo import vistaagregarequipo
from vista.vistaconfiguracion import vistaconfiguracion
from vista.vistadetallemicroproyecto import vistadetallemicroproyecto
from vista.vistagestiondeldesarrollo import vistagestiondeldesarrollo
from vista.vistainforme import vistainforme
from vista.vistafactoresclavesdeexito import vistafactoresclavesdeexito
from vista.vistaconcertaciondepropositos import vistaconcertaciondepropositos
from vista.vistaresultadodeconcertaciondepropositos import vistaresultadosconcertaciondepropositos
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
from vista.vistacompetenciastransversales import vistacompetenciastransversales
from vista.vistaresultadoscompetenciastransversales import vistaresultadoscompetenciastransversales
from vista.vistaresultadoscompetenciasdocentes import vistaresultadoscompetenciasdocentes
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
app.register_blueprint(vistaconcertaciondepropositos)
app.register_blueprint(vistadetallemicroproyecto)
app.register_blueprint(vistafactoresclavesdeexito)
app.register_blueprint(vistaconcertaciondedisponibilidad)
app.register_blueprint(vistacompetenciasdocentes)
app.register_blueprint(vistacompetenciastransversales)
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
app.register_blueprint(vistaresultadoscompetenciastransversales)
app.register_blueprint(vistaresultadoscompetenciasdocentes)
app.register_blueprint(vistaresultadosconcertaciondepropositos)
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
    session.clear() # Limpiar la sesión
    return redirect('inicio.html')

@app.route('/download_excel')
def download_excel():
    tipo = request.args.get('tipo', 'datos')

    if tipo == 'grafica':
        # Generar la gráfica usando matplotlib
        fig = Figure()
        ax = fig.subplots()

        # Obtener las respuestas almacenadas en la sesión
        respuestas = session.get('respuestas', {})

        # Preparar los datos para la gráfica
        xValues = list(range(1, len(respuestas) + 1))
        yValues = [float(respuesta) for respuesta in respuestas.values()]

        # Graficar los datos
        ax.plot(xValues, yValues, marker='o', linestyle='-', color='b')
        ax.set_title('Valores de Respuestas')
        ax.set_xlabel('Índice')
        ax.set_ylabel('Valor')

        # Guardar la gráfica en un archivo de imagen en memoria
        output = io.BytesIO()
        fig.savefig(output, format='png')
        output.seek(0)

        # Devolver la imagen como una descarga
        return send_file(output, download_name="grafica.png", as_attachment=True, mimetype='image/png')

    else:
        # Código existente para descargar los datos en Excel
        respuestas = session.get('respuestas', {})

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
        worksheet.write('A1', 'Pregunta', header_format)
        worksheet.write('B1', 'Respuesta', header_format)
        worksheet.write('C1', 'Valor', header_format)

        # Ajustar el ancho de las columnas
        worksheet.set_column('A:A', 40)  # Ajusta el ancho de la columna A
        worksheet.set_column('B:B', 40)  # Ajusta el ancho de la columna B
        worksheet.set_column('C:C', 10)  # Ajusta el ancho de la columna C

        preguntas_respuestas = []

        # Iterar sobre el diccionario de respuestas almacenadas en sesión
        for id_pregunta, id_respuesta in respuestas.items():
            try:
                response_pregunta = requests.get(f'{API_URL}/pregunta/id_pregunta/{id_pregunta}', timeout=10)
                response_pregunta.raise_for_status()
                pregunta = response_pregunta.json()

                if isinstance(pregunta, list) and len(pregunta) > 0:
                    pregunta = pregunta[0]

                response_respuesta = requests.get(f'{API_URL}/respuesta/id_respuesta/{id_respuesta}', timeout=10)
                response_respuesta.raise_for_status()
                respuesta = response_respuesta.json()

                if isinstance(respuesta, list) and len(respuesta) > 0:
                    respuesta = respuesta[0]

                preguntas_respuestas.append({
                    'texto_pregunta': pregunta.get('texto_pregunta', 'Pregunta no disponible'),
                    'texto_respuesta': respuesta.get('texto_respuesta', 'Respuesta no disponible'),
                    'valor_respuesta': respuesta.get('valor_respuesta', 'Valor no disponible')
                })

            except requests.RequestException as e:
                print(f"Error al obtener datos: {e}")

        # Escribir los datos en el archivo Excel
        for i, respuesta in enumerate(preguntas_respuestas, start=1):
            worksheet.write(f'A{i+1}', respuesta['texto_pregunta'], cell_format)
            worksheet.write(f'B{i+1}', respuesta['texto_respuesta'], cell_format)
            worksheet.write(f'C{i+1}', respuesta['valor_respuesta'], cell_format)

        workbook.close()
        output.seek(0)

        return send_file(output, download_name="Resultados.xlsx", as_attachment=True)

@app.route('/finalizo', methods=['GET'])
def finalizo():
    usuario_id = request.args.get('usuario_id')  # Obtener el usuario_id de la consulta
    return render_template('finalizo.html', usuario_id=usuario_id)

@app.route('/presentacionGDD', methods = ['GET'])
def get_presentacionGDD():
    return render_template('presentacionGDD.html')


if __name__ == '__main__':
    # Corre la aplicación en el modo debug, lo que permitirá
    # la recarga automática del servidor cuando se detecten cambios en los archivos.
    app.run(debug=True)