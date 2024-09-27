def calcular_rendimento(bruto,liquido):
    rendimento = (liquido/bruto)*100
    return rendimento

def calcular_preco_unidade(bruto,valor):
    preco_unidade = valor / bruto
    return preco_unidade

def calcular_prejuizo(peso_bruto,peso_liquido,preco_por_unidade):
    custo_peso_bruto = peso_bruto * preco_por_unidade
    custo_peso_liquido = peso_liquido * preco_por_unidade
    qtd_desperdicio = custo_peso_bruto - custo_peso_liquido
    prejuizo = qtd_desperdicio * preco_por_unidade
    return prejuizo

def calcular_desperdicio(bruto,liquido):
    desperdicio = bruto - liquido
    return desperdicio 

def desperdicio_percentual(bruto,liquido):
    percentual_desperdicio = ((bruto - liquido) / bruto) * 100
    return percentual_desperdicio

def calcular_faturamento(qnt_vendida, preco_cobrado):
    return qnt_vendida * preco_cobrado

def calcular_faturamento_ideal(faturamento, perda):
    return faturamento + perda

