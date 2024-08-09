from flask import Blueprint, jsonify, request, render_template
from Entidad import Entidad
from control.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistainforme = Blueprint('idinforme', __name__, template_folder='templates')

@vistainforme.route('/informe', methods=['GET', 'POST'])
def vista_informe():
    """ mensaje = ""
    objControlEntidad = ControlEntidad('usuario')

    if request.method == 'GET':
        # Obtener todas las entidades de usuarios desde la base de datos
        arregloEntidades = objControlEntidad.listar()

        # Consulta para obtener los usuarios
        consultasql_usuarios = "SELECT * FROM usuarios;"
        objEntidad_consulta_usuarios = objControlEntidad.consultar(consulta=consultasql_usuarios)

        # Convertir los resultados en listas de diccionarios para enviarlos como JSON
        response = {
            'arregloUsuario': [entidad.to_dict() for entidad in arregloEntidades],  # Suponiendo que Entidad tiene un método to_dict()
            'usuarios': [usuario.to_dict() for usuario in objEntidad_consulta_usuarios]
        }

        # Enviar la respuesta en formato JSON
        return jsonify(response)

    if request.method == 'POST':
        data = request.json
        
        # Leer los datos del JSON
        boton = data.get('boton', '')
        documento_usu = data.get('documento_usu', '')
        fk_rol_usu = data.get('fk_rol_usu', '')
        fk_cargo_usu = data.get('fk_cargo_usu', '')
        estado_usu = data.get('estado_usu', '')
        foto_usu = data.get('foto_usu', '')
        consecutivo_usu = data.get('consecutivo_usu', '')
        fk_costo_usu = data.get('fk_costo_usu', '')
        email = data.get('email', '')
        contrasena = data.get('contrasena', '')

        datosEntidad = {
            'documento_usu': documento_usu,
            'fk_rol_usu': fk_rol_usu,
            'fk_cargo_usu': fk_cargo_usu,
            'estado_usu': estado_usu,
            'foto_usu': foto_usu,
            'consecutivo_usu': consecutivo_usu,
            'fk_costo_usu': fk_costo_usu,
            'email': email,
            'contrasena': contrasena
        }
        objEntidad = Entidad(datosEntidad)

        if boton == 'Guardar':
            objControlEntidad.guardar(objEntidad)
            return jsonify({'success': True, 'message': 'Usuario guardado exitosamente'})
        
        elif boton == 'Consultar':
            objEntidad = objControlEntidad.buscarPorId('documento_usu', documento_usu)
            if objEntidad:
                return jsonify({'success': True, 'usuario': objEntidad.to_dict()})
            else:
                return jsonify({'success': False, 'message': 'Usuario no encontrado.'})

        elif boton == 'Modificar':
            objControlEntidad.modificar('documento_usu', documento_usu, objEntidad)
            return jsonify({'success': True, 'message': 'Usuario modificado exitosamente'})

        elif boton == 'Borrar':
            objControlEntidad.borrar('documento_usu', documento_usu)
            return jsonify({'success': True, 'message': 'Usuario borrado exitosamente'})

        else:
            return jsonify({'success': False, 'message': 'Acción no reconocida'})

    return jsonify({'success': False, 'message': 'Método no soportado'})
 """

# Suponiendo que existe un método to_dict() en la clase Entidad para convertir los datos en un diccionario.
     
    #Fin de lo nuevo
    # supuestamente no se usa esta linea, ya que se da al usuario como formato json
    return render_template('informe.html')