
# extract_faces.py
import cv2
import os
import face_recognition

def capturar_rostro(numeroId, nombre_empleado):
    carpeta_rostros = f"Data/faces/{numeroId}"

    if not os.path.exists(carpeta_rostros):
        os.makedirs(carpeta_rostros)

    # Inicializar la cámara
    cap = cv2.VideoCapture(0)

    try:
        count_images = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error al leer el fotograma de la cámara.")
                break

            frame = cv2.flip(frame, 1)
            faces = face_recognition.face_locations(frame)

            for (top, right, bottom, left) in faces:
                face = frame[top:bottom, left:right]
                face_filename = f"{carpeta_rostros}/{nombre_empleado}_1.jpg"
                cv2.imwrite(face_filename, cv2.cvtColor(face, cv2.COLOR_BGR2RGB))  # Guardar la imagen con el formato correcto
                count_images += 1

            cv2.imshow("Captura de Rostro", frame)

            if count_images >= 1:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        print(f"Se capturó 1 imagen.")

    except cv2.error as cv2_error:
        print(f"Error de OpenCV: {cv2_error}")
    except Exception as e:
        print(f"Error al capturar el rostro: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Ejemplo de uso
# capturar_rostro(1001, "UsuarioEjemplo")

