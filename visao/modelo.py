# módulo do OpenCV usado para a captura de vídeo da webcam
import cv2

# função da biblioteca Keras (dentro do tensorflow) para carregar um modelo treinado carregado em um arquivo
from tensorflow.keras.models import load_model

# usado para abrir e manipular imagens - irá converter e redimensionar a imagem para o formato correto para o modelo
from PIL import Image, ImageOps  

# usado para transformar a imagem em uma estrutura de dados númericos (array, matrizes)
import numpy as np

# desativa a notação científica ao exibir valores númericos
np.set_printoptions(suppress=True)

# carrega o modelo
model = load_model("visao/keras_model.h5", compile=False)

# carrega as classes que o modelo foi treinado para reconhecer
class_names = open("classes.txt", "r").readlines()

# np.ndarray() cria um array vazio, onde a imagem será armazenada para ser passada ao modelo
# as especificações do shape() para o array são:
# 1 -> significa que será processada uma imagem por vez
# 224, 224 (pixels) -> refere-se ao tamanho da imagem que o modelo foi treinado para reconhecer
# 3 -> refere-se aos canais de cor (RGB nesse caso)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Inicializar a webcam
cap = cv2.VideoCapture(0)

# captura a imagem da webcam
# ret é um booleano que indica se a captura foi bem-sucedida
# frame é a imagem capturada, representada como um array numpy
ret, frame = cap.read()

# Verificar se a captura foi bem-sucedida
if ret:
    # Converter o frame (imagem) em um objeto Image do PIL
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # redimenciona a imagem para o tamanho esperado (224x224 pixels) e corta o excesso, se necessário
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # transforma a imagem em um array numérico 
    image_array = np.asarray(image)

    # normaliza a imagem para um intervalo de -1 a 1, convertendo os valores dos pixels de 0 a 255 para -1 a 1, pois foi o que o modelo foi treinado
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # carrega a imagem dentro do array criado anteriormente
    data[0] = normalized_image_array

    # passa a imagem processada (array) para o modelo e obtém as previsões
    # o modelo retorna um array de probabilidades, onde cada posição corresponde à probabilidade de uma imagem pertencer a uma classe especifica  
    prediction = model.predict(data)

    # np.argmax() encontra o indice da classe com a maior probabilidade
    index = np.argmax(prediction)

    # armazena o nome da classe a partir do indice encontrado
    class_name = class_names[index]

    # obtem a probabilidade associada à classe prevista
    confidence_score = prediction[0][index]

    # exibe a classe com maior probabilidade
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

# Libera a câmera
cap.release()

