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

nome = 'manga'
id_categoria = 7
comando = f'INSERT INTO info_alimentos (nome, id_categoria) VALUES ("{nome}", {id_categoria})'
cursor.execute(comando)
conexao.commit()


# # Read

comando = 'SELECT * FROM info_alimentos'
cursor.execute(comando)
dados = cursor.fetchall()

print(dados)


# Update

nome = 'manga'
id_categoria = 10

comando = f'UPDATE info_alimentos SET id_categoria = {id_categoria} WHERE nome = "{nome}"'
cursor.execute(comando)
conexao.commit()


# Delete

id_alimento = 2

comando = f'DELETE FROM info_alimentos WHERE id_alimentos = {id_alimento}'
cursor.execute(comando)
conexao.commit()

cursor.close()
conexao.close()