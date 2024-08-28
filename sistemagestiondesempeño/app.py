from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000/api/{projectName}/procedures/execute"
headers = {'Content-Type': 'application/json'}

@app.route('/', ['GET', 'POST'])
def inicio():
    return render_template('inicio.html')

@app.route('/execute', methods=['POST'])
def execute_procedure():
    print(request.headers)  # Agregar esta línea para ver los encabezados
    # Verificar que el Content-Type sea application/json
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Must be application/json."}), 400

    data = request.get_json()

    try:
        # Realizar la solicitud POST a la API externa
        response = requests.post(API_URL.format(projectName=data['projectName']), json={
            "procedure": data['procedure'],
            "parameters": data['parameters']
        }, headers=headers)

        # Verificar si la solicitud fue exitosa
        response.raise_for_status()
        
        # Devolver la respuesta JSON de la API externa
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        # Manejar cualquier error que ocurra durante la solicitud
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

