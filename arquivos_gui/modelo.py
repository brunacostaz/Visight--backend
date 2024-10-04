import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
print(tf.__version__)


# Carregando o modelo
try:
    modelo_carregado = load_model("keras_model.h5")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    exit(1)

# Lista de classes (certifique-se de que elas estão na ordem correta do modelo)
classes_cifar10 = ['maçã', 'banana', 'manga', 'melancia', 'cereja', 
                   'morango', 'abacaxi', 'abacate', 'laranja', 'kiwi', 
                   'alface', 'uva', 'cenoura']

# Inicia captura da webcam
cap = cv2.VideoCapture(0)
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

    # Obtém a classe predita
    classe_predita = np.argmax(predicao)
    nome_classe_predita = classes_cifar10[classe_predita]

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
cv2.destroyAllWindows()
