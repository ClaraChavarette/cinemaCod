import mysql.connector

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Usuário padrão do XAMPP
    password="",  # Deixe em branco se você não configurou uma senha
    database="cinema_bd",  # Nome do seu banco de dados
    port=3306  # Porta padrão do MySQL
)
cursor = conn.cursor()



print('funcionou')
