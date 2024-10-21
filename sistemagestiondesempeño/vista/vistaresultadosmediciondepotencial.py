from flask import Blueprint, render_template
from configBd import API_URL
from markupsafe import Markup
import requests
import plotly.graph_objects as go
 
# Crear un Blueprint
vistaresultadosmediciondepotencial = Blueprint('idresultadosmediciondepotencial', __name__, template_folder='templates')

@vistaresultadosmediciondepotencial.route('/resultadosmediciondepotencial', methods=['GET'])
def vista_resultados_medicion_de_potencial():
    try:
        # Obtener todas las respuestas guardadas
        url_respuestas_guardadas = f"{API_URL}/dimension_mp_respuesta_guardada"
        response_respuestas = requests.get(url_respuestas_guardadas)
        response_respuestas.raise_for_status()
        respuestas_guardadas = response_respuestas.json()

        detalles_respuestas = []
        categorias = []
        niveles = []

        for respuesta_guardada in respuestas_guardadas:
            try:
                # Obtener detalles de la dimensión
                url_dimension = f"{API_URL}/dimension_mp/id_dimension_mp/{respuesta_guardada['id_dimension_mp']}"
                response_dimension = requests.get(url_dimension)
                response_dimension.raise_for_status()
                dimension_detalle = response_dimension.json()[0]

                # Obtener detalles de la respuesta
                url_respuesta = f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_respuesta/{respuesta_guardada['id_dimension_mp_respuesta']}"
                response_respuesta = requests.get(url_respuesta)
                response_respuesta.raise_for_status()
                respuesta_detalle = response_respuesta.json()[0]

                # Agregar los datos para el gráfico
                categorias.append(dimension_detalle['nombre'])
                niveles.append(respuesta_detalle['nivel'])

                # Crear el detalle de la respuesta
                detalle = {
                    'dimension': dimension_detalle['nombre'],
                    'respuesta': respuesta_detalle['respuesta_mp'],
                    'nivel': respuesta_detalle['nivel'],
                    'fecha_respuesta': respuesta_guardada['fecha_respuesta']
                }
                detalles_respuestas.append(detalle)

            except Exception as e:
                detalles_respuestas.append({
                    'dimension': 'Error',
                    'respuesta': str(e),
                    'nivel': 'N/A',
                    'fecha_respuesta': respuesta_guardada['fecha_respuesta']
                })

        # Calcular el promedio de los niveles
        if niveles:
            promedio_nivel = sum(niveles) / len(niveles)
            promedio_nivel_redondeado = round(promedio_nivel)
        else:
            promedio_nivel_redondeado = 0

        # Obtener la información del nivel promedio
        url_nivel = f"{API_URL}/dimension_mp_respuesta_nivel/id_nivel/{promedio_nivel_redondeado}"
        print(url_nivel)
        response_nivel = requests.get(url_nivel)
        response_nivel.raise_for_status()
        nivel_detalle = response_nivel.json()[0]
        print('cual es el nivel detalle: ', nivel_detalle)

        # Crear gráfico de araña
        fig = go.Figure()

        # Añadir la primera (y única) traza del gráfico
        fig.add_trace(go.Scatterpolar(
            r=niveles,
            theta=categorias,
            fill='toself',
            name='Nivel de Respuesta'
        ))

        # Configurar el gráfico
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 6]
                )
            ),
            showlegend=False,
            width=625,
            height=500
        )

        # Convertir el gráfico en HTML
        grafico_html = Markup(fig.to_html(full_html=False))

        return render_template('resultadosmediciondepotencial.html', respuestas=detalles_respuestas, grafico=grafico_html, nivel_detalle=nivel_detalle)

    except requests.RequestException as e:
        return render_template('resultadosmediciondepotencial.html', respuestas=[], error=str(e))

""" @vistaresultadosmediciondepotencial.route('/resultadosmediciondepotencial', methods=['GET'])
def vista_resultados_medicion_de_potencial():
    try:
        # Obtener todas las respuestas guardadas
        url_respuestas_guardadas = f"{API_URL}/dimension_mp_respuesta_guardada"
        response_respuestas = requests.get(url_respuestas_guardadas)
        response_respuestas.raise_for_status()
        respuestas_guardadas = response_respuestas.json()

        detalles_respuestas = []
        categorias = []
        niveles = []

        for respuesta_guardada in respuestas_guardadas:
            try:
                # Obtener detalles de la dimensión
                url_dimension = f"{API_URL}/dimension_mp/id_dimension_mp/{respuesta_guardada['id_dimension_mp']}"
                response_dimension = requests.get(url_dimension)
                response_dimension.raise_for_status()
                dimension_detalle = response_dimension.json()[0]

                # Obtener detalles de la respuesta
                url_respuesta = f"{API_URL}/dimension_mp_respuesta/id_dimension_mp_respuesta/{respuesta_guardada['id_dimension_mp_respuesta']}"
                response_respuesta = requests.get(url_respuesta)
                response_respuesta.raise_for_status()
                respuesta_detalle = response_respuesta.json()[0]

                # Agregar los datos para el gráfico
                categorias.append(dimension_detalle['nombre'])
                niveles.append(respuesta_detalle['nivel'])

                # Crear el detalle de la respuesta
                detalle = {
                    'dimension': dimension_detalle['nombre'],
                    'respuesta': respuesta_detalle['respuesta_mp'],
                    'nivel': respuesta_detalle['nivel'],
                    'fecha_respuesta': respuesta_guardada['fecha_respuesta']
                }
                detalles_respuestas.append(detalle)

            except Exception as e:
                detalles_respuestas.append({
                    'dimension': 'Error',
                    'respuesta': str(e),
                    'nivel': 'N/A',
                    'fecha_respuesta': respuesta_guardada['fecha_respuesta']
                })

        # Calcular el promedio de los niveles
        if niveles:
            promedio_nivel = sum(niveles) / len(niveles)
            promedio_nivel_redondeado = round(promedio_nivel)
        else:
            promedio_nivel_redondeado = 0

        # Obtener la información del nivel promedio
        url_nivel = f"{API_URL}/dimension_mp_respuesta_nivel/id_nivel/{promedio_nivel_redondeado}"
        response_nivel = requests.get(url_nivel)
        response_nivel.raise_for_status()
        nivel_detalle = response_nivel.json()

        # Crear gráfico de araña
        fig = go.Figure()

        # Añadir la primera (y única) traza del gráfico
        fig.add_trace(go.Scatterpolar(
            r=niveles,
            theta=categorias,
            fill='toself',
            name='Nivel de Respuesta'
        ))

        # Configurar el gráfico
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 6]
                )
            ),
            showlegend=False,
            width=625,
            height=500
        )

        # Convertir el gráfico en HTML
        grafico_html = Markup(fig.to_html(full_html=False))

        return render_template('resultadosmediciondepotencial.html', respuestas=detalles_respuestas, grafico=grafico_html, nivel_detalle=nivel_detalle)

    except requests.RequestException as e:
        return render_template('resultadosmediciondepotencial.html', respuestas=[]) """