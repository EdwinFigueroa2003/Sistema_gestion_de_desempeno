from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad
 
# Crear un Blueprint
vistafactoresclavesdeexito = Blueprint('idfactoresclavesdeexito', __name__, template_folder='templates')
 
@vistafactoresclavesdeexito.route('/factoresclavesdeexito', methods=['GET', 'POST'])
def vista_factores_claves_de_exito():
        #Inicio de lo nuevo
    """ mensaje = ""
    objControlEntidad = ControlEntidad('competencia')  # Reemplazar 'nombre_controlador' con el nombre del controlador adecuado

    if request.method == 'GET':
        # Obtener todas las entidades desde la base de datos
        arregloEntidades = objControlEntidad.listar()

        # Consulta SQL para obtener los datos
        consultasql_competencias = "SELECT * FROM nombre_competencias;"  # Reemplazar 'nombre_tabla' con el nombre de la tabla
        objEntidad_consulta_competencias = objControlEntidad.consultar(consulta=consultasql_competencias)

        # Convertir los resultados en listas de diccionarios para enviarlos como JSON
        response = {
            'arregloCompetencias': [entidad.to_dict() for entidad in arregloEntidades],  # Suponiendo que Entidad tiene un método to_dict()
            'competencias': [dato.to_dict() for dato in objEntidad_consulta_competencias]  # Ajustar 'dato' al nombre del objeto
        }

        # Enviar la respuesta en formato JSON
        return jsonify(response)
    
    if request.method == 'POST':
        data = request.json
        
        # Leer los datos del JSON
        boton = data.get('boton', '')
        id_competencia = data.get('id_competencia', '')  # Reemplazar 'parametro1' con el nombre del parámetro
        nombre_comp = data.get('nombre_comp', '')  # Reemplazar 'parametro2' con el nombre del parámetro
        definicion_comp = data.get('definicion_comp', '')
        logo_comp = data.get('logo_comp', '')
        preg_eval_comp = data.get('preg_eval_comp', '')
        estado_comp = data.get('estado_comp', '')
        fk_nivel_contrib_comp = data.get('fk_nivel_contrib_comp', '')
        # Agregar más parámetros según sea necesario

                # Crear un diccionario con los datos de la entidad
        datosEntidad = {
            'id_competencia': id_competencia,
            'nombre_comp' :nombre_comp,
            'definicion_comp': definicion_comp,
            'logo_comp': logo_comp,
            'preg_eval_comp':preg_eval_comp,
            'estado_comp':estado_comp,
            'fk_nivel_contrib_comp':fk_nivel_contrib_comp,
            # Agregar más parámetros según sea necesario
            }
        objEntidad = Entidad(datosEntidad)

        if boton == 'Guardar':
            objControlEntidad.guardar(objEntidad)
            return jsonify({'success': True, 'message': 'Datos guardados exitosamente'})

        elif boton == 'Consultar':
            objEntidad = objControlEntidad.buscarPorId('id_competencia', id_competencia)  # Reemplazar 'parametro1' con el nombre del parámetro clave
            if objEntidad:
                return jsonify({'success': True, 'datos': objEntidad.to_dict()})
            else:
                return jsonify({'success': False, 'message': 'Datos no encontrados.'})
            
        elif boton == 'Modificar':
            objControlEntidad.modificar('id_competencia', id_competencia, objEntidad)  # Reemplazar 'parametro1' con el nombre del parámetro clave
            return jsonify({'success': True, 'message': 'Datos modificados exitosamente'})
        
        elif boton == 'Borrar':
            objControlEntidad.borrar('id_competencia', id_competencia)  # Reemplazar 'parametro1' con el nombre del parámetro clave
            return jsonify({'success': True, 'message': 'Datos borrados exitosamente'})

        else:
            return jsonify({'success': False, 'message': 'Acción no reconocida'})

    return jsonify({'success': False, 'message': 'Método no soportado'}) """

    #Fin de lo nuev
    return render_template('factoresclavesdeexito.html')