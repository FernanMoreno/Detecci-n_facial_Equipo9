import cv2
import os
import face_recognition
import tkinter as tk
from PIL import Image, ImageTk

class RecognitionSystem:
    def __init__(self, app):
        self.faces_encodings = []
        self.faces_names = []
        self.detener_flag = False
        self.cap = None
        self.app = app

    def configurar_cap(self, cap):
        self.cap = cap

    def cargar_imagenes_empleado_global(self, codigo_empleado):
        carpeta_rostros = f"Data/faces/{codigo_empleado}"

        for file_name in os.listdir(carpeta_rostros):
            image_path = os.path.join(carpeta_rostros, file_name)
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(image)

            if face_locations:
                top, right, bottom, left = face_locations[0]
                face = image[top:bottom, left:right]

                face_encodings = face_recognition.face_encodings(face)

                if face_encodings:
                    f_coding = face_encodings[0]
                    self.faces_encodings.append(f_coding)
                    self.faces_names.append(file_name.split(".")[0])
            else:
                print(f"No se encontraron caras en la imagen: {file_name}")

    def detener(self):
        self.detener_flag = True
        if self.cap:
            self.cap.release()

    def realizar_reconocimiento_facial(self):
        try:
            while not self.detener_flag:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error al leer el fotograma de la cámara.")
                    break

                frame = cv2.flip(frame, 1)
                orig = frame.copy()
                faces = face_recognition.face_locations(frame)

                recognized = False

                if faces:
                    for (top, right, bottom, left) in faces:
                        face = orig[top:bottom, left:right]
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

                        encodings = face_recognition.face_encodings(face)

                        if encodings:
                            actual_face_encoding = encodings[0]

                            distances = face_recognition.face_distance(self.faces_encodings, actual_face_encoding)

                            if distances:
                                min_distance = min(distances)
                                result = list(distances <= 0.6)

                                if True in result:
                                    index = result.index(True)
                                    user_name = self.faces_names[index]
                                    security_percentage = (1 - min_distance) * 100
                                    color = (125, 220, 0)
                                    access_message = "Acceso Permitido"
                                    recognized = True
                                else:
                                    user_name = "Desconocido"
                                    security_percentage = None
                                    color = (50, 50, 255)
                                    access_message = "Acceso Denegado"

                                cv2.rectangle(frame, (left, bottom), (right, bottom + 30), color, -1)
                                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                                cv2.putText(frame, access_message, (left, bottom + 25), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

                                if security_percentage is not None:
                                    self.app.user_label.config(text=f"Usuario: {user_name} - Seguridad: {security_percentage:.2f}%")
                                else:
                                    self.app.user_label.config(text=f"Usuario: {user_name} - Seguridad: 0%")

                    if not recognized:
                        cv2.putText(frame, "Acceso Denegado", (10, 30), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

                photo = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.app.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.app.canvas.photo = photo

                self.app.update_idletasks()
                self.app.update()

        except cv2.error as cv2_error:
            print(f"Error de OpenCV: {cv2_error}")
        except Exception as e:
            print(f"Error en el reconocimiento facial: {e}")
            print("Faces Encodings:", self.faces_encodings)
            print("Faces Names:", self.faces_names)

        finally:
            if self.app:
                self.app.quit()
