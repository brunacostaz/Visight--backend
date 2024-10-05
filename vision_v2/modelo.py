'''import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
import time
from datetime import datetime


def encontrar_bounding_box(frame):
    # Converte a imagem para tons de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar um limiar para destacar a fruta
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Encontra os contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Encontra o contorno com a maior área
        maior_contorno = max(contours, key=cv2.contourArea)
        # Retorna a bounding box (x, y, w, h)
        return cv2.boundingRect(maior_contorno)
    
    return None

# Carregando o modelo
try:
    modelo_carregado = load_model("D:/Fiap/projetos/Visight-IC/WasteZero--python/vision_v2/modeloVisao.h5")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    exit(1)

classes= ['sem fruta', 'maca', 'banana']

# Inicia captura da webcam
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Erro ao abrir a webcam.")
    exit(1)

while True:
    # Captura o frame da webcam
    ret, frame = cap.read()

    if not ret:
        print("Erro ao capturar frame da webcam.")
        break

    # Preprocessamento da imagem
    img_resized = cv2.resize(frame, (224, 224))
    img_array = img_to_array(img_resized)
    img_array = img_array.reshape((1, 224, 224, 3))
    img_array = img_array / 255.0  # Normalização

    # Realiza a predição
    try:
        predicao = modelo_carregado.predict(img_array, verbose=0)
    except Exception as e:
        print(f"Erro na predição: {e}")
        break

    # Tenta encontrar a bounding box usando contornos
    bounding_box = encontrar_bounding_box(frame)

    # Obtém a classe predita
    classe_predita = np.argmax(predicao)
    nome_classe_predita = classes[classe_predita]

    # Obtém a probabilidade máxima
    confidencia = np.max(predicao)

    if confidencia > 0.90:
        print(f"Fruta identificada: {nome_classe_predita} (Confiança: {confidencia:.2f})")
        if nome_classe_predita != classes[0]:
            alimento = nome_classe_predita

    # Se uma bounding box foi encontrada, desenha na imagem
    if bounding_box is not None:
        x, y, w, h = bounding_box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Desenha o retângulo

    # Mostra o nome da classe no frame
    cv2.putText(frame, f"Classe predita: {nome_classe_predita}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Exibe o frame atualizado
    cv2.imshow('Webcam', frame)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()'''

import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf

# Carregando o modelo
try:
    modelo_carregado = load_model("D:/Fiap/projetos/Visight-IC/WasteZero--python/vision_v2/modeloVisao.h5")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    exit(1)

classes = ['sem fruta', 'maca', 'banana']

def encontrar_bounding_box(frame):
    """Encontra a bounding box em torno da fruta no frame capturado."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        maior_contorno = max(contours, key=cv2.contourArea)
        return cv2.boundingRect(maior_contorno)
    
    return None

def reconhecer_alimento():    
    # Inicia a captura da webcam
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Erro ao abrir a webcam.")
        return None

    # Captura um único frame
    ret, frame = cap.read()
    cap.release()  # Libera a câmera imediatamente

    if not ret:
        print("Erro ao capturar frame da webcam.")
        return None

    # Preprocessamento da imagem
    img_resized = cv2.resize(frame, (224, 224))
    img_array = img_to_array(img_resized)
    img_array = img_array.reshape((1, 224, 224, 3))
    img_array = img_array / 255.0  # Normalização

    # Realiza a predição
    try:
        predicao = modelo_carregado.predict(img_array, verbose=0)
    except Exception as e:
        print(f"Erro na predição: {e}")
        return None

    # Obtém a classe predita
    classe_predita = np.argmax(predicao)
    nome_classe_predita = classes[classe_predita]

    # Obtém a probabilidade máxima
    confidencia = np.max(predicao)

    # Verifica se a confiança é maior que 90%
    if confidencia > 0.90:
        print(f"Fruta identificada: {nome_classe_predita} (Confiança: {confidencia:.2f})")
        if nome_classe_predita != classes[0]:  # classes[0] = 'sem fruta'
            return nome_classe_predita  # Retorna a classe do alimento

    return None  # Retorna None se a confiança for baixa ou se não há fruta
