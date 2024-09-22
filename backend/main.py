from funcoes import *
from listas import *
import random 

import os
import json

os.chdir("D:/Fiap/projetos/WasteZero-IC/WasteZero--python/external_data")
import json
with open("base_dados.json", 'r') as file:
    base_dados = json.load(file)

#simulação do recebimento de dados da visão computacional

keys_carne = '\n'.join(tipos_carne.keys())
tipo_alimento = forca_opcao(tipos_carne,'Qual o tipo de carne você irá preparar?\n-> ',f'Digite somente se é do tipo: \n\n{keys_carne}')

if tipo_alimento == 'gado' or tipo_alimento == 'peixe':
    formatacao_lista = '\n'.join(tipos_carne[tipo_alimento])
    alimento = forca_opcao(tipos_carne[tipo_alimento], 'Qual o alimento que você irá preparar?\n-> ', f'Digite somente esses: \n\n{formatacao_lista}')

    ultimo_indice = len(base_dados['custo_por_kg']['carne'][tipo_alimento][alimento]) - 1
else:
    alimento = tipo_alimento
    ultimo_indice = len(base_dados['custo_por_kg']['carne'][tipo_alimento]) - 1

preco_kg = base_dados['custo_por_kg']['carne'][tipo_alimento][alimento][ultimo_indice]

#simulação dos pesos medidos (esses dados virão da balança)

valor_min_kg = 1000
valor_max_kg = 7000
peso_bruto = random.randint(valor_min_kg,valor_max_kg)
peso_liquido = random.randint(valor_min_kg,valor_max_kg)

valor_min_g = 30
valor_max_g = 300
peso_corte = random.randint(valor_min_g,valor_max_g)
print(f'\nPeso Bruto: {peso_bruto} g\nPeso Liquído: {peso_liquido} g\nPeso pós corte: {peso_corte} g\nFator de correção: {peso_liquido - peso_corte} g')

#cálculos 

rendimento = calcular_rendimento(peso_bruto,peso_liquido)
preco_unidade = calcular_preco_unidade(peso_bruto,preco_kg)
prejuizo = calcular_prejuizo(peso_bruto, peso_liquido, preco_unidade)
desperdicio = calcular_desperdicio(peso_bruto,peso_liquido)
percentual_desperdicio = desperdicio_percentual(peso_bruto,peso_liquido)

vendido = 114 
preco_kg_restaurante = 42.70
faturamento = calcular_faturamento_real(vendido, preco_kg_restaurante)

faturamento_ideal = calcular_faturamento_ideal(faturamento, prejuizo)



print(f'\nAnálise de dados de {alimento}\n\nRendimento kg: {rendimento:.2f}%\nPrejuízo: {prejuizo:.2f}%\nDesperdício: {desperdicio:.2f} g -> equivalente a {percentual_desperdicio:.2f}%\nFaturamento recebido: R$ {faturamento:.2f}\nFaturamento caso não houvesse desperdício: R$ {faturamento_ideal:.2f}')
