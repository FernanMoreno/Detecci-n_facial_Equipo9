import cv2
import os
import tkinter as tk
from tkinter.simpledialog import askstring
from base.database import createTable, solicitudAcceso, insertarTrabajador
from recognition_system import RecognitionSystem
from PIL import Image, ImageTk
import time
import threading
from extract_faces import capturar_rostro

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Reconocimiento Facial")
        self.configure(bg='#000000')

        self.info_label = tk.Label(self, text="Por favor, acerque su cara a la cámara", fg="white", bg="black",
                                   font=("Helvetica", 16))
        self.info_label.pack(padx=10, pady=10)

        self.user_label = tk.Label(self, text="Usuario: ", fg="white", bg="black", font=("Helvetica", 16))
        self.user_label.pack(padx=10, pady=10)

        self.result_label = tk.Label(self, text="", fg="red", bg="black", font=("Helvetica", 16))
        self.result_label.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(self, width=640, height=480, bg='#000000')
        self.canvas.pack()

        self.menu_var = tk.StringVar(self)
        self.menu_var.set("Seleccionar Acción")

        self.menu = tk.OptionMenu(self, self.menu_var, "Seleccionar Acción", "Entrar", "Salir", "Registrar")
        self.menu.pack(pady=10)

        self.btn_ejecutar = tk.Button(self, text="Ejecutar Acción", command=self.ejecutar_accion)
        self.btn_ejecutar.pack(pady=10)

        self.cap = cv2.VideoCapture(0)  # Instancia de la cámara
        self.recognition_system = RecognitionSystem(self)
        self.recognition_system.configurar_cap(self.cap)  # Pasa la instancia de la cámara
        createTable()

        self.detener_hilo = False
        self.hilo_camara = threading.Thread(target=self.actualizar_camara)
        self.hilo_camara.start()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def ejecutar_accion(self):
        accion = self.menu_var.get()

        if accion == "Entrar":
            self.verificar_empleado()
        elif accion == "Salir":
            self.salir()
        elif accion == "Registrar":
            self.registrar_empleado()
        else:
            self.info_label.config(text="Selecciona una acción válida")

    def iniciar_camara(self):
        if not self.cap or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.recognition_system.configurar_cap(self.cap)
            self.mostrar_resultado("Cámara iniciada.")

    def verificar_empleado(self):
        try:
            numeroId = askstring("Número de Empleado", "Introduce tu número de empleado (4 dígitos):")

            if numeroId and numeroId.isdigit() and len(numeroId) == 4:
                numeroId = int(numeroId)
                acceso, nombre_empleado = solicitudAcceso(numeroId)

                if acceso:
                    if nombre_empleado is not None:
                        print(f"Acceso permitido. Nombre asociado al id de empleado {numeroId}: {nombre_empleado}")
                    else:
                        print(f"Acceso permitido. Id de empleado: {numeroId}")

                    self.recognition_system.cargar_imagenes_empleado_global(numeroId)
                    self.iniciar_camara()
                    self.recognition_system.realizar_reconocimiento_facial()
                else:
                    self.mostrar_resultado("Acceso denegado. Número de empleado no encontrado en la base de datos.")
            else:
                self.mostrar_resultado("El número de empleado debe tener exactamente 4 dígitos y ser un número entero.")

        except Exception as e:
            print(f"Error: {e}")

    def salir(self):
        self.info_label.config(text="Saliendo...")
        self.detener_hilo = True
        if self.cap:
            self.cap.release()
        if self.recognition_system:
            self.recognition_system.detener()
        self.destroy()

    def registrar_empleado(self):
        try:
            numeroId = askstring("Número de Empleado", "Introduce el número de empleado (4 dígitos):")

            if numeroId and numeroId.isdigit() and len(numeroId) == 4:
                numeroId = int(numeroId)
                nombre_empleado = askstring("Nombre de Empleado", "Introduce el nombre del empleado:")

                if nombre_empleado:
                    insertarTrabajador(numeroId, nombre_empleado)

                    carpeta_rostros = f"Data/faces/{numeroId}"
                    if not os.path.exists(carpeta_rostros):
                        os.makedirs(carpeta_rostros)

                    # Capturar y almacenar la foto en el repositorio
                    capturar_rostro(numeroId, nombre_empleado)

                    self.recognition_system.cargar_imagenes_empleado_global(numeroId)
                else:
                    print("Nombre de empleado no ingresado.")
            else:
                print("El número de empleado debe tener exactamente 4 dígitos y ser un número entero.")

        except Exception as e:
            print(f"Error: {e}")

    def mostrar_resultado(self, mensaje):
        if self.result_label:
            self.result_label.config(text=mensaje)
            self.update_idletasks()
            self.update()

    def on_closing(self):
        self.detener_hilo = True
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.recognition_system:
            self.recognition_system.detener()
        self.destroy()

        # Agrega un tiempo para asegurar que la cámara se libere antes de cerrar
        self.after(1000, self.quit)

    def actualizar_camara(self):
        try:
            while not self.detener_hilo and self.winfo_exists():
                time.sleep(0.01)  # Agrega un pequeño retardo para liberar el hilo
        except Exception as e:
            print(f"Error en el hilo de la cámara: {e}")

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
