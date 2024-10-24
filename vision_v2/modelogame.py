import pygame
import cv2
import pygame.freetype
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
import time
from datetime import datetime

# Conexão ESP

import serial
import time
import json
import os
import sys
import asyncio

# Conexão BD

import mysql.connector
import json

conexao = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'amotec',
    database= 'bdvisight'
)

cursor = conexao.cursor()

# Função para inserir dados no banco de dados
def inserirBD(nomeAlimento, liquido, bruto):
    query = f"CALL calcular('{nomeAlimento}', {liquido} , {bruto});"
    cursor.execute(query)
    conexao.commit()
    print(f"Inserido no banco de dados: {nomeAlimento}, {liquido}kg, {bruto}kg")

# Configura a serial para realizar a comunicação
porta = 'COM3'
baud_rate = 115200
comunicacao = serial.Serial(porta, baud_rate)

# Aguardar a estabilização da comunicação
time.sleep(2)
print("Comunicação serial iniciada...")

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
    modelo_carregado = load_model("D:/Fiap/projetos/Visight-IC/WasteZero--python/vision_v2/modeloBruto.h5")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    exit(1)

classes= ['sem fruta', 'maca', 'banana', 'pote']

# Inicia captura da webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro ao abrir a webcam.")
    exit(1)

pesoLiquido = 0
pesoBruto = 0

async def receber_pesoBruto():
    global pesoBruto

    try:
        # Limpa o buffer de entrada para evitar leitura de dados antigos
        comunicacao.reset_input_buffer()
        time.sleep(0.1)
        try:
            validacao = "B"
            comunicacao.write((validacao + '\n' ).encode())
            print(f'Validação enviada!')
            time.sleep(0.1)
        except Exception as e:
            print(f"Erro ao enviar dado para o ESP: {e}")

        if comunicacao.in_waiting > 0:
            # Recebe dados da célula de carga via serial
            pesoBruto = comunicacao.readline().decode('utf-8').strip()
            print(f"Dados recebidos: {pesoBruto}")
        
        try:
            pesoBruto = float(pesoBruto)
        except ValueError:
            print(f"Valor inválido recebido: {pesoBruto}")
            
    except serial.SerialException as e:
        print(f"Erro de comunicação serial: {e}")


async def receber_pesoLiquido():
    global pesoLiquido

    try:
        # Limpa o buffer de entrada para evitar leitura de dados antigos
        comunicacao.reset_input_buffer()
        time.sleep(0.05)
        try:
            validacao = 'L'
            comunicacao.write((validacao + '\n' ).encode())
            print(f'Validação 2 enviada!')
            time.sleep(0.05)
        except Exception as e:
            print(f"Erro ao enviar dado para o ESP: {e}")
            
        if comunicacao.in_waiting > 0:
            # Recebe dados da célula de carga via serial
            pesoLiquido = comunicacao.readline().decode('utf-8').strip()
            print(f"Dados recebidos: {pesoLiquido}")
            
            try:
                pesoLiquido = float(pesoLiquido)
                if pesoLiquido != 0:
                    inserirBD(nome_classe_predita, pesoLiquido, pesoBruto)
            except ValueError:
                print(f"Valor inválido recebido: {pesoLiquido}")
                return
            
            if pesoBruto <= 0 or pesoLiquido <= 0:
                return
                
            
    except serial.SerialException as e:
        print(f"Erro de comunicação serial: {e}")
        return

timer = 30

async def main():
    await asyncio.gather(receber_pesoBruto())
    
async def main2():
    await asyncio.gather(receber_pesoLiquido())


# Inicializa o Pygame
pygame.init()

# Dimensões da tela
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonte para exibir o texto
pygame.freetype.init()
font = pygame.freetype.SysFont(None, 24)

# Inicializa a captura de vídeo da Webcam
cap = cv2.VideoCapture(1)
# Carregar imagem de fundo
background_image = pygame.image.load("vision_v2/VISIGHT.png")

# Função para converter a imagem do OpenCV (BGR) para Pygame (RGB)
def cv2_to_pygame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    return pygame.transform.rotate(frame, -90)

