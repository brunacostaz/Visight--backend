import mysql.connector

conexao = mysql.connector.connect(
    host= 'localhost',
    user= 'root',
    password= 'amotec',
    database= 'bdvisight'
)

cursor = conexao.cursor()

# CRUD

# comando = '' # cria um comando SQL
# cursor.execute(comando) # executa o comando 
# conexao.commit() # se for um comando de edição (Create, Update ou Delete), precisa dar commit
# dados = cursor.fetchall() # se for um comando de leitura (Read), precisa de um fetchall() para pegar as informações e armazenar no código

# Create

# nome = 'manga'
# id_categoria = 7
# comando = f'INSERT INTO info_alimentos (nome_alimento) VALUES ("{nome}")'
# cursor.execute(comando)
# conexao.commit()


 # Read

alimento = 'manga'

comando = f'SELECT id_alimentos FROM info_alimentos WHERE nome_alimento = "{alimento}" ORDER BY id_alimentos DESC LIMIT 1'
cursor.execute(comando)
id_encontrado = cursor.fetchone()

if id_encontrado:
    id_alimento = id_encontrado[0]
else:
    print('Nenhum dado encontrado')

print(id_alimento)


# # Update

peso_bruto = 100

comando = f'UPDATE info_alimentos SET peso_bruto = {peso_bruto} WHERE id_alimentos = "{id_alimento}"'
cursor.execute(comando)
conexao.commit()


# Delete

# id_alimento = 3

# comando = f'DELETE FROM info_alimentos WHERE id_alimentos = {id_alimento}'
# cursor.execute(comando)
# conexao.commit()

# cursor.close()
# conexao.close()