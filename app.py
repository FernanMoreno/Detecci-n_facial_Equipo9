import cv2
import os
import face_recognition
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Codificar los rostros extraídos
image_faces_path = r"C:\Users\bniet\OneDrive\Desktop\BootCamp IA\Detecci-n_facial_Equipo9\faces"

faces_encodings = []
faces_names = []
for file_name in os.listdir(image_faces_path):
    image = cv2.imread(os.path.join(image_faces_path, file_name))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    f_coding = face_recognition.face_encodings(image, known_face_locations=[(0, 150, 150, 0)])[0]
    faces_encodings.append(f_coding)
    faces_names.append(file_name.split(".")[0])

# Función para el hilo de video
def video_thread():
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        orig = frame.copy()
        faces = face_classif.detectMultiScale(frame, 1.1, 5)

        recognized = False

        for (x, y, w, h) in faces:
            face = orig[y:y + h, x:x + w]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            actual_face_encoding = face_recognition.face_encodings(face, known_face_locations=[(0, w, h, 0)])[0]
            distances = face_recognition.face_distance(faces_encodings, actual_face_encoding)
            min_distance = min(distances)
            result = list(distances <= 0.6)

            if True in result:
                index = result.index(True)
                user_name = faces_names[index]
                security_percentage = (1 - min_distance) * 100
                color = (125, 220, 0)
                access_message = "Acceso Permitido"
                recognized = True
            else:
                user_name = "Desconocido"
                security_percentage = None
                color = (50, 50, 255)
                access_message = "Acceso Denegado"

            cv2.rectangle(frame, (x, y + h), (x + w, y + h + 30), color, -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, access_message, (x, y + h + 25), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

            if security_percentage is not None:
                user_label.config(text=f"Usuario: {user_name} - Seguridad: {security_percentage:.2f}%")
            else:
                user_label.config(text=f"Usuario: {user_name} - Seguridad: 0%")

        if not recognized:
            cv2.putText(frame, "Acceso Denegado", (10, 30), 2, 1, (255, 255, 255), 2, cv2.LINE_AA)

        photo = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.photo = photo

        root.update_idletasks()
        root.update()

# LEYENDO VIDEO
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Detector facial
face_classif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Reconocimiento Facial")
root.configure(bg='#000000')

# Etiqueta para mostrar el mensaje explicativo y el nombre del usuario
info_label = tk.Label(root, text="Por favor, acerque su cara a la cámara", fg="white", bg="black", font=("Helvetica", 16))
info_label.pack(padx=10, pady=10)

user_label = tk.Label(root, text="Usuario: ", fg="white", bg="black", font=("Helvetica", 16))
user_label.pack(padx=10, pady=10)

# Lienzo para mostrar el video
canvas = tk.Canvas(root, width=640, height=480, bg='#000000')
canvas.pack()

# Función para cerrar la aplicación
def close_app(event):
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# Enlazar funciones a eventos
root.bind('<Escape>', close_app)

# Iniciar el hilo de video
video_thread = threading.Thread(target=video_thread)
video_thread.daemon = True  # Establecer como hilo demonio  
video_thread.start()


# Iniciar el bucle principal de Tkinter
root.mainloop()