# Cores
ORANGE = (255, 130, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

nome_classe_predita = ""
frutaAnterior = nome_classe_predita
bruto = False

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Preenche o fundo com laranja
    screen.fill(ORANGE)
    # Desenhar a imagem de fundo
    screen.blit(background_image, (0, 0))
    
    # Captura o frame da webcam
    ret, frame = cap.read()
    if ret:
        frame_surface = cv2_to_pygame(frame)
        frame_surface = pygame.transform.scale(frame_surface, (580, 480))
        screen.blit(frame_surface, (150, 230))  # Posiciona a imagem da webcam

    # Desenha as caixas de texto para as informações
    font.render_to(screen, (800, 260), "Verifique sua balança!", WHITE, size=45)
    
    # Campo Alimento
    font.render_to(screen, (800, 360), f"Alimento: {nome_classe_predita}", WHITE,size=40)
    
    # Campo Peso Bruto
    font.render_to(screen, (800, 420), f"Peso Bruto: {pesoBruto}", WHITE, size=40)
    
    # Campo Peso Líquido
    font.render_to(screen, (800, 480), f"Peso Liquido: {pesoLiquido}", WHITE, size=40)

    # Atualiza a tela
    pygame.display.flip()    
    
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

    # Se uma bounding box foi encontrada, desenha na imagem
    if bounding_box is not None:
        x, y, w, h = bounding_box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Desenha o retângulo

    print(timer)
    
    if bruto == False:
        if nome_classe_predita == 'sem fruta':
            timer = 30
    
        elif nome_classe_predita == 'maca' or nome_classe_predita == 'banana':
            timer -= 1
            if timer < 0:
                timer = 30
            elif nome_classe_predita != frutaAnterior:
                timer = 30
                frutaAnterior = nome_classe_predita
                print("timer do peso bruto zerou")
            elif nome_classe_predita == frutaAnterior and confidencia > 0.71 and timer == 0:
                print("entrou peso bruto")
                timer = 30
                # Executa o loop de eventos asyncio
                asyncio.run(main()) 
                while nome_classe_predita != 'sem fruta':
                    # Captura o frame da webcam
                    ret, frame = cap.read()
                    if ret:
                        frame_surface = cv2_to_pygame(frame)
                        frame_surface = pygame.transform.scale(frame_surface, (580, 480))
                        screen.blit(frame_surface, (150, 230))  # Posiciona a imagem da webcam

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

                    # Se uma bounding box foi encontrada, desenha na imagem
                    if bounding_box is not None:
                        x, y, w, h = bounding_box
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Desenha o retângulo
                    
                    if nome_classe_predita == 'sem fruta':
                        bruto = True
                    
                    # Atualiza a tela
                    pygame.display.flip()   
                bruto = True
    else:
        if nome_classe_predita == 'sem fruta':
            timer = 30
    
        elif nome_classe_predita == 'maca' or nome_classe_predita == 'banana':
            timer -= 1
            if timer < 0:
                timer = 30
            elif nome_classe_predita != frutaAnterior:
                timer = 30
                frutaAnterior = nome_classe_predita
                print("timer do peso liquido zerou")
            elif nome_classe_predita == frutaAnterior and confidencia > 0.71 and timer == 0:
                print("entrou peso liquido")
                timer = 30
                # Executa o loop de eventos asyncio
                asyncio.run(main2()) 
                while nome_classe_predita != 'sem fruta':
                    # Captura o frame da webcam
                    ret, frame = cap.read()
                    if ret:
                        frame_surface = cv2_to_pygame(frame)
                        frame_surface = pygame.transform.scale(frame_surface, (580, 480))
                        screen.blit(frame_surface, (150, 230))  # Posiciona a imagem da webcam
                        
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

                    # Se uma bounding box foi encontrada, desenha na imagem
                    if bounding_box is not None:
                        x, y, w, h = bounding_box
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Desenha o retângulo
                    
                    if nome_classe_predita == 'sem fruta':
                        bruto = False
                    # Atualiza a tela
                    pygame.display.flip()  
                bruto = False
    
                
# Libera a captura de vídeo e fecha janelas
cap.release()
pygame.quit()
# Fechar a conexão
conexao.close()
cap.release()
cv2.destroyAllWindows()