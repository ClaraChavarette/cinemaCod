import subprocess
import mysql.connector
import sys  # Adicione isso no topo


# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Usuário padrão do XAMPP
    password="",  # Deixe em branco se você não configurou uma senha
    database="cinema_bd",  # Nome do seu banco de dados
    port=3306  # Porta padrão do MySQL
)
cursor = conn.cursor()

#criando a pillha para salvar as escolhas do usuario
pilhaEscolha = []


def mostraFilmes():
    print("FILMES EM EXIBIÇÃO:")

    # Executa a consulta para selecionar todos os filmes
    cursor.execute("SELECT nome, faixaEtaria, matricula FROM filmes")
    filmes = cursor.fetchall()  # Pega todas as linhas retornadas pela consulta

    # Itera sobre os resultados e imprime as informações dos filmes
    for filme in filmes:
        nome, faixaEtaria, matricula = filme
        print(f"Filme: {nome}")
        print(f"Faixa etária: {faixaEtaria}")
        print(f"Código: {matricula}")
        print("-----")  # Separador para cada filme

# Chama a função para exibir os filmes
mostraFilmes()








def escolherPoltrona():
    print("POLTRONAS DISPONIVEIS:")
    # Executa a consulta para selecionar todos os filmes
    cursor.execute("SELECT num, lado FROM poltrona")
    poltrona = cursor.fetchall()  # Pega todas as linhas retornadas pela consulta

    # Itera sobre os resultados e imprime as informações dos filmes
    for poltrona in poltrona:
        num, lado  = poltrona
        print(f"Número: {num}")
        print(f"Lado: {lado}")
        print("-----")  # Separador para cada filme

    poltronaEscolhida = input("Digite o número da poltrona que quer sentar: ")
    # Executa a consulta para selecionar a sesao baseado no código 
    cursor.execute("SELECT num, lado FROM poltrona WHERE num = %s", (poltronaEscolhida,))
    sessao = cursor.fetchone()
    pilhaEscolha.append((poltronaEscolhida))



def escolherSessao():

    print("SESSÕES DISPONIVEIS:")
    # Executa a consulta para selecionar todos os filmes
    cursor.execute("SELECT cod, dia, hora, sala FROM sessao")
    sessao = cursor.fetchall()  # Pega todas as linhas retornadas pela consulta

    # Itera sobre os resultados e imprime as informações dos filmes
    for sessao in sessao:
        cod, dia, hora, sala  = sessao
        print(f"Código da sessão: {cod}")
        print(f"Horário: {hora}")
        print(f"Dia: {dia}")
        print(f"Sala: {sala}")
        print("-----")  # Separador para cada filme

    sessaoEscolhida = input("Digite o código da sessão que quer comprar: ")
    # Executa a consulta para selecionar a sesao baseado no código 
    cursor.execute("SELECT cod, dia, hora, sala FROM sessao WHERE cod = %s", (sessaoEscolhida,))
    sessao = cursor.fetchone()
    pilhaEscolha.append((sessaoEscolhida))




    
def escolherIngresso():
    cursor.execute("SELECT mat, tipo, valor FROM ingresso")
    ingressos = cursor.fetchall()  # Pega todas as linhas

    for ingresso in ingressos:
        mat, tipo, valor = ingresso
        print(f"Ingresso: {tipo}")
        print(f"Código: {mat}")
        #print(f"Preço: {valor}")
        print("-----")  # Separador para cada ingresso

    escolhaIngresso = input("Digite o código da matrícula do ingresso que quer comprar: ")
    
    # Aqui você deve converter para inteiro se for comparar com número
    if (escolhaIngresso) == "0":
        print(f"Preço do ingresso com matrícula 0: {valor}")
    elif (escolhaIngresso) == "1":
        print(f"Preço do ingresso com matrícula 1: {valor}")

    pilhaEscolha.append((escolhaIngresso))


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



def escolherFilme():
    filmeEscolhido = int(input("Digite o código do filme que quer comprar: "))

    # Executa a consulta para selecionar o filme baseado no código (matricula)
    cursor.execute("SELECT nome, matricula FROM filmes WHERE matricula = %s", (filmeEscolhido,))
    filmes = cursor.fetchone()

     # Verifica se o filme existe
    if filmes:
        nome, matricula = filmes
        print(f"Filme: {nome}")
        
        filmeConfirmado = input("Confirme se o filme acima foi o escolhido (S para sim e N para não): ").lower()
        if filmeConfirmado == "s":
            pilhaEscolha.append(filmeEscolhido)
            menu()
        elif filmeConfirmado == "n":
            print("Você optou por não escolher esse filme.")
            escolherFilme()  # Chama a função novamente para escolher outro filme
    else:
        print("Código do filme não encontrado. Tente novamente.")
        escolherFilme()

escolherFilme()



# Função de cadastro de usuário na tabela já existente
def cadastrarUsuario(nome, senha):
    try:
        # Armazena a senha em texto simples
        cursor.execute('''INSERT INTO usuarios (nome, senha) VALUES (%s, %s)''', (nome, senha))
        conn.commit()
        print("Usuário cadastrado com sucesso! Faça o login...")
        menu()
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
        pilhaEscolha.append((nome,senha ))
        escolherSessao()
        escolherPoltrona()
        escolherIngresso()
      
        return False 
    else:
        print("Usuário ou senha incorretos.")
        menu()















# Fecha o cursor e a conexão
cursor.close()
conn.close()

    
