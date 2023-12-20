# base/database.py

import sqlite3
import os
from tkinter import messagebox, simpledialog

def createTable():
    try:
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ids'")
            table_exist = cursor.fetchone()

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
        # Buscar el empleado en la base de datos por el código
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ids WHERE codigo = ?", (numeroId,))
            existeEmpleado = cursor.fetchone()

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
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre FROM ids WHERE codigo = ?", (numeroId,))
            empleado = cursor.fetchone()
            
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
        with sqlite3.connect("Data/idPersonales.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM ids WHERE codigo = ?", (int(numeroId),))
            existeEmpleado = cursor.fetchone()

            if existeEmpleado:
                print("Ya está registrado")
            else:
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
