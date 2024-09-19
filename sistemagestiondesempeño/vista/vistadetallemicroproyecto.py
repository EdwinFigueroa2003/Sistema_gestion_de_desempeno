from flask import Blueprint, render_template
import requests
from configBd import API_URL
 
# Crear un nuevo Blueprint para los detalles del microproyecto
vistadetallemicroproyecto = Blueprint('iddetallemicroproyecto', __name__, template_folder='templates')
 
@vistadetallemicroproyecto.route('/microproyecto/<int:id_microproyecto>', methods=['GET'])
def detalle_microproyecto(id_microproyecto):
    try:
        # Hacer solicitud a la API para obtener detalles del microproyecto
        actividades_response = requests.get(f'{API_URL}/actividades_clave?id_micro_proyecto={id_microproyecto}', timeout=10)
        indicadores_response = requests.get(f'{API_URL}/indicadores?id_micro_proyecto={id_microproyecto}', timeout=10)
        aportes_response = requests.get(f'{API_URL}/aportes_valor?id_micro_proyecto={id_microproyecto}', timeout=10)
 
        # Verificar las respuestas de la API
        if actividades_response.status_code == 200:
            actividades_clave = actividades_response.json()
        else:
            actividades_clave = []
 
        if indicadores_response.status_code == 200:
            indicadores = indicadores_response.json()
        else:
            indicadores = []
 
        if aportes_response.status_code == 200:
            aportes_valor = aportes_response.json()
        else:
            aportes_valor = []
 
        # Pasar los datos a la plantilla
        return render_template('detalle_microproyecto.html', 
                               actividades_clave=actividades_clave, 
                               indicadores=indicadores, 
                               aportes_valor=aportes_valor)
 
    except Exception as e:
        print(f"Error al obtener los detalles del microproyecto: {e}")
        return render_template('detalle_microproyecto.html', 
                               actividades_clave=[], 
                               indicadores=[], 
                               aportes_valor=[])