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

def printTitulo(texto):
    largura = len(texto) + 4
    print("-" * largura)  # Usando "_" para o topo
    print(f"| {texto.upper()} |")  # Exibe o texto em maiúsculas
    print("-" * largura)  # Usando "-" para a base
    


def printInput(texto):
    largura = len(texto) + 3
    print("-" * largura)  # Usando "_" para o topo
    print(f" {texto} ")  # Exibe o texto em maiúsculas
    print("-" * largura)  # Usando "-" para a base
    


# Função para exibir os filmes em exibição
def mostraFilmes():
  
    printTitulo("    FILMES EM EXIBIÇÃO:    ")
    
    cursor.execute("SELECT nome, faixaEtaria, matricula FROM filmes")
    filmes = cursor.fetchall()
    for filme in filmes:
        nome, faixaEtaria, matricula = filme
        printFormatado = f"{matricula}- Filme: {nome} | Faixa etária: {faixaEtaria} "
        print(printFormatado)
        print("     ")  # Usando o comprimento da string para a linha de separação

mostraFilmes()

# Função para escolher o filme
def escolherFilme():
    print("       ")
    filmeEscolhido = int(input("DIGITE O NÚMERO DO FILME QUE QUER COMPRAR: "))  # Solicita a entrada do usuário
    cursor.execute("SELECT nome, matricula FROM filmes WHERE matricula = %s", (filmeEscolhido,))
    filme = cursor.fetchone()
    if filme:
        nome, matricula = filme   
        printInput("Confirme se o filme: " f"{nome}" ", foi o escolhido ")
        filmeConfirmado = input("(S para sim e N para não): ").lower()
        if filmeConfirmado == "s":
           
            pilhaEscolha.append({'tipo': 'filme', 'nome': nome, 'codigo': matricula})

        elif filmeConfirmado == "n":
            print("Você optou por não escolher esse filme.")
            escolherFilme()  # Chama a função novamente para escolher outro filme
    else:
        print("Código do filme não encontrado. Tente novamente.")
        escolherFilme()
escolherFilme()

# Função para escolher a sessão
def escolherSessao():
    print("   ")
    printTitulo("   SESSÕES DISPONÍVEIS:   ")
    cursor.execute("SELECT cod, dia, hora, sala FROM sessao")
    sessoes = cursor.fetchall()
    for sessao in sessoes:
        cod, dia, hora, sala = sessao
        print(f"{cod}- Dia: {dia}   |   Hora: {hora}  |  Sala: {sala}")
    printInput("Digite o código da sessão ")
    sessaoEscolhida = input("Sessão escolhida: ").lower()
    cursor.execute("SELECT cod, dia, hora, sala FROM sessao WHERE cod = %s", (sessaoEscolhida,))
    sessao = cursor.fetchone()
 
    pilhaEscolha.append({'tipo': 'sessao', 'codigo': sessaoEscolhida, 'detalhes': sessao})

  
valorTotal = 0  # Inicializa o valor total dos ingressos

def escolherPoltrona():
    print("   ")
    printTitulo("   POLTRONAS DISPONÍVEIS:   ")
    cursor.execute("SELECT num, lado FROM poltrona")
    poltronas = cursor.fetchall()
    for poltrona in poltronas:
        num, lado = poltrona
        print(f"Número: {num}  |  Lado: {lado}")
    poltronasEscolhidas = []

    printInput("Digite o número da poltrona")
    while True:
        
        poltronaEscolhida = input("Poltrona escolhida ou 'c' para continuar: ").lower()
        if poltronaEscolhida.lower() == 'c':
            break
        cursor.execute("SELECT num, lado FROM poltrona WHERE num = %s", (poltronaEscolhida,))
        poltrona = cursor.fetchone()

        if any(p['numero'] == poltronaEscolhida for p in poltronasEscolhidas):    # Verifica se a poltrona já foi selecionada
            print("Poltrona já selecionada, escolha outra!")
        elif poltrona:
            poltronasEscolhidas.append({'tipo': 'poltrona', 'numero': poltronaEscolhida, 'lado': poltrona[1]})
            #print(f"Poltrona {poltronaEscolhida} adicionada.")
        else:
            print("Poltrona inválida ou não disponível. Tente novamente.")     

    pilhaEscolha.extend(poltronasEscolhidas)  # Adiciona todas as escolhas à pilha de uma vez
    print("   ")
    print("Poltronas selecionadas:", [p['numero'] for p in poltronasEscolhidas])

    # Chama escolherIngresso para o número de poltronas selecionadas
    numPoltronas = len(poltronasEscolhidas)
    if numPoltronas > 0:
        print("   ")
        printInput(f"Selecione um tipo de ingresso para cada poltrona:")
        escolherIngresso(numPoltronas)  # Chama a função apenas uma vez com o total de poltronas


