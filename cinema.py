import subprocess

print("FILMES EM EXIBIÇÃO:")

filme1 ="1- É assim que acaba"
filme2 = "2- Thor"
filme3 = "3- Top gan"

print(filme1)
print(filme2)
print(filme3)

filmeEscolhido = input("Digite o número do filme que quer comprar: ")
if filmeEscolhido == "1":   
    print(filme1)
    confirmado = input("Confirme se o filme acima foi o escolhido (S para sim e N para não)")
    if confirmado == "s" or confirmado =="S":
        subprocess.run(['python', 'cinemaDois.py'])
    elif confirmado == "n" or confirmado =="N":
        subprocess.run(['python', 'cinema.py'])

elif filmeEscolhido == "2":
    print(filme2)
    confirmado = input("Confirme se o filme acima foi o escolhido (S para sim e N para não)")
    if confirmado == "s" or confirmado =="S":
        subprocess.run(['python', 'cinemaDois.py'])
    elif confirmado == "n" or confirmado =="N":
        subprocess.run(['python', 'cinema.py'])


elif filmeEscolhido == "3":
    print(filme2)
    confirmado = input("Confirme se o filme acima foi o escolhido (S para sim e N para não)")
    if confirmado == "s" or confirmado =="S":
        subprocess.run(['python', 'cinemaDois.py'])
    elif confirmado == "n" or confirmado =="N":
        subprocess.run(['python', 'cinema.py'])





