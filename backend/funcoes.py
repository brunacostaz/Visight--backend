def calcular_rendimento(bruto,liquido):
    return (liquido/bruto)*100

def calcular_preco_unidade(bruto,valor):
    return valor / bruto

def calcular_prejuizo(peso_bruto,peso_liquido,preco_por_unidade):
    custo_peso_bruto = peso_bruto * preco_por_unidade
    custo_peso_liquido = peso_liquido * preco_por_unidade
    qtd_desperdicio = custo_peso_bruto - custo_peso_liquido

    return qtd_desperdicio * preco_por_unidade

def calcular_desperdicio(bruto,liquido):
    return bruto - liquido

def desperdicio_percentual(bruto,liquido):
    return ((bruto - liquido) / bruto) * 100

def calcular_faturamento(qnt_vendida, preco_cobrado):
    return qnt_vendida * preco_cobrado

def rentabilidade(preco_venda_prato, peso_final, custo_kg):
    return preco_venda_prato - (peso_final * custo_kg)

