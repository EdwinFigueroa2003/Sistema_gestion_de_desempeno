from flask import Blueprint, render_template
import requests
from configBd import API_URL
 
# Crear un nuevo Blueprint para los detalles del microproyecto
vistadetallemicroproyecto = Blueprint('iddetallemicroproyecto', __name__, template_folder='templates')
 
@vistadetallemicroproyecto.route('/microproyecto/<int:id_microproyecto>', methods=['GET'])
def detalle_microproyecto(id_microproyecto):
    try:

        # Depuración: Imprimir el ID del microproyecto
        print(f"Obteniendo detalles para el microproyecto con ID: {id_microproyecto}")
        
        # Usar las rutas correctas para obtener detalles del microproyecto
        actividades_url = f'{API_URL}/actividades_clave/id_micro_proyecto/{id_microproyecto}'
        indicadores_url = f'{API_URL}/indicadores/id_micro_proyecto/{id_microproyecto}'
        aportes_url = f'{API_URL}/aportes_valor/id_micro_proyecto/{id_microproyecto}'

        # Depuración: Imprimir las URLs que se están solicitando
        print(f"Solicitando actividades clave de: {actividades_url}")
        print(f"Solicitando indicadores de: {indicadores_url}")
        print(f"Solicitando aportes de valor de: {aportes_url}")

        # Hacer solicitud a la API para obtener detalles del microproyecto
        actividades_response = requests.get(f'{API_URL}/actividades_clave/id_micro_proyecto/{id_microproyecto}', timeout=10)
        indicadores_response = requests.get(f'{API_URL}/indicadores/id_micro_proyecto/{id_microproyecto}', timeout=10)
        aportes_response = requests.get(f'{API_URL}/aportes_valor/id_micro_proyecto/{id_microproyecto}', timeout=10)
 


        # Verificar las respuestas de la API
        if actividades_response.status_code == 200:
            actividades_clave = actividades_response.json()
        else:
            actividades_clave = []
            print(f"Error en la solicitud de actividades clave: {actividades_response.status_code}")
 
        if indicadores_response.status_code == 200:
            indicadores = indicadores_response.json()

            # Depuración: Imprimir la respuesta de indicadores
            print(f"Indicadores obtenidos: {indicadores}")
        else:
            indicadores = []
            print(f"Error en la solicitud de indicadores: {indicadores_response.status_code}")
 
        if aportes_response.status_code == 200:
            aportes_valor = aportes_response.json()
                        
            # Depuración: Imprimir la respuesta de aportes de valor
            print(f"Aportes de valor obtenidos: {aportes_valor}")
        else:
            aportes_valor = []
            print(f"Error en la solicitud de aportes de valor: {aportes_response.status_code}")
 
        # Pasar los datos a la plantilla
        return render_template('detalle_microproyecto.html', 
                               actividades_clave=actividades_clave, 
                               indicadores=indicadores, 
                               aportes_valor=aportes_valor)
 
    except Exception as e:
        # Depuración: Imprimir cualquier error ocurrido durante la ejecución
        print(f"Error al obtener los detalles del microproyecto: {e}")
        return render_template('detalle_microproyecto.html', 
                               actividades_clave=[], 
                               indicadores=[], 
                               aportes_valor=[])