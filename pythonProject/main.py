import cv2
import mediapipe as mp
import pyautogui
from PIL import ImageGrab
import numpy as np

# Iniciar la cámara
camara = cv2.VideoCapture(0)

# Configurar el modelo de Mediapipe para detectar puntos de referencia faciales
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Obtener el tamaño de la pantalla
screen_w, screen_h = pyautogui.size()

# Factor de ampliación para la región de magnificación
magnification_factor = 10

# Bandera para habilitar/deshabilitar la magnificación
magnification_enabled = True

# Definir la región ampliada fuera del bucle
magnified_region = np.zeros((100, 100, 3), dtype=np.uint8)  # Cambia las dimensiones según sea necesario

def on_click(x, y, button, pressed):
    global magnification_enabled

    if button == "middle":
        magnification_enabled = not magnification_enabled

while True:
    # Capturar el fotograma de la cámara
    _, frame = camara.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar el fotograma para detectar puntos de referencia faciales
    output = face_mesh.process(rgb_frame)
    landmarks_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmarks_points:
        landmarks = landmarks_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            # Dibujar un círculo en el punto de referencia facial
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:
                # Mover el cursor del mouse a la posición del punto de referencia facial
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)

                if magnification_enabled:
                    # Definir la región alrededor del cursor del mouse para la magnificación
                    region = np.array(ImageGrab.grab(bbox=(int(screen_x - 150), int(screen_y - 50),
                                                           int(screen_x + 150), int(screen_y + 50))))

                    # Redimensionar la región para crear el efecto de magnificación
                    magnified_region = cv2.resize(region, None, fx=3, fy=3)  # Ajustar el tamaño objetivo

                    # Reemplazar la región original con la región ampliada
                    # region[int(y - 100):int(y + 100), int(x - 100):int(x + 100)] #= magnified_region

    # Mostrar la ventana con el nombre "Control de Mouse"
    cv2.imshow('Control de Mouse', magnified_region)

    # Esperar 1 milisegundo y verificar si se ha presionado una tecla
    cv2.waitKey(1)
