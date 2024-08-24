Las carpetas que hay aquí, la importante es el "sistemagestiondesempeño" que es el que se actualiza.
La carpeta ENV es un entorno virtual que toca crearlo en cada dispositivo.
El otro archivo en una base de datos que se esta usando de prueba, hasta que se tenga la oficial.




""" from ControlEntidad import ControlEntidad """

""" # Define el Blueprint para login
login = Blueprint('inicio', __name__, template_folder='templates')

@app.route('/', methods = ['GET', 'POST'])
@login.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        email = markupsafe.escape(request.form['txtEmail'])
        contrasena = markupsafe.escape(request.form['txtContrasena'])

        api_url = "http://190.217.58.246:5184/api/SGD/procedures/execute"
        payload = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "usuario",
                "select_columns": "email, contrasena",
                "where_condition": f"email = '{email}'"
            }
        }

        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            users = response.json()
            user = users['outputParams']['result'][0] if users['outputParams']['result'] else None
            print(users)
            print(user)

            if user:
                if contrasena == user['contrasena']:
                    session['user_email'] = user['email']
                    return redirect(url_for('menu.html'))  # Asume que tienes una ruta 'home'
                else:
                    flash('Correo electrónico o contraseña inválidos', 'error')
            else:
                flash('Correo electrónico o contraseña inválidos', 'error')
        else:
            flash('Error al conectar con el servicio de autenticación.', 'error')
    
    return render_template('inicio.html') """