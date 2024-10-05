from funcoes import *
from listas import *
import os
import json
from datetime import datetime

# Definindo o diretório para leitura de dados externos
os.chdir("D:/Fiap/projetos/Visight-IC/WasteZero--python/external_data")

# Carregando dados do arquivo 'infosGerais.json'
with open("infosGerais.json", 'r') as file:
    dados_restaurantes = json.load(file)

# Extraindo os nomes dos alimentos dos dados carregados
dados_externos = []
for alimento in dados_restaurantes["alimentos"]:
    dados_externos.append(alimento["nome"])

# Mudando o diretório para onde o arquivo 'pesos.json' está localizado
os.chdir("D:/Fiap/projetos/Visight-IC/WasteZero--python/database")

# Carregando dados do arquivo 'pesos.json'
with open("pesos.json", 'r') as file:
    dados_internos = json.load(file)

# Lista para armazenar os resultados dos cálculos
dados_resultados = []

# Processamento dos dados internos
for itens in dados_internos:
    analise = itens.copy()  # Cópia dos dados para análise

    # Definindo variáveis
    custo_kg = 0  # Deve ser ajustado conforme necessário
    qnt_kg = 0    # Quantidade em kg (pode ser atualizado)
    preco_venda = 0  # Preço de venda por unidade
    qnt_vendas = 0   # Quantidade de vendas

    # Cálculo do peso líquido e peso pós-corte a partir do peso bruto
    peso_bruto = analise["peso"]
    peso_liquido = peso_bruto - 0.03
    peso_corte = peso_liquido - 0.02
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtendo o timestamp atual

    # Realizando os cálculos
    rendimento = calcular_rendimento(peso_bruto, peso_liquido)
    preco_unidade = calcular_preco_unidade(peso_bruto, custo_kg)
    prejuizo = calcular_prejuizo(peso_bruto, peso_liquido, preco_unidade)
    desperdicio = calcular_desperdicio(peso_bruto, peso_liquido)
    percentual_desperdicio = desperdicio_percentual(peso_bruto, peso_liquido)
    faturamento = calcular_faturamento(qnt_vendas, preco_venda)

    # Armazenando os resultados em um dicionário
    resultado = {
        "alimento": analise["tipo_alimento"],
        "peso_bruto": peso_bruto,
        "peso_liquido": peso_liquido,
        "peso_corte": peso_corte,
        "rendimento": rendimento,
        "prejuizo": prejuizo,
        "desperdicio": desperdicio,
        "percentual_desperdicio": percentual_desperdicio,
        "faturamento": faturamento,
        "timestamp": timestamp
    }

    # Adicionando o resultado à lista
    dados_resultados.append(resultado)

# Salvando os resultados em um novo arquivo JSON
output_file_path = "D:/Fiap/projetos/Visight-IC/WasteZero--python/database/resultados_analise.json"
with open(output_file_path, 'w') as outfile:
    json.dump(dados_resultados, outfile, indent=4)

print(f"Dados processados e armazenados em {output_file_path}")
