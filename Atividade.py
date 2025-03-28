import getpass
import json

# Feito por: BRUNA DA SILVA CARNELOSSI
#         e: EDMUND SOARES DE SOUZA
          

while True:
    # Abre o arquivo usuariosPermissoes.json  
    with open("usuariosPermissoes.json", mode="r") as arquivo:
        permissoes = json.load(arquivo)

    menuInicial = input(f"Bem-vindo \n--------------------------\n [1] - Login\n [2] - Cadastrar \n [3] - Sair\n--------------------------\n")
    
    # Login
    autentificado = False
    tentativas = 0
    if menuInicial == "1":
        login = input("Login: ")
        senha = getpass.getpass("Senha: ")
        if any(permissoes["nome"] == login and permissoes["senha"] == senha for permissoes in permissoes):
            print(f"\n Usuario autenticado parabens {login}\n")
            autentificado = True
            break
                                
        else:
            print("\n Login ou Senha incorretos, por favor tente novamente \n")
            tentativas +=1

        if autentificado == True:
            break
    elif menuInicial == "2":
        print("ok")
    elif menuInicial == "3":
        print("ok")
    else:
        print("esta opcao n existe")

  
                          