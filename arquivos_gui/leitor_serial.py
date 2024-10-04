import time
import serial

def ler_dados_serial(porta, baud_rate):
    try:
        # Abrindo a conexão serial
        ser = serial.Serial(porta, baud_rate, timeout=1)
        print(f"Conectado à porta {porta} com baud rate {baud_rate}")

        pesos_frutas = []  # Array para armazenar os pesos das frutas

        while True:
            fruta = input("Digite o nome da fruta (ou 'sair' para encerrar): ").strip()
            if fruta.lower() == 'sair':
                break  # Sai do loop se o usuário digitar 'sair'

            print(f"Aguardando o peso da fruta: {fruta}...")
            if ser.in_waiting > 0:
                # Lendo linha da porta serial
                linha = ser.readline().decode('utf-8').strip()
                if linha:
                    print(f"Peso da {fruta}: {linha} kg")
                    pesos_frutas.append((fruta, float(linha)))  # Adiciona a fruta e seu peso ao array

            time.sleep(0.1)  # Pequeno delay para evitar sobrecarga de processamento

    except serial.SerialException as e:
        print(f"Erro ao acessar a porta serial: {e}")
    except KeyboardInterrupt:
        print("\nEncerrando a leitura de dados.")
    except ValueError:
        print("Erro ao converter o peso para float. Verifique se os dados são válidos.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Conexão serial fechada.")

        # Exibir todos os pesos coletados
        print("\nPesos coletados:")
        for fruta, peso in pesos_frutas:
            print(f"{fruta}: {peso} kg")

if __name__ == "__main__":
    # Exemplo de uso: substitua "COM10" pela porta correspondente no seu sistema
    porta_serial = "COM10"  # Verifique a porta correta
    baud_rate = 115200       # Mesmo baud rate configurado no ESP32

    ler_dados_serial(porta_serial, baud_rate)
