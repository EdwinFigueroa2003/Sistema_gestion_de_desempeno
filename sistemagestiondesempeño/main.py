# main.py
from pprint import pprint
from flask import Flask, render_template, request, url_for, redirect, session, jsonify, flash, send_file
import markupsafe, uuid, psycopg2, os, io, xlsxwriter, openpyxl, pandas, requests
from Entidad import Entidad
from werkzeug.utils import secure_filename
from datetime import datetime
from control.ControlEntidad import ControlEntidad


from menu import menu
from vista.vistaequipo import vistaequipo
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
""" from vista.vistacompetenciastransversales import vistacompetenciastransversales """
""" from vista.vistaresultadoscompetenciastransversales import vistaresultadoscompetenciastransversales """
""" from vista.vistaresultadoscompetenciasdocentes import vistaresultadoscompetenciasdocentes"""
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

API_URL = 'http://190.217.58.246:5184/api/sgd'


app.register_blueprint(menu)
app.register_blueprint(vistaequipo)
app.register_blueprint(vistaanalisisorganizacional)
app.register_blueprint(vistaconcertaciondepropositos)
app.register_blueprint(vistafactoresclavesdeexito)
app.register_blueprint(vistaconcertaciondedisponibilidad)
app.register_blueprint(vistacompetenciasdocentes)
""" app.register_blueprint(vistacompetenciastransversales) """
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
""" app.register_blueprint(vistaresultadoscompetenciastransversales) """
""" app.register_blueprint(vistaresultadoscompetenciasdocentes) """
app.register_blueprint(vistadashboard)
app.register_blueprint(vistareportesindividual)
app.register_blueprint(vistareportesgeneral)
app.register_blueprint(vistavideos)
app.register_blueprint(vistacursos)
app.register_blueprint(vistapodcast)
app.register_blueprint(vistaidentificaciondelideres)
 
# Establecer la ruta base si es necesario, por defecto es '/'
#breakpoint();

API_URL = 'http://190.217.58.246:5184/api/sgd'

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

@app.route('/competenciastransversales', methods=['GET', 'POST'])
def vista_competenciastransversales():
    id_apartado = 1  # Cambia este valor si fuera necesario
    user_id = 1  # Cambia esto según sea necesario

    if request.method == 'POST':
        # Manejar los datos del formulario y la navegación entre preguntas
        current_index = int(request.form.get('current_index', 0))
        respuestas = session.get('respuestas', {})

        # Guardar la respuesta seleccionada para la pregunta actual
        if 'respuesta_seleccionada' in request.form:
            pregunta_id = request.form.get('pregunta_id')
            respuestas[pregunta_id] = request.form.get('respuesta_seleccionada')
            session['respuestas'] = respuestas

        if 'next' in request.form:
            current_index += 1
        elif 'prev' in request.form:
            current_index -= 1

        # Obtener la lista de preguntas
        try:
            response_preguntas = requests.get(f'{API_URL}/pregunta/id_apartado/{id_apartado}', timeout=10)
            response_preguntas.raise_for_status()
            preguntas = response_preguntas.json()

            # Asegúrate de que la pregunta actual esté disponible
            if current_index < 0:
                current_index = 0
            if current_index >= len(preguntas):
                return redirect(url_for('finalizo'))

            pregunta_actual = preguntas[current_index]
            id_pregunta = pregunta_actual['id_pregunta']
            response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
            response_respuestas.raise_for_status()
            pregunta_actual['respuestas'] = response_respuestas.json()

            return render_template('competenciastransversales.html', pregunta=pregunta_actual, preguntas=preguntas,
                                   current_index=current_index, total_preguntas=len(preguntas))
        except requests.RequestException as e:
            print(f"Error al obtener datos: {e}")
            return render_template('competenciastransversales.html', pregunta=None, preguntas=[])

    # Inicializa el índice de la pregunta actual en GET
    current_index = 0
    try:
        response_preguntas = requests.get(f'{API_URL}/pregunta/id_apartado/{id_apartado}', timeout=10)
        response_preguntas.raise_for_status()
        preguntas = response_preguntas.json()

        if preguntas:
            pregunta_actual = preguntas[current_index]
            id_pregunta = pregunta_actual['id_pregunta']
            response_respuestas = requests.get(f'{API_URL}/respuesta/id_pregunta/{id_pregunta}', timeout=10)
            response_respuestas.raise_for_status()
            pregunta_actual['respuestas'] = response_respuestas.json()
            
            return render_template('competenciastransversales.html', pregunta=pregunta_actual, preguntas=preguntas,
                                   current_index=current_index, total_preguntas=len(preguntas))
    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return render_template('competenciastransversales.html', pregunta=None, preguntas=[])


@app.route('/resultadoscompetenciastransversales', methods=['GET'])
def resultadoscompetenciastransversales():
    respuestas = session.get('respuestas', {})
    
    preguntas_respuestas = []
    for id_pregunta, id_respuesta in respuestas.items():
        try:
            # Verifica que el endpoint para obtener preguntas por ID sea correcto
            response_pregunta = requests.get(f'{API_URL}/pregunta/id_pregunta/{id_pregunta}', timeout=10)
            response_pregunta.raise_for_status()
            pregunta = response_pregunta.json()

            # Imprimir la respuesta de la API para depuración
            print(f"Respuesta de pregunta: {pregunta}")

            # Si es una lista, accede al primer elemento
            if isinstance(pregunta, list) and len(pregunta) > 0:
                pregunta = pregunta[0]
            
            # Verifica que el endpoint para obtener respuestas por ID sea correcto
            response_respuesta = requests.get(f'{API_URL}/respuesta/id_respuesta/{id_respuesta}', timeout=10)
            response_respuesta.raise_for_status()
            respuesta = response_respuesta.json()

            # Imprimir la respuesta de la API para depuración
            print(f"Respuesta de respuesta: {respuesta}")

            # Si es una lista, accede al primer elemento
            if isinstance(respuesta, list) and len(respuesta) > 0:
                respuesta = respuesta[0]

            preguntas_respuestas.append({
                'texto_pregunta': pregunta.get('texto_pregunta', 'Pregunta no disponible'),
                'texto_respuesta': respuesta.get('texto_respuesta', 'Respuesta no disponible'),
                'valor_respuesta': respuesta.get('valor_respuesta', 'valor no disponible')
            })

        except requests.RequestException as e:
            print(f"Error al obtener datos: {e}")

    return render_template('resultadoscompetenciastransversales.html', respuestas=preguntas_respuestas)

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

@app.route('/api/sgd/usuario_respuesta', methods=['POST'])
def agregar_usuario_respuesta():
    try:
        data = request.json
        id_usuario = data.get('id_usuario')
        id_pregunta = data.get('id_pregunta')
        id_respuesta = data.get('id_respuesta')
        fecha_respuesta = data.get('fecha_respuesta')

        # Verifica que todos los datos estén presentes
        if not (id_usuario and id_pregunta and id_respuesta and fecha_respuesta):
            return jsonify({'error': 'Datos incompletos'}), 400

        # Aquí podrías agregar lógica para insertar los datos en la base de datos

        return jsonify({'message': 'Respuesta guardada correctamente'}), 200
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/finalizo', methods=['GET'])
def finalizo():
    usuario_id = request.args.get('usuario_id')  # Obtener el usuario_id de la consulta
    return render_template('finalizo.html', usuario_id=usuario_id)


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