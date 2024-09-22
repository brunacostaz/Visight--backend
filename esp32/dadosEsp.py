import serial
import time

# configura a serial para realizar a comunicação
porta = 'COM3'
transmissao = 115200
comunicacao = serial.Serial(porta, transmissao)

time.sleep(2)

while True:
    # verifica quantos bytes de dados estão disponíveis na serial para serem lidos
    if comunicacao.in_waiting > 0:
        # lê uma linha inteira da serial, decodifica a informação em bytes para string e limpa os espaços em branco
        peso = comunicacao.readline().decode('utf-8').strip()
        print(f'Peso: {peso}')

    time.sleep(1)



