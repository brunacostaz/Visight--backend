import cv2
import numpy as np
import tensorflow as tf

# Função para carregar e pré-processar a imagem capturada da câmera
def processar_imagem(frame):
    # Redimensiona a imagem para o tamanho que o modelo espera (224x224)
    img_redimensionada = cv2.resize(frame, (224, 224))
    
    # Normaliza a imagem (valores entre 0 e 1)
    img_normalizada = img_redimensionada / 255.0
    
    # Expande a dimensão para (1, 224, 224, 3), já que o modelo espera um lote (batch)
    img_expandidas = np.expand_dims(img_normalizada, axis=0)
    
    return img_expandidas

# Carrega o modelo pré-treinado no dataset Fruits 360
modelo = tf.keras.models.load_model('keras_model.h5')

# Dicionário para mapear classes do Fruits 360 para seus respectivos nomes
classes_fruits360 = {
    0: 'Banana',
    1: 'Morango',
    2: 'Uva',
    3: 'Laranja',
    4: 'Melancia',
    5: 'Pera',
    6: 'Cereja',
    7: 'Maçã'
}

# Inicializa a captura da câmera
camera = cv2.VideoCapture(1)

# Define um limite de confiança
limite_confianca = 0.5  # Ajuste conforme necessário

while True:
    # Captura o frame atual da câmera
    ret, frame = camera.read()
    
    if not ret:
        print("Falha ao capturar imagem da câmera")
        break
    
    # Processa a imagem capturada
    img_processada = processar_imagem(frame)
    
    # Faz a predição com o modelo pré-treinado
    predicao = modelo.predict(img_processada)
    
    # Obtém a probabilidade máxima
    confidencia = np.max(predicao)
    
    # Encontra o índice da classe com a maior probabilidade
    indice_classe = np.argmax(predicao)
    
    # Mapeia o índice para o nome da fruta
    if confidencia > limite_confianca:
        fruta_identificada = classes_fruits360.get(indice_classe, "Desconhecida")
    else:
        fruta_identificada = "Desconhecida"

    # Exibe a fruta identificada no terminal
    if confidencia > 0.90:
        print(f"Fruta identificada: {fruta_identificada} (Confiança: {confidencia:.2f})")


    # Mostra o frame da câmera com o nome da fruta identificado
    cv2.putText(frame, f'Fruta: {fruta_identificada}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Identificacao de Frutas', frame)
    
    # Aguarda a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
camera.release()
cv2.destroyAllWindows()
