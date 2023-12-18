import os

def rostro():
    personName = input("Introduzca el nombre: ")
    dataPath = "Reconocimiento_Facial/Data"
    personPath = f"{dataPath}/{personName}"
    return personPath