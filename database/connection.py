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
def inserir_dados_no_banco(peso, alimento, timestamp):
    query = "INSERT INTO tabela_alimentos (peso, alimento, timestamp) VALUES (%s, %s, %s)"
    valores = (peso, alimento, timestamp)
    cursor.execute(query, valores)
    conexao.commit()
    print(f"Inserido no banco de dados: {peso}kg, {alimento}, {timestamp}")

# Função para ler o arquivo JSON e inserir os dados no MySQL
def ler_json_inserir_mysql():
    json_file_path = "D:/Fiap/projetos/Visight-IC/WasteZero--python/database/pesos.json"
    
    with open(json_file_path, 'r') as file:
        dados = json.load(file)

        for registro in dados:
            peso = registro["peso"]
            alimento = registro["alimento"]
            timestamp = registro["timestamp"]
            
            # Inserir cada registro no banco de dados
            inserir_dados_no_banco(peso, alimento, timestamp)

# Chamar a função para ler o JSON e inserir os dados no banco
ler_json_inserir_mysql()

# Fechar a conexão
conexao.close()
