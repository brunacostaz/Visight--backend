def meu_in(lista, opcao):
    for i in range(len(lista)):
        if opcao == lista[i]:
            return True
    return False    

def forca_opcao(lista,msg,erro):
    elemento = input(msg)
    while not meu_in(lista, elemento):
        print(erro)
        elemento = input(msg)
    return elemento

def verificar_num(msg):
    num = input(msg)
    while not num.isnumeric():
        print('Digite somente números!')
        num = input(msg)
    num = int(num)
    return num

def calcular_rendimento(bruto,liquido):
    rendimento = (liquido/bruto)*100
    return rendimento

def calcular_prejuizo(peso_bruto,peso_liquido,preco_por_kg):
    custo_peso_bruto = peso_bruto * preco_por_kg
    custo_peso_liquido = peso_liquido * preco_por_kg
    prejuizo = custo_peso_bruto - custo_peso_liquido
    return prejuizo

def calcular_desperdicio(bruto,liquido):
    desperdicio = bruto - liquido
    return desperdicio 

def desperdicio_percentual(bruto,liquido):
    percentual_desperdicio = ((bruto - liquido) / bruto) * 100
    return percentual_desperdicio

