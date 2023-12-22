# base/database.py

import sqlite3  # Importa el módulo sqlite3 para trabajar con bases de datos SQLite
import os  # Importa el módulo os para operaciones relacionadas con el sistema operativo
from tkinter import messagebox, simpledialog  # Importa componentes específicos de la biblioteca Tkinter

def createTable():
    try:
        # Conecta a la base de datos o la crea si no existe
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()

            # Verifica si la tabla 'ids' ya existe en la base de datos
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ids'")
            table_exist = cursor.fetchone()

            # Si la tabla no existe, la crea con columnas 'codigo' y 'nombre'
            if not table_exist:
                cursor.execute("""CREATE TABLE IF NOT EXISTS ids(
                                codigo INTEGER PRIMARY KEY,
                                nombre TEXT)""")
                print("Se creó la base de datos y la tabla 'ids'")
            else:
                print("La tabla 'ids' ya existe")

    except sqlite3.Error as e:
        print(f"ERROR: {e}")

def solicitudAcceso(numeroId):
    try:
        # Busca al empleado en la base de datos por el código
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ids WHERE codigo = ?", (numeroId,))
            existeEmpleado = cursor.fetchone()

            # Si el empleado existe, devuelve acceso y el nombre asociado al código
            if existeEmpleado:
                nombreEmpleado = existeEmpleado[1]
                print(f"Acceso permitido. Nombre asociado al id de empleado {numeroId}: {nombreEmpleado}")
                acceso = True
                return acceso, nombreEmpleado
            else:
                print("El empleado no se encuentra en la lista")
                acceso = False
                return acceso, None

    except Exception as e:
        print(f"Error: {e}")
        acceso = False
        return acceso, None

def getEmployeeData(numeroId):
    try:
        # Obtiene el nombre del empleado desde la base de datos por el código
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM ids WHERE codigo = ?", (numeroId,))
            empleado = cursor.fetchone()

            # Si se encuentra el empleado, devuelve True y el nombre, de lo contrario, False y None
            if empleado:
                nombre_empleado = empleado[0]
                return True, nombre_empleado
            else:
                return False, None

    except Exception as e:
        print(f"Error: {e}")
        return False, None

def insertarTrabajador(numeroId, nombreEmpleado):
    try:
        # Inserta un nuevo trabajador en la base de datos si no existe
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ids WHERE codigo = ?", (int(numeroId),))
            existeEmpleado = cursor.fetchone()

            if existeEmpleado:
                print("Ya está registrado")
            else:
                # Inserta el nuevo empleado y crea una carpeta para almacenar sus datos
                cursor.execute("INSERT INTO ids (codigo, nombre) VALUES (?, ?)", (int(numeroId), nombreEmpleado))
                conexion.commit()
                print("Empleado registrado")

                carpeta_empleado = f"Data/Rostros/{numeroId}"
                os.makedirs(carpeta_empleado, exist_ok=True)
                print(f"Carpeta para el empleado {numeroId} creada")

    except Exception as e:
        print(f"Error: {e}")

# Crear la tabla al importar el módulo
createTable()
