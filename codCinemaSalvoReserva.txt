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

# Criando a pilha para salvar as escolhas do usuário
pilhaEscolha = []

# Função para exibir os filmes em exibição
def mostraFilmes():
    print("FILMES EM EXIBIÇÃO:")
    cursor.execute("SELECT nome, faixaEtaria, matricula FROM filmes")
    filmes = cursor.fetchall()
    for filme in filmes:
        nome, faixaEtaria, matricula = filme
        print(f"Filme: {nome}")
        print(f"Faixa etária: {faixaEtaria}")
        print(f"Código: {matricula}")
        print("-----")
mostraFilmes()

# Função para escolher o filme
def escolherFilme():
    filmeEscolhido = int(input("Digite o código do filme que quer comprar: "))
    cursor.execute("SELECT nome, matricula FROM filmes WHERE matricula = %s", (filmeEscolhido,))
    filme = cursor.fetchone()
    if filme:
        nome, matricula = filme
        print(f"Filme: {nome}")
        filmeConfirmado = input("Confirme se o filme acima foi o escolhido (S para sim e N para não): ").lower()
        if filmeConfirmado == "s":
            #pilhaEscolha.append(filmeEscolhido)
            pilhaEscolha.append({'tipo': 'filme', 'nome': nome, 'codigo': matricula})
            print("Filme selecionado")
        elif filmeConfirmado == "n":
            print("Você optou por não escolher esse filme.")
            escolherFilme()  # Chama a função novamente para escolher outro filme
    else:
        print("Código do filme não encontrado. Tente novamente.")
        escolherFilme()
escolherFilme()

# Função para escolher a sessão
def escolherSessao():
    print("SESSÕES DISPONÍVEIS:")
    cursor.execute("SELECT cod, dia, hora, sala FROM sessao")
    sessoes = cursor.fetchall()
    for sessao in sessoes:
        cod, dia, hora, sala = sessao
        print(f"Código: {cod}, Dia: {dia}, Hora: {hora}, Sala: {sala}")
    sessaoEscolhida = input("Digite o código da sessão: ")
    cursor.execute("SELECT cod, dia, hora, sala FROM sessao WHERE cod = %s", (sessaoEscolhida,))
    sessao = cursor.fetchone()
    #pilhaEscolha.append(sessaoEscolhida)
    pilhaEscolha.append({'tipo': 'sessao', 'codigo': sessaoEscolhida, 'detalhes': sessao})

# Função para escolher a poltrona
def escolherPoltrona():
    print("POLTRONAS DISPONÍVEIS:")
    cursor.execute("SELECT num, lado FROM poltrona")
    poltronas = cursor.fetchall()
    for poltrona in poltronas:
        num, lado = poltrona
        print(f"Número: {num}, Lado: {lado}")
    poltronaEscolhida = input("Digite o número da poltrona: ")
    cursor.execute("SELECT num, lado FROM poltrona WHERE num = %s", (poltronaEscolhida,))
    poltrona = cursor.fetchone()
    #pilhaEscolha.append(poltronaEscolhida)
    pilhaEscolha.append({'tipo': 'poltrona', 'numero': poltronaEscolhida, 'lado': poltrona[1]})

# Função para escolher o ingresso
def escolherIngresso():
    cursor.execute("SELECT mat, tipo, valor FROM ingresso")
    ingressos = cursor.fetchall()
    for ingresso in ingressos:
        mat, tipo, valor = ingresso
        print(f"Ingresso: {tipo}, Código: {mat}")
    escolhaIngresso = input("Digite o código do ingresso: ")

    # Executa a consulta para obter o ingresso escolhido e seu valor
    cursor.execute("SELECT tipo, valor FROM ingresso WHERE mat = %s", (escolhaIngresso,))
    ingressoEscolhido = cursor.fetchone()  # Pega o ingresso escolhido

    if ingressoEscolhido:
        tipo, valor = ingressoEscolhido  # Desempacota o tipo e o valor
        print(f"Preço do ingresso: {valor}")  # Exibe o preço do ingresso

        confirmaPreco = input("Continuar? (s/n) ")
        if confirmaPreco == "s":
            #pilhaEscolha.append(escolhaIngresso)
            pilhaEscolha.append({'tipo': 'ingresso', 'codigo': escolhaIngresso, 'detalhes': {'tipo': tipo, 'valor': valor}})
            comprar()
        elif confirmaPreco == "n":
            print("Você optou por não continuar, escolha novamente")
            escolherIngresso() 
    else:
        print("Ingresso não encontrado. Tente novamente.")
        escolherIngresso()  # Chama a função novamente se o ingresso não for encontrado
    


# Função de compra que exibe a pilha
#def comprar():
  # print("\nResumo da compra:")
    #print("Você escolheu:")
   # for escolha in pilhaEscolha:
        #print(f"- {escolha}")  # Exibe cada escolha da pilha

# Função de compra que exibe a pilha
def comprar():
    print("\nResumo da compra:")
    for escolha in pilhaEscolha:     #escolha é = i
        if escolha['tipo'] == 'filme':
            print(f"Filme escolhido: {escolha['nome']} (Código: {escolha['codigo']})")
        elif escolha['tipo'] == 'sessao':
            detalhes = escolha['detalhes']
            print(f"Sessão escolhida: {detalhes[0]} (Código: {escolha['codigo']}), Dia: {detalhes[1]}, Hora: {detalhes[2]}, Sala: {detalhes[3]}")
        elif escolha['tipo'] == 'poltrona':
            print(f"Poltrona escolhida: {escolha['numero']} (Lado: {escolha['lado']})")
        elif escolha['tipo'] == 'ingresso':
            detalhes = escolha['detalhes']
            print(f"Ingresso escolhido: {detalhes['tipo']} (Código: {escolha['codigo']}), Preço: {detalhes['valor']}")





# Função de cadastro de usuário
def cadastrarUsuario(nome, senha):
    try:
        cursor.execute('''INSERT INTO usuarios (nome, senha) VALUES (%s, %s)''', (nome, senha))
        conn.commit()
        print("Usuário cadastrado com sucesso!")
        menu()
    except mysql.connector.IntegrityError:
        print("Erro: Usuário já existe.")
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar usuário: {err}")

# Função de login
def login(nome, senha):
    nome = nome.strip()
    senha = senha.strip()
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s AND senha = %s", (nome, senha))
    usuario = cursor.fetchone()
    if usuario:
        print("Login bem-sucedido!")
       # pilhaEscolha.append(("nome: ", nome))
        pilhaEscolha.append({'tipo': 'usuario', 'nome': nome})
        
        escolherSessao()
        escolherPoltrona()
        escolherIngresso()
    else:
        print("Usuário ou senha incorretos.")
        menu()

# Função de menu
def menu():
    print("\n1. Cadastrar novo usuário")
    print("2. Login")
    print("3. Sair")
    escolhaMenu = input("Escolha uma opção: ")
    if escolhaMenu == "1":
        nome = input("Nome de usuário: ")
        senha = input("Senha: ")
        cadastrarUsuario(nome, senha)
    elif escolhaMenu == "2":
        nome = input("Nome de usuário: ")
        senha = input("Senha: ")
        login(nome, senha)
    elif escolhaMenu == "3":
        print("Encerrado.")
        sys.exit()
    else:
        print("Opção inválida!")
        menu()

# Iniciar o programa chamando o menu
menu()







# Fecha o cursor e a conexão
cursor.close()
conn.close()
