import getpass
import json
import os

# Feito por: BRUNA DA SILVA CARNELOSSI
#         e: EDMUND SOARES DE SOUZA     


def menuOpcoes(login, autentificado):
    with open("usuariosPermissoes.json", mode="r") as arquivo:
            permissoes = json.load(arquivo)
    usuarioAutenticado = next((usuario for usuario in permissoes if usuario["login"] == login), None)
    permissoesDoUsuario = usuarioAutenticado["permissoes"]
    
    while True:
        # Abre arquivos.json
        with open("arquivos.json", mode="r") as bibliotecaDeArquivos:
            arquivos = json.load(bibliotecaDeArquivos)
        opcoes = input("Comandos disponíveis:\n"
                                " [1] - Listar arquivos\n"
                                " [2] - Ler arquivo\n"
                                " [3] - Executar arquivo\n"
                                " [4] - Excluir arquivo\n"
                                " [5] - Criar arquivo\n"
                                " [6] - Sair\n")
        # Listar arquivos:
        if opcoes == "1":
            x = 0
            print("\nArquivos Disponíveis")
            # print(arquivos[2]["arquivo"])
            for arquivo in arquivos:
                print(f"{x+1} - {arquivo['arquivo']};")
                x = x+1
            print()

        # Ler arquivos:
        elif opcoes == "2":
            lerArquivo = input("Qual arquivo você deseja ler: ")
            
            if any(arquivo["arquivo"] == lerArquivo for arquivo in arquivos):               
                if lerArquivo in permissoesDoUsuario["read"]:
                    print(f"\nAcesso permitdo!\nVocê está lendo o arquivo {lerArquivo}!\n")
                else:
                    print("\nAcesso negado!\nVocê não possui permissão para ler este arquivo!\n")
               
            else:
                print("Este arquivo não existe!")

        # Executar arquivo:
        elif opcoes == "3":
            executarArquivo = input("Qual arquivo você deseja executar: ")
            if any(arquivo["arquivo"] == executarArquivo for arquivo in arquivos):               
                if executarArquivo in permissoesDoUsuario["write"]:
                    print(f"\nAcesso permitdo!\nVocê está escrevendo no arquivo {executarArquivo}!\n")
                else:
                    print("\nAcesso negado!\nVocê não possui permissão para escrever neste arquivo!\n")
               
            else:
                print("Este arquivo não existe!")

        # Deletar arquivo:
        elif opcoes == "4":
            deletarArquivo = input("Qual arquivo você deseja deletar: ")
            if any(arquivo["arquivo"] == deletarArquivo for arquivo in arquivos):               
                if deletarArquivo in permissoesDoUsuario["delete"]:
                    os.remove(deletarArquivo) 
                    print("\nAcesso permitido!\nArquivo deletado com sucesso!\n")
                else:
                    print("\nAcesso negado!\nVocê não possui permissão para deletar este arquivo!\n")
               
            else:
                print("Este arquivo não existe!")

        # Criar arquivo:
        elif opcoes == "5":
            criarArquivo = input("Digite o arquivo que você deseja criar: ")
            newArquivo = {"arquivo": criarArquivo}

            arquivos.append(newArquivo)
            with open("arquivos.json", mode="w") as arquivo:
                    json.dump(arquivos, arquivo)
            print(f"\nArquivo {criarArquivo} criado com sucesso!\n")

            for usuario_data in permissoesDoUsuario:
                if usuario_data[login] == permissoes["login"]:
                    usuario_data["permissoes"]["read"].append(newArquivo)
                    usuario_data["permissoes"]["write"].append(newArquivo)
                    usuario_data["permissoes"]["delete"].append(newArquivo)
                    break
                else:
                    print("Deu errado")
               
                with open("usuariosPermissoes.json", mode="w") as arquivo:
                    json.dump(permissoes, arquivo)

            print(f"Permissões concedidas para {login} no arquivo {criarArquivo}.\n")



        # Sair:
        elif opcoes == "6":
            print("Até a próxima :3")
            break
        else:
            print("Opção Inválida!")

while True:
    # Abre o arquivo usuariosPermissoes.json  
    with open("usuariosPermissoes.json", mode="r") as arquivo:
        permissoes = json.load(arquivo)

    menuInicial = input(f"\nBem-vindo \n--------------------------\n"
                        " [1] - Login\n [2] - Cadastrar \n [3] - Sair"
                        "\n--------------------------\n")
    
    # Login:
    autentificado = False
    if menuInicial == "1":
        tentativas = 0
        while tentativas < 5:
            login = input("Login: ")
            senha = getpass.getpass("Senha: ")
            if any(usuario["login"] == login and usuario["senha"] == senha for usuario in permissoes):
                print(f"\n Usuário autenticado!\n Seja Bem-vindo(a) {login}!\n")
                autentificado = True

                # Redirecionando Usuário para o menu de comandos
                menuOpcoes(login, autentificado)
                break
            else:
                print(f"\n Login ou Senha incorretos, por favor tente novamente, você tem {5 - tentativas} restantes!\n")
                tentativas +=1
           

    # Cadastrar:
    elif menuInicial == "2":
        tentativas = 0
        while tentativas < 5:
            newLogin = input("Digite o seu nome (login): ")
            if any(usuario["login"] == newLogin for usuario in permissoes):
                print("\nEste login já está em uso. Escolha outro.\n")
                continue

            newSenha = getpass.getpass("Digite uma senha: ")
            confirmarSenha = getpass.getpass("Confirmar senha: ")
            
            if newSenha == confirmarSenha:
                newUsuario = {"login": newLogin,
                            "senha": newSenha,
                            "permissoes": {"read": [],
                                            "write": [],
                                            "delete": []}}
                
                permissoes.append(newUsuario)

                with open("usuariosPermissoes.json", mode="w") as arquivo:
                    json.dump(permissoes, arquivo)
                print("\nUsuário cadastrado com sucesso!\n")
                break

            else:
                print("\nAs senhas não coincidem. Tente novamente\n")
                tentativas += 1
                continue

    # Sair:
    elif menuInicial == "3":
        print("Obrigada pela visita :) \nAté Breve!\n")
        break

    # Excesão:
    else:
        print("\nErro! Opção inválida!\n")

if autentificado == True:
    print("ok")
else:
    print("not ok :(")
                          