import sqlite3
import os

# Conectar a la base de datos SQLite
conexion = sqlite3.connect("Data/idPersonales.db")
cursor = conexion.cursor()

# Función para crear la tabla si no existe
def createTable():
    try:
        # Verificar si la tabla 'ids' ya existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ids'")
        table_exist = cursor.fetchone()

        if not table_exist:
            # Crear la tabla 'ids' si no existe
            conexion.execute("""CREATE TABLE IF NOT EXISTS ids(
                            codigo INTEGER PRIMARY KEY,
                            nombre TEXT)""")
            print("Se creó la base de datos y la tabla 'ids'")
        else:
            print("La tabla 'ids' ya existe")

    except sqlite3.OperationalError as e:
        print(f"ERROR: {e}")

    finally:
        conexion.close()  # Cerrar la conexión a la base de datos


# Función para solicitar acceso
def solicitudAcceso():
    try:
        numeroId = int(input("Introduce tu numero de empleado (4 dígitos): "))

        # Buscar el empleado en la base de datos por el código
        cursor.execute("SELECT * FROM ids WHERE codigo = ?", (numeroId,))
        existeEmpleado = cursor.fetchone()

        if existeEmpleado:
            nombreEmpleado = existeEmpleado[1]
            print(f"Acceso permitido. Nombre asociado al id de empleado {numeroId}: {nombreEmpleado}")
            acceso = True
            return acceso
        else:
            print("El empleado no se encuentra en la lista")
            acceso = False
            return acceso, numeroId

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conexion.close()  # Cerrar la conexión a la base de datos


# Función para insertar un nuevo trabajador
def insertarTrabajador():
    try:
        numeroId = input("Introduce el nuevo id de empleado (máximo 4 dígitos): ")
        nombreEmpleado = input("Nombre del empleado: ")

        if len(numeroId) == 4 and numeroId.isdigit() and not numeroId.startswith('0'):
            # Buscar el empleado en la base de datos por el código
            cursor.execute("SELECT * FROM ids WHERE codigo = ?", (int(numeroId),))
            existeEmpleado = cursor.fetchone()

            if existeEmpleado:
                print("Ya está registrado")
            else:
                # Insertar nuevo empleado en la base de datos
                cursor.execute("INSERT INTO ids (codigo, nombre) VALUES (?, ?)", (int(numeroId), nombreEmpleado))
                conexion.commit()
                print("Empleado registrado")

                carpeta_empleado = f"Data/faces/{numeroId}"
                os.makedirs(carpeta_empleado, exist_ok=True)
                print(f"Carpeta para el empleado {numeroId} creada")
        else:
            print("El id debe tener exactamente 4 dígitos y no puede comenzar con 0")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conexion.close()  # Cerrar la conexión a la base de datos
    
#createTable()

insertarTrabajador()

#solicitudAcceso()


