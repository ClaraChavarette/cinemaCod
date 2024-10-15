import mysql.connector
import subprocess
import sys #usado para fechar o programa

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Usuário padrão do XAMPP
    password="",  # Deixe em branco se você não configurou uma senha
    database="cinema_bd",  # Nome do seu banco de dados
    port=3306  # Porta padrão do MySQL
)
cursor = conn.cursor()

# Função de cadastro de usuário na tabela já existente
def cadastrarUsuario(nome, senha):
    try:
        # Armazena a senha em texto simples
        cursor.execute('''INSERT INTO usuarios (nome, senha) VALUES (%s, %s)''', (nome, senha))
        conn.commit()
        print("Usuário cadastrado com sucesso! Faça o login...")
    except mysql.connector.IntegrityError:
        print("Erro: Usuário já existe.")
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar usuário: {err}")

# Função de login usando a tabela existente
def login(nome, senha):
    nome = nome.strip()  # Remove espaços em branco
    senha = senha.strip()      # Remove espaços em branco
    
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (nome, senha))
    cinema_bd = cursor.fetchone()
    
    if cinema_bd:
        print("Login bem-sucedido!")
        subprocess.run(['python', 'cinemaTres.py'])
        return False 
    else:
        print("Usuário ou senha incorretos.")
        menu()

# Menu para interagir com o sistema de login e cadastro
def menu():
        print("\n1. Cadastrar novo usuário")
        print("2. Login")
        print("3. Sair")
        escolhaMenu = input("Escolha uma opção: ")

        if escolhaMenu == "1":
            nome = input("Nome de usuário: ")
            senha = input("Senha (mínimo 4 caracteres): ")
            cadastrarUsuario(nome, senha)
        elif escolhaMenu == "2":
            nome = input("Nome de usuário: ")
            senha = input("Senha: ")
            login(nome, senha)
        elif escolhaMenu == "3":
           print("Encerrado.")
           sys.exit()  # Encerra o programa
        else:
            print("Opção inválida!")
            menu()

# Executa o sistema com a tabela existente
menu()

# Fecha a conexão com o banco de dados
conn.close()
