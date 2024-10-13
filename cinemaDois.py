import mysql.connector
import subprocess
import sys #usado para fechar o programa

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Usuário padrão do XAMPP
    password="",  # Deixe em branco se você não configurou uma senha
    database="loginCinema",  # Nome do seu banco de dados
    port=3306  # Porta padrão do MySQL
)
cursor = conn.cursor()

# Função de cadastro de usuário na tabela já existente
def cadastrarUsuario(usuario, senha):
    try:
        # Armazena a senha em texto simples
        cursor.execute('''INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)''', (usuario, senha))
        conn.commit()
        print("Usuário cadastrado com sucesso! Faça o login...")
    except mysql.connector.IntegrityError:
        print("Erro: Usuário já existe.")
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar usuário: {err}")

# Função de login usando a tabela existente
def login(usuario, senha):
    usuario = usuario.strip()  # Remove espaços em branco
    senha = senha.strip()      # Remove espaços em branco
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
    loginCinema = cursor.fetchone()
    
    if loginCinema:
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
            usuario = input("Nome de usuário: ")
            senha = input("Senha (mínimo 4 caracteres): ")
            cadastrarUsuario(usuario, senha)
        elif escolhaMenu == "2":
            usuario = input("Nome de usuário: ")
            senha = input("Senha: ")
            login(usuario, senha)
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
