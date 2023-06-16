import cv2  # Importa el módulo para el procesamiento de imágenes y video.
import mediapipe as mp  # Importa el módulo para el reconocimiento de manos.
import pyautogui  # Importa el módulo para controlar el mouse y el teclado.

cap = cv2.VideoCapture(0)  # Crea un objeto para capturar el video de la cámara.
hand_detector = mp.solutions.hands.Hands()  # Crea un objeto para detectar las manos.
drawing_utils = mp.solutions.drawing_utils  # Crea un alias para el módulo de dibujo.

screen_width, screen_height = pyautogui.size()  # Obtiene las dimensiones de la pantalla.

index_y = 0  # Inicializa la variable index_y con 0.

while True:  # Inicia un bucle infinito.

    _, frame = cap.read()  # Lee un cuadro de video de la cámara.
    frame = cv2.flip(frame, 1)  
    frame_height, frame_width, _ = frame.shape  # Obtiene las dimensiones del cuadro de video.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convierte el cuadro a formato RGB
    output = hand_detector.process(rgb_frame)  # Procesa el cuadro para detectar las manos.
    hands = output.multi_hand_landmarks  # Obtiene las coordenadas de los puntos de referencia de las manos.
    if hands:  # Si se detectaron manos:

        for hand in hands:  # Para cada mano detectada:
            drawing_utils.draw_landmarks(frame, hand)  # Dibuja los puntos de referencia de la mano en el cuadro.
            landmarks = hand.landmark  # Obtiene los puntos de referencia de la mano.

            for id, landmark in enumerate(landmarks):  # Para cada punto de referencia:
                x = int(landmark.x * frame_width)  # Obtiene la coordenada x del punto y la ajusta al tamaño del cuadro.
                y = int(landmark.y * frame_height)  # Obtiene la coordenada y del punto y la ajusta al tamaño del cuadro.

                if id == 8:  # Si es el punto de referencia del dedo índice:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))  # Dibuja un círculo en el punto.
                    index_x = screen_width / frame_width * x  # Calcula la posición x en la pantalla.
                    index_y = screen_height / frame_height * y  # Calcula la posición y en la pantalla.

                if id == 4:  # Si es el punto de referencia del pulgar:

                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))  # Dibuja un círculo en el punto.

                    thumb_x = screen_width / frame_width * x  # Calcula la posición x del pulgar en la pantalla.
                    thumb_y = screen_height / frame_height * y  # Calcula la posición y del pulgar en la pantalla.

                    print('outside', abs(index_y - thumb_y))  # Imprime la diferencia entre las posiciones y de los dedos.

                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)