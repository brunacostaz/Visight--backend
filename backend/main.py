from funcoes import *
from listas import *
import random 

import os
import json

os.chdir("D:/Fiap/projetos/Visight-IC/WasteZero--python/external_data")
import json
with open("infosGerais.json", 'r') as file:
    base_dados = json.load(file)

alimentos = base_dados["alimentos"]
#simulação do recebimento de dados da visão computacional

keys_alimentos = []

for alimento in alimentos:
    keys_alimentos.append(alimento["nome"])

keys = '\n'.join(keys_alimentos)

tipo_alimento = input(f'Qual o alimento você irá preparar?\n {keys}\n--> ')

custo_kg = 0
qnt_kg = 0
preco_venda = 0
qnt_vendas = 0
indice_alimento = 0

for i in range(len(alimentos)):
    if tipo_alimento == alimentos[i]["nome"]:
        custo_kg = alimentos[i]["compra"]["custo_kg"]
        qnt_kg = alimentos[i]["compra"]["quantidade_kg"]
        preco_venda = alimentos[i]["venda"]["preco_venda"]
        qnt_vendas = alimentos[i]["venda"]["quantidade_vendas"]
        indice_alimento = i

#simulação dos pesos medidos (esses dados virão da balança)

peso_bruto = random.randint(5000,7000)
peso_liquido = random.randint(1000,4000)

valor_min_g = 30
valor_max_g = 300
peso_corte = random.randint(valor_min_g,valor_max_g)
print(f'\nPeso Bruto: {peso_bruto} g\nPeso Liquído: {peso_liquido} g\nPeso pós corte: {peso_corte} g\nFator de correção: {peso_liquido - peso_corte} g')

#cálculos 

rendimento = calcular_rendimento(peso_bruto,peso_liquido)
preco_unidade = calcular_preco_unidade(peso_bruto,custo_kg)
prejuizo = calcular_prejuizo(peso_bruto, peso_liquido, preco_unidade)
desperdicio = calcular_desperdicio(peso_bruto,peso_liquido)
percentual_desperdicio = desperdicio_percentual(peso_bruto,peso_liquido)
faturamento = calcular_faturamento(qnt_vendas, preco_venda)

print(f'\nAnálise de dados de {alimentos[indice_alimento]["nome"]}\n\nPeso Bruto: {peso_bruto}\nPeso liquído: {peso_liquido}\nPeso final: {peso_corte}\nRendimento kg: {rendimento:.2f}%\nPrejuízo: {prejuizo:.2f}%\nDesperdício: {desperdicio:.2f} g -> equivalente a {percentual_desperdicio:.2f}%\nFaturamento recebido: R$ {faturamento:.2f}')
