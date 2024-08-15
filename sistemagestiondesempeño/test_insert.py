import requests

# URL de tu servidor Flask
FLASK_URL = "http://127.0.0.1:5000/execute"

# Datos para la solicitud POST /execute
insert_data = {
    "projectName": "your_project_name",
    "procedure": "insert_json_entity",
    "parameters": {
        "table_name": "usuario",
        "json_data": {
            "consecutivo_usu": 1,
            "fk_costo_usu": 1,
            "fk_rol_usu": 1,
            "fk_cargo_usu": 1,
            "documento_usu": "1234567890",
            "contrasena": "password",
            "estado_usu": "Activo",
            "foto_usu": "foto.jpg",
            "email": "email@example.com"
        }
    }
}

# Realiza la solicitud POST a /execute
response = requests.post(FLASK_URL, json=insert_data)
print("Response status code:", response.status_code)
print("Response JSON:", response.json())



# URL de tu servidor Flask
FLASK_URL = "http://127.0.0.1:5000/execute"

# Datos para la solicitud POST /execute
update_data = {
    "projectName": "your_project_name",
    "procedure": "update_json_entity",
    "parameters": {
        "table_name": "usuario",
        "json_data": {
            "estado_usu": "Inactivo"
        },
        "where_condition": "consecutivo_usu = 1"
    }
}

# Realiza la solicitud POST a /execute
response = requests.post(FLASK_URL, json=update_data)
print("Response status code:", response.status_code)
print("Response JSON:", response.json())


#Eliminación en usuario
#Guarda el siguiente código en un archivo llamado test_delete.py:



# URL de tu servidor Flask
FLASK_URL = "http://127.0.0.1:5000/execute"

# Datos para la solicitud POST /execute
delete_data = {
    "projectName": "your_project_name",
    "procedure": "delete_json_entity",
    "parameters": {
        "table_name": "usuario",
        "where_condition": "consecutivo_usu = 1"
    }
}

# Realiza la solicitud POST a /execute
response = requests.post(FLASK_URL, json=delete_data)
print("Response status code:", response.status_code)
print("Response JSON:", response.json())



# URL de tu servidor Flask
FLASK_URL = "http://127.0.0.1:5000/execute"

# Datos para la solicitud POST /execute
select_data = {
    "projectName": "your_project_name",
    "procedure": "select_json_entity",
    "parameters": {
        "table_name": "usuario u JOIN evaluacion e ON u.fk_cargo_usu = e.fk_tipo_eval",
        "json_data": {
            "fk_costo_usu": 1
        },
        "where_condition": "u.fk_costo_usu = :fk_costo_usu",
        "select_columns": "u.consecutivo_usu, u.documento_usu, e.nombre_eval, e.fecha_creacion_eval",
        "order_by": "u.consecutivo_usu ASC",
        "limit_clause": ""
    }
}

# Realiza la solicitud POST a /execute
response = requests.post(FLASK_URL, json=select_data)
print("Response status code:", response.status_code)
print("Response JSON:", response.json())


