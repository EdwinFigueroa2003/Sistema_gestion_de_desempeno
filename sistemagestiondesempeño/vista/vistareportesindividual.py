from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistareportesindividual = Blueprint('idreportesindividual', __name__, template_folder='templates')
 
@vistareportesindividual.route('/reportesindividual', methods=['GET', 'POST'])
def vista_reportes_individual():

    #Inicio de lo nuevo
    """mensaje = ""
    objControlEntidad = ControlEntidad('reportes')  # Reemplazar 'nombre_controlador' con el nombre del controlador adecuado

    if request.method == 'GET':
        # Obtener todas las entidades desde la base de datos
        arregloEntidades = objControlEntidad.listar()

        # Consulta SQL para obtener los datos
        consultasql_calificacion = "SELECT * FROM nombre_calificacion;"  # Reemplazar 'nombre_tabla' con el nombre de la tabla
        objEntidad_consulta_calificacion = objControlEntidad.consultar(consulta=consultasql_calificacion)

        # Convertir los resultados en listas de diccionarios para enviarlos como JSON
        response = {
            'arregloCalificacion': [entidad.to_dict() for entidad in arregloEntidades],  # Suponiendo que Entidad tiene un método to_dict()
            'calificacion': [dato.to_dict() for dato in objEntidad_consulta_calificacion]  # Ajustar 'dato' al nombre del objeto
        }

        # Enviar la respuesta en formato JSON
        return jsonify(response)
    
    if request.method == 'POST':
        data = request.json
        
        # Leer los datos del JSON
        boton = data.get('boton', '')
        id_calif = data.get('id_calif', '')
        fk_respuesta_calif = data.get('fk_respuesta_calif', '')  # Reemplazar 'parametro1' con el nombre del parámetro
        fk_usuario_calif = data.get('fk_usuario_calif', '')  # Reemplazar 'parametro2' con el nombre del parámetro
        fk_evaluacion_calif = data.get('fk_evaluacion_calif', '')
        fk_cargo_calif = data.get('fk_cargo_calif', '')
        fk_cuestionario_calif = data.get('fk_cuestionario_calif', '')
        # Agregar más parámetros según sea necesario

                # Crear un diccionario con los datos de la entidad
        datosEntidad = {
            'id_calif': id_calif,
            'fk_respuesta_calif': fk_respuesta_calif,
            'fk_usuario_calif' :fk_usuario_calif,
            'fk_evaluacion_calif': fk_evaluacion_calif,
            'fk_cargo_calif': fk_cargo_calif,
            'fk_cuestionario_calif':fk_cuestionario_calif
            # Agregar más parámetros según sea necesario
            }
        objEntidad = Entidad(datosEntidad)

        if boton == 'Guardar':
            objControlEntidad.guardar(objEntidad)
            return jsonify({'success': True, 'message': 'Datos guardados exitosamente'})

        elif boton == 'Consultar':
            objEntidad = objControlEntidad.buscarPorId('id_calif', id_calif)  # Reemplazar 'parametro1' con el nombre del parámetro clave
            if objEntidad:
                return jsonify({'success': True, 'datos': objEntidad.to_dict()})
            else:
                return jsonify({'success': False, 'message': 'Datos no encontrados.'})
            
        elif boton == 'Modificar':
            objControlEntidad.modificar('id_calif', id_calif, objEntidad)  # Reemplazar 'parametro1' con el nombre del parámetro clave
            return jsonify({'success': True, 'message': 'Datos modificados exitosamente'})
        
        elif boton == 'Borrar':
            objControlEntidad.borrar('id_calif', id_calif)  # Reemplazar 'parametro1' con el nombre del parámetro clave
            return jsonify({'success': True, 'message': 'Datos borrados exitosamente'})

        else:
            return jsonify({'success': False, 'message': 'Acción no reconocida'})

    return jsonify({'success': False, 'message': 'Método no soportado'})
    """
    #Fin de lo nuevo

    return render_template('reportesindividual.html')