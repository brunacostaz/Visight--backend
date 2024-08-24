from funcoes import *
from listas import *
import random 

# Estrutura do código
# pede os inputs para o usuário do alimento, tipo de corte e valor pago 
# recebe os peços do arduino do alimento bruto e do alimento liquido
# realiza os cálculos do fator de correção, rentabilidade, prejuízos, desperdício

tipo_alimento = forca_opcao(categoria_alimento,'Qual o tipo de alimento que você irá preparar? (carne/vegetal)\n-> ','Digite somente se o alimento é vegetal ou carne')
alimento = input('Qual o alimento que você irá preparar? (ex: picanha, cenoura...)\n-> ')
preco_kg = verificar_num('Qual o valor pago pelo kg? ')

valor_min_kg = 1000
valor_max_kg = 7000
peso_bruto = random.randint(valor_min_kg,valor_max_kg)
peso_liquido = random.randint(valor_min_kg,valor_max_kg)

valor_min_g = 30
valor_max_g = 300
peso_corte = random.randint(valor_min_g,valor_max_g)
print(f'Peso Bruto: {peso_bruto} g\nPeso Liquído: {peso_liquido} g\nPeso pós corte: {peso_corte} g')


rendimento = calcular_rendimento(peso_bruto,peso_liquido)
preco_unidade = calcular_preco_unidade(peso_bruto,preco_kg)
prejuizo = calcular_prejuizo(peso_bruto, peso_liquido, preco_unidade)
desperdicio = calcular_desperdicio(peso_bruto,peso_liquido)
percentual_desperdicio = desperdicio_percentual(peso_bruto,peso_liquido)


print(f'\nAnálise de dados\n\nRendimento: {rendimento:.2f}%\nPrejuízo: {prejuizo:.2f}%\nDesperdício: {desperdicio:.2f} g - equivalente a {percentual_desperdicio:.2f}%')
