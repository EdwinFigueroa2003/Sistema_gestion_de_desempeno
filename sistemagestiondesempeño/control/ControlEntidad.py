from pprint import pprint
import psycopg2
from psycopg2 import errors
from control.ControlConexion import ControlConexion
from Entidad import Entidad
from configBd import * 

class ControlEntidad:
    def __init__(self, nombre_tabla):
        self.tabla = nombre_tabla
        self.objControlConexion = ControlConexion()  
    def validarIngreso(self, clave_primaria, valorCp,contrasena,valorCo):
        valido = False
        try:
            conexion = self.objControlConexion.abrirBd(servidor=serv, usuario=usua, password=passw, db=bdat, puerto=port)
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return None 
            cursor = conexion.cursor()

            sql = f"SELECT * FROM {self.tabla} WHERE {clave_primaria} = %s AND {contrasena} = %s"
            print("sql=",sql)
            cursor.execute(sql, [valorCp,valorCo])

            resultado = cursor.fetchone()  # Obtener el primer resultado
            
            if resultado:
                valido=True
        except psycopg2.Error as e:
            print(f"Error al buscar en {self.tabla} por ID: {e.pgerror}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return valido
 
    def guardar(self, entidad):
        resultado = False
        try:
            conexion = self.objControlConexion.abrirBd(servidor=serv, usuario=usua, password=passw, db=bdat, puerto=port)
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return False 
            cursor = conexion.cursor()
 
            propiedades = entidad.obtener_propiedades()
            campos = propiedades.keys()
            valores = propiedades.values()
            placeholders = ", ".join(["%s"] * len(campos))
            query_campos = ", ".join(campos)
            sql = f"INSERT INTO {self.tabla} ({query_campos}) VALUES ({placeholders})"
            cursor.execute(sql, list(valores))
            conexion.commit()
            resultado = True
 
            # Si la tabla es 'usuario', también guardar en la tabla 'rol_usuario'
            if self.tabla == 'usuario':
                email = propiedades.get('email', '')  # Obtener el email del usuario
                roles = propiedades.get('roles', [])   # Obtener los roles del usuario
 
                # Guardar en la tabla 'rol_usuario'
                self.guardar_rol_usuario(conexion, cursor, email, roles)
 
        except psycopg2.Error as e:
            print(f"Error al guardar en {self.tabla}: {e.pgerror}")
            conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return resultado
 
    def guardar_rol_usuario(self, conexion, cursor, email, roles):
        try:
            for rol in roles:
                sql = "INSERT INTO rol_usuario (email, id_rol) VALUES (%s, %s)"
                cursor.execute(sql, (email, rol))
            conexion.commit()
        except psycopg2.Error as e:
            print(f"Error al guardar roles en la tabla rol_usuario: {e.pgerror}")
            conexion.rollback()
        except Exception as e:
            print(f"Error inesperado al guardar roles en la tabla rol_usuario: {e}")
            conexion.rollback()

    def modificar(self, clave_primaria, valor, entidad):
        resultado = False
        try:
            conexion = self.objControlConexion.abrirBd(servidor=serv, usuario=usua, password=passw, db=bdat, puerto=port)
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return False 
            cursor = conexion.cursor()

            propiedades = entidad.obtener_propiedades()
            actualizaciones = []
            valores = []
            for campo, valor_campo in propiedades.items():
                if campo != clave_primaria:
                    actualizaciones.append(f"{campo} = %s")
                    valores.append(valor_campo)

            valores.append(valor)  # El valor de la clave primaria para el WHERE
            sql = f"UPDATE {self.tabla} SET {', '.join(actualizaciones)} WHERE {clave_primaria} = %s"
            print("sql=",sql)
            cursor.execute(sql, valores)
            conexion.commit()
            resultado = True

        except psycopg2.Error as e:
            print(f"Error al actualizar en {self.tabla}: {e.pgerror}")
            conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return resultado

    def borrar(self, clave_primaria, valor):
        resultado = False
        try:
            conexion = self.objControlConexion.abrirBd(servidor=serv, usuario=usua, password=passw, db=bdat, puerto=port)
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return False            
            cursor = conexion.cursor()
            
            sql = f"DELETE FROM {self.tabla} WHERE {clave_primaria} = %s"
            print("sql=",sql)
            cursor.execute(sql, [valor])
            conexion.commit()
            resultado = True

        except psycopg2.Error as e:
            print(f"Error al eliminar en {self.tabla}: {e.pgerror}")
            conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return resultado
    
    def buscarPorId(self, clave_primaria, valor):
        entidad = None
        try:
            conexion = self.objControlConexion.abrirBd(servidor=serv, usuario=usua, password=passw, db=bdat, puerto=port)
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return None 
            cursor = conexion.cursor()

            sql = f"SELECT * FROM {self.tabla} WHERE {clave_primaria} = %s"
            print("sql=",sql)
            cursor.execute(sql, [valor])

            resultado = cursor.fetchone()  # Obtener el primer resultado
            
            # Si hay un resultado, construye un objeto Entidad a partir de él.
            if resultado:
                columnas = [desc[0] for desc in cursor.description]  # obtener los nombres de las columnas
                propiedades = dict(zip(columnas, resultado))  # mapea las columnas a sus valores correspondientes
                entidad = Entidad(propiedades)

        except psycopg2.Error as e:
            print(f"Error al buscar en {self.tabla} por ID: {e.pgerror}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        
        return entidad  # Retorna un objeto Entidad o None si no se encuentra el registro.

    def listar(self):
        resultados = []
        conexion = None
        cursor = None
        try:
            conexion = self.objControlConexion.abrirBd(servidor=serv, usuario=usua, password=passw, db=bdat, puerto=port)
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return []  # Retorna una lista vacía en caso de fallo de conexión
            cursor = conexion.cursor()

            sql = f"SELECT * FROM {self.tabla}"
            cursor.execute(sql)
            resultados = cursor.fetchall()  # Obtener todos los resultados
        except psycopg2.Error as e:
            print(f"Error al listar {self.tabla}: {e.pgerror}")
            if conexion:
                conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            if conexion:
                conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if self.objControlConexion and conexion:
                self.objControlConexion.cerrarBd()

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]
        
        # Convertir cada fila de resultados en un objeto Entidad
        entidades = [Entidad(dict(zip(columnas, row))) for row in resultados]
        return entidades

    def consultar(self, consulta, parametros=None):
        resultados = []
        conexion = None
        cursor = None
        try:
            conexion = self.objControlConexion.abrirBd(servidor=serv, usuario=usua, password=passw, db=bdat, puerto=port)
            cursor = conexion.cursor()

            cursor.execute(consulta, parametros if parametros else ())
            resultados = cursor.fetchall()  # Obtener todos los resultados

        except psycopg2.Error as e:
            print(f"Error al realizar la consulta en {self.tabla}: {e.pgerror}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            if cursor:
                cursor.close()
            if self.objControlConexion and conexion:
                self.objControlConexion.cerrarBd()

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Convertir cada fila de resultados en un objeto Entidad
        entidades = [Entidad(dict(zip(columnas, row))) for row in resultados]

        return entidades


""" import requests

# Configuración de la URL base del servidor
PROJECT_NAME = "SGD"
BASE_URL = f"http://190.217.58.246:5184/api/{PROJECT_NAME}/procedures/execute"  # Reemplaza con la URL correcta

class ControlEntidad:
    def _init_(self, table_name):
        self.table_name = table_name

    def validarIngreso(self, email, contrasena):  # Añadido self
        condition = {
            "username": email,
            "password": contrasena
        }
        select_columns = ["email"]

        payload = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": self.table_name,  # Usar el atributo de instancia
                "where_condition": condition,
                "select_columns": select_columns
            }
        }
        response = requests.post(BASE_URL, json=payload)
        result = response.json()

        return bool(result.get("data"))

    def insert_data(self, data):
        payload = {
            "procedure": "insert_json_entity",
            "parameters": {
                "table_name": self.table_name,
                "json_data": data
            }
        }
        response = requests.post(BASE_URL, json=payload)
        return response.json()

    def update_data(self, data, condition):
        payload = {
            "procedure": "update_json_entity",
            "parameters": {
                "table_name": self.table_name,
                "json_data": data,
                "where_condition": condition
            }
        }
        response = requests.post(BASE_URL, json=payload)
        return response.json()

    def delete_data(self, condition):
        payload = {
            "procedure": "delete_json_entity",
            "parameters": {
                "table_name": self.table_name,
                "where_condition": condition
            }
        }
        response = requests.post(BASE_URL, json=payload)
        return response.json()

    def select_data(self, condition=None, order_by=None, limit=None, select_columns=None):
        payload = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": self.table_name,
                "where_condition": condition,
                "order_by": order_by,
                "limit_clause": limit,
                "select_columns": select_columns
            }
        }
        response = requests.post(BASE_URL, json=payload)
        return response.json() """