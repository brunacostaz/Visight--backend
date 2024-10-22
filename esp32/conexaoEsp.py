import serial
import time
import json
import os
import sys

sys.path.append(os.path.abspath('D:/Fiap/projetos/Visight-IC/WasteZero--python/vision_v2'))
from modelo import reconhecer_alimento

# Configura a serial para realizar a comunicação
porta = 'COM3'
baud_rate = 115200
comunicacao = serial.Serial(porta, baud_rate)

# Aguardar a estabilização da comunicação
time.sleep(2)
print("Comunicação serial iniciada...")

peso_anterior = None
peso_estabilizado = None
estabilizado_por = 0
tempo_espera = 3  # Tempo para considerar que o peso está estabilizado

json_file_path = "D:/Fiap/projetos/Visight-IC/WasteZero--python/database/pesos.json"

# Função para ler o JSON existente ou criar um novo
def ler_arquivo_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, 'r') as file:
            return json.load(file)
    else:
        return []

# Função para gravar os dados no arquivo JSON
def gravar_arquivo_json(caminho, dados):
    with open(caminho, 'w') as file:
        json.dump(dados, file, indent=4)

# Função para filtrar pesos negativos antes de registrar
def filtrar_pesos(peso):
    if peso < 0:
        print(f"Peso negativo detectado: {peso}. Ignorando.")
        return False  # Ignorar peso negativo
    return True  # Peso válido

# Função para enviar alimento identificado ao ESP via serial
def enviar_alimento_para_esp(alimento):
    try:
        validacao = 'Alimento reconhecido'
        comunicacao.write((validacao + '\n' ).encode())
        time.sleep(1)
        print(f'Validação enviada!')
        time.sleep(1)
    except Exception as e:
        print(f"Erro ao enviar dado para o ESP: {e}")


# Loop principal para monitorar o peso e enviar alimento ao ESP
while True:
    try:
        # Limpa o buffer de entrada para evitar leitura de dados antigos
        comunicacao.reset_input_buffer()

        time.sleep(2)
        tipo_alimento = reconhecer_alimento()

        if tipo_alimento == None:
            continue

        time.sleep(2)
        enviar_alimento_para_esp(tipo_alimento)
        
        if comunicacao.in_waiting > 0:
            # Recebe dados da célula de carga via serial
            peso_serial = comunicacao.readline().decode('utf-8').strip()
            print(f"Dados recebidos: {peso_serial}")

            try:
                peso_atual = float(peso_serial)

            except ValueError:
                print(f"Valor inválido recebido: {peso_serial}")
                continue

            # Verifica se o peso é zero 
            if peso_atual == 0:
                print("Peso igual a zero, aguardando nova fruta...")
                peso_anterior = None
                estabilizado_por = 0  # Reseta o contador de estabilização
                continue


    #         # Se houver uma variação significativa no peso, reinicia a estabilização
    #         if peso_anterior is None or abs(peso_atual - peso_anterior) > 3:
    #             estabilizado_por = 0
    #             peso_anterior = peso_atual
    #             print(f'Peso recebido no ESP32: {peso_atual:.2f} kg (variação > 3g)')
    #         else:
    #             estabilizado_por += 1
    #             print(f"Peso estável por {estabilizado_por} leituras")

    #             # Se o peso permanecer estável pelo tempo suficiente, considerar estabilizado
    #             if estabilizado_por > tempo_espera:
    #                 peso_estabilizado = peso_atual
    #                 print(f'Peso estabilizado e computado: {peso_estabilizado:.2f} kg')

    #                 # Verifica se o peso estabilizado é válido (não negativo)
    #                 if filtrar_pesos(peso_estabilizado):
    #                     # Reconhecer o alimento e associá-lo ao peso estabilizado
    #                     tipo_alimento = reconhecer_alimento()

    #                     if tipo_alimento:
    #                         # Envia o alimento identificado para o ESP via serial
    #                         enviar_alimento_para_esp(tipo_alimento)

    #                         # Registro de peso com o nome do alimento
    #                         novo_peso = {
    #                             "peso": peso_estabilizado,
    #                             "tipo_alimento": tipo_alimento,  
    #                             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    #                         }

    #                         # Atualiza o JSON com o alimento e o peso estabilizados
    #                         dados_pesos = ler_arquivo_json(json_file_path)
    #                         dados_pesos.append(novo_peso)

    #                         # Gravar os dados atualizados no JSON
    #                         gravar_arquivo_json(json_file_path, dados_pesos)
    #                         print(f'Peso gravado no arquivo JSON: {peso_estabilizado:.2f} kg, alimento: {tipo_alimento}')
    #                     else:
    #                         print("Nenhum alimento identificado com confiança suficiente.")

    #                 # Reinicia o contador de estabilização para aguardar nova fruta
    #                 estabilizado_por = 0
    #                 peso_anterior = None 

    except serial.SerialException as e:
        print(f"Erro de comunicação serial: {e}")
        break