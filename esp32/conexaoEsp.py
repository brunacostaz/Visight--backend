import serial
import time
import json
import os

# Configura a serial para realizar a comunicação
porta = 'COM3'  # Verifique se está correta para o seu sistema
transmissao = 115200  # Baud rate, verifique se é o mesmo usado pelo ESP32
comunicacao = serial.Serial(porta, transmissao)

# Aguardar a estabilização da comunicação
time.sleep(2)
print("Comunicação serial iniciada...")

peso_anterior = None  # Variável para armazenar o peso anterior
peso_estabilizado = None  # Variável para armazenar o peso estabilizado
peso_computado = False  # Flag para indicar se o peso já foi computado
estabilizado_por = 0  # Contador para rastrear quanto tempo o peso está estabilizado
tempo_espera = 3  # Tempo em segundos que o peso deve estar estabilizado

# Arquivo JSON onde os pesos serão salvos
json_file_path = "pesos.json"

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

# Loop principal
while True:
    try:
        # Limpa o buffer de entrada para evitar leitura de dados antigos
        comunicacao.reset_input_buffer()

        # Verifica se há dados disponíveis na serial
        if comunicacao.in_waiting > 0:
            # Lê os dados da serial
            peso_serial = comunicacao.readline().decode('utf-8').strip()
            print(f"Dados recebidos: {peso_serial}")  # Debug para ver o que está sendo recebido

            try:
                # Converte o valor recebido em um float
                peso_atual = float(peso_serial)

                # Ignora valores de peso iguais a zero
                if peso_atual == 0:
                    print("Peso igual a zero, ignorado.")
                    continue

            except ValueError:
                # Se não for possível converter para float, ignora
                print(f"Valor inválido recebido: {peso_serial}")
                continue  # Ignora iterações com dados inválidos

            # Verifica se o peso está estabilizado
            if peso_anterior is None or abs(peso_atual - peso_anterior) > 5:
                # Se o peso atual mudou significativamente, reseta o contador e flag
                estabilizado_por = 0
                peso_computado = False  # Permite que o peso seja computado novamente
                peso_anterior = peso_atual  # Atualiza o peso anterior
                print(f'Peso recebido no ESP32: {peso_atual:.2f} kg (variação > 5g)')
            else:
                # O peso está estabilizado
                estabilizado_por += 1
                print(f"Peso estável por {estabilizado_por} leituras")

                if estabilizado_por >= tempo_espera and not peso_computado:
                    peso_estabilizado = peso_atual
                    print(f'Peso estabilizado e computado: {peso_estabilizado:.2f} kg')  # Exibe o peso estabilizado
                    # Marca que o peso foi computado para não computar novamente
                    peso_computado = True

                    # Ler o arquivo JSON existente
                    dados_pesos = ler_arquivo_json(json_file_path)

                    # Novo registro de peso
                    novo_peso = {
                        "peso": peso_estabilizado,
                        "tipo_alimento": "fruta",  # Este valor pode ser substituído com base no reconhecimento da visão
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")  # Marca de tempo
                    }

                    # Adiciona o novo peso estabilizado à lista de dados
                    dados_pesos.append(novo_peso)

                    # Grava os dados atualizados no arquivo JSON
                    gravar_arquivo_json(json_file_path, dados_pesos)

                    print(f'Peso gravado no arquivo JSON: {peso_estabilizado:.2f} kg')

                    estabilizado_por = 0  # Reseta o contador após computar

            # Exibe peso atual sem armazenar se ainda não foi estabilizado
            if not peso_computado:
                print(f'Peso atual: {peso_atual:.2f} kg (não estabilizado)')

    except serial.SerialException as e:
        print(f"Erro de comunicação serial: {e}")
        break  # Encerra o loop em caso de erro de comunicação
