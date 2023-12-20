import cv2
import numpy as np

# Model Architecture
prototxt = "C:/Users/ferna/Desktop/F5/Reconocimiento_Facial/model/deploy.prototxt.txt"

# Weights
model = 'C:/Users/ferna/Desktop/F5/Reconocimiento_Facial/model/res10_300x300_ssd_iter_140000.caffemodel'

# Load model
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# Inicializar la cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

# Crear una ventana para mostrar el video
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

try:
    while True:
        ret, frame = cap.read()

        # Verificar si se pudo leer el fotograma
        if not ret or frame is None:
            print("Error al leer el fotograma.")
            break

        # Escalar y convertir a blob
        height, width, _ = frame.shape
        frame_resized = cv2.resize(frame, (300, 300))
        blob = cv2.dnn.blobFromImage(frame_resized, 1.0, (300, 300), (104, 117, 123))

        # Pasar el blob a la red neuronal
        net.setInput(blob)
        detections = net.forward()

        # Umbral de confianza
        confidence_threshold = 0.7

        for detection in detections[0, 0]:
            confidence = detection[2]

            # Si la confianza es mayor que el umbral, dibujar el rectángulo
            if confidence > confidence_threshold:
                box = detection[3:7] * np.array([width, height, width, height])
                x_start, y_start, x_end, y_end = map(int, box)
                cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
                cv2.putText(frame, f"Conf: {confidence:.2f}", (x_start, y_start - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # Mostrar el fotograma en la ventana
        cv2.imshow('Video', frame)

        # Salir del bucle si se presiona la tecla 'Esc'
        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    # Manejar la interrupción del usuario (pulsar 'Ctrl+C' en la consola)
    pass

finally:
    # Liberar la cámara y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

