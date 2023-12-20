import cv2
import os
import numpy as np

# Model Architecture
prototxt = "C:/Users/ferna/Desktop/F5/Reconocimiento_Facial/model/deploy.prototxt.txt"

# Weights
model = 'C:/Users/ferna/Desktop/F5/Reconocimiento_Facial/model/res10_300x300_ssd_iter_140000.caffemodel'

# Load model
net = cv2.dnn.readNetFromCaffe(prototxt, model)

# Ruta de la carpeta con las imágenes desconocidas
image_folder_path = "C:/Users/ferna/Desktop/F5/Reconocimiento_Facial/knowns"

# Lista de nombres de archivos en la carpeta
image_files = os.listdir(image_folder_path)

for image_file in image_files:
    # Ruta completa de la imagen
    image_path = os.path.join(image_folder_path, image_file)

    # Leer la imagen
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: No se pudo cargar la imagen en la ruta: {image_path}")
        continue

    height, width, _ = image.shape
    image_resized = cv2.resize(image, (300, 300))

    # Crear blob
    blob = cv2.dnn.blobFromImage(image_resized, 1.0, (300, 300), (104, 117, 123))

    # Pasar el blob a la red neuronal
    net.setInput(blob)
    detections = net.forward()

    confidence_threshold = 0.7

    for detection in detections[0, 0]:
        confidence = detection[2]

        if confidence > confidence_threshold:
            box = detection[3:7] * np.array([width, height, width, height])
            x_start, y_start, x_end, y_end = map(int, box)
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
            cv2.putText(image, f"Conf: {confidence:.2f}", (x_start, y_start - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Mostrar la imagen
    cv2.imshow("Image", image)
    cv2.waitKey(0)

# Cerrar todas las ventanas al finalizar
cv2.destroyAllWindows()

