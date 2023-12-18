import os
from databas.database import numeroId
from main.main import menu_principal

numeroId = numeroId

def verificar_imagenes():
    carpeta_empleado = f"Data/faces/{numeroId}"
    if os.path.exists(carpeta_empleado) and os.listdir(carpeta_empleado):
        print(f"Empleado {numeroId} registrado. Rostros encontrados.")
    else:
        print(f"Empleado {numeroId} registrado, pero no se encontraron rostros.")
        opcion = input("¿Desea capturar un rostro ahora? (s/n): ").lower()
        if opcion == "s":
            print("Ejecutado. Registro perfecto")
            menu_principal()
        else:
            print("Volviendo al menú principal.")
            menu_principal()