# Função para escolher o ingresso
def escolherIngresso(numPoltronas):
    global valorTotal
    valorTotal = 0  # Reinicia o valor total para cada compra de ingressos
    ingressosSelecionados = []

    # Exibe as opções de ingressos disponíveis
    cursor.execute("SELECT mat, tipo, valor FROM ingresso")
    ingressos = cursor.fetchall()
    for ingresso in ingressos:
        mat, tipo, valor = ingresso
        print(f"{mat}- Tipo: {tipo}   |   Valor: {valor}")
        
     # Exibe a instrução de inserir o código do ingresso apenas uma vez
    print("   ")
    printInput("Digite o número do ingresso para cada poltrona:")

    # Solicita o código do ingresso para cada poltrona
    for _ in range(numPoltronas):
        while True:
            escolhaIngresso = input("Número: ")
            cursor.execute("SELECT tipo, valor FROM ingresso WHERE mat = %s", (escolhaIngresso,))
            ingressoEscolhido = cursor.fetchone()

            if ingressoEscolhido:
                tipo, valor = ingressoEscolhido  # Desempacota o tipo e o valor
                print(f"Ingresso escolhido: {tipo}   |   Preço: {valor}")
                valorTotal += valor  # Soma o valor ao total
                ingressosSelecionados.append({'tipo': 'ingresso', 'codigo': escolhaIngresso, 'detalhes': {'tipo': tipo, 'valor': valor}})
                break
            else:
                print("   ")
                print("Ingresso não encontrado. Tente novamente.")

    # Adiciona ingressos à pilhaEscolha e exibe o total ao final
    pilhaEscolha.extend(ingressosSelecionados)
    printTitulo(f"Total: {valorTotal}")
    pilhaEscolha.append({'tipo': 'total', 'valor_total': valorTotal})




# Função de compra que exibe a pilha
def comprar():
    print("\n") 
    printTitulo("   Notinha Ingresso:   ")
    # Abre o arquivo para escrita
    with open("notinha_ingresso.txt", "w") as file:
        file.write("   Notinha Ingresso:   \n")
        file.write("\n")

        for escolha in pilhaEscolha:
            if escolha['tipo'] == 'filme':
                texto = f"Filme: {escolha['codigo']}- {escolha['nome']}\n"
                print(texto.strip())
                file.write(texto)
                
            elif escolha['tipo'] == 'sessao':
                detalhes = escolha['detalhes']
                texto = f"Sessão: {escolha['codigo']}-  Dia: {detalhes[1]}  |   Hora: {detalhes[2]}   |   Sala: {detalhes[3]}\n"
                print(texto.strip())
                file.write(texto)
                
            elif escolha['tipo'] == 'poltrona':
                texto = f"Poltrona: {escolha['numero']}- Lado: {escolha['lado']}\n"
                print(texto.strip())
                file.write(texto)
                
            elif escolha['tipo'] == 'ingresso':
                detalhes = escolha['detalhes']
                texto = f"Ingresso: {escolha['codigo']}- {detalhes['tipo']}   |   Preço: {detalhes['valor']}\n"
                print(texto.strip())
                file.write(texto)
                
            elif escolha['tipo'] == 'total':
                texto = f"Total: {valorTotal}\n"
                print(texto.strip())
                file.write(texto)
    
    print("\nNotinha salva em 'notinha_ingresso.txt'!")





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
        print("   ")
        printTitulo("Login bem-sucedido!")
       # pilhaEscolha.append(("nome: ", nome))
        pilhaEscolha.append({'tipo': 'usuario', 'nome': nome})
        
        escolherSessao()
        escolherPoltrona()
        comprar()
       # escolherIngresso()
    else:
        print("Usuário ou senha incorretos.")
        menu()

# Função de menu
def menu():
    print("\n")
    printTitulo("MENU")
    print("1. Cadastrar novo usuário")
    print("2. Login")
    print("3. Sair")
    escolhaMenu = input("Escolha uma opção: ")
    if escolhaMenu == "1":
        print("   ")
        nome = input("Nome de usuário: ")
        senha = input("Senha: ")
        cadastrarUsuario(nome, senha)
    elif escolhaMenu == "2":
        print("   ")
        nome = input("Nome de usuário: ")
        senha = input("Senha: ")
        login(nome, senha)
    elif escolhaMenu == "3":
        print("   ")
        print("Encerrado.")
        sys.exit()
    else:
        print("   ")
        print("Opção inválida!")
        menu()

# Iniciar o programa chamando o menu
menu()

# Fecha o cursor e a conexão
cursor.close()
conn.close()
