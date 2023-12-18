from databas.database import solicitudAcceso, insertarTrabajador

def menu_principal():
    while True:
        print("----Entrada----")
        print("Introduce una de las siguientes opciones")
        print("1. Verificación de empleado")
        print("2. Salir")

        opcion = int(input("Opción: "))

        if opcion == 1:
            solicitudAcceso()
        elif opcion == 2:
            print("¡Hasta luego! :D")
            break
        elif opcion == 3:
            insertarTrabajador()
        else:
            print("Esta no es una opción válida")
