import getpass
import json
import os


# Acesso do Administrador - Atribuir Permissão
def atribuirPermissao():
    with open("usuariosPermissoes.json", mode="r") as arquivo:
        permissoes = json.load(arquivo)

    usuario = input("Digite o nome do usuário para atribuir permissões: ").strip()
    usuarioEncontrado = next((u for u in permissoes if u["login"] == usuario), None)

    if not usuarioEncontrado:
        print("Usuário não encontrado!\n")
        return

    tipoPermissao = input("Qual tipo de permissão deseja atribuir? (read / write / delete): ").strip().lower()
    if tipoPermissao not in ["read", "write", "delete"]:
        print("Tipo de permissão inválido!\n")
        return

    with open("arquivos.json", mode="r") as arqs:
        arquivos = json.load(arqs)

    arquivoNome = input("Digite o nome do arquivo: ").strip()
    if not any(a["arquivo"] == arquivoNome for a in arquivos):
        print("Arquivo não encontrado!\n")
        return

    if arquivoNome in usuarioEncontrado["permissoes"][tipoPermissao]:
        print(f"O usuário já possui permissão de {tipoPermissao} para esse arquivo.\n")
    else:
        usuarioEncontrado["permissoes"][tipoPermissao].append(arquivoNome)
        with open("usuariosPermissoes.json", mode="w") as arquivo:
            json.dump(permissoes, arquivo, indent=4)
        print(f"Permissão '{tipoPermissao}' atribuída ao usuário '{usuario}' para o arquivo '{arquivoNome}'.\n")

# Acesso do Administrador - Remover Permissão 
def deletarPermissoes():
    with open("usuariosPermissoes.json", mode="r") as arquivo:
        permissoes = json.load(arquivo)

    usuario = input("Digite o nome do usuário para remover permissões: ").strip()
    usuarioEncontrado = next((u for u in permissoes if u["login"] == usuario), None)

    if not usuarioEncontrado:
        print("Usuário não encontrado!\n")
        return

    tipoPermissao = input("Qual tipo de permissão deseja remover? (read / write / delete): ").strip().lower()
    if tipoPermissao not in ["read", "write", "delete"]:
        print("Tipo de permissão inválido!\n")
        return

    arquivoNome = input("Digite o nome do arquivo: ").strip()

    if not arquivoNome in usuarioEncontrado["permissoes"][tipoPermissao]:
        print(f"O usuário já não possui permissão de {tipoPermissao} para esse arquivo.\n")
    else:
        usuarioEncontrado["permissoes"][tipoPermissao].remove(arquivoNome)
        with open("usuariosPermissoes.json", mode="w") as arquivo:
            json.dump(permissoes, arquivo, indent=4)
        print(f"Permissão '{tipoPermissao}' removida do usuário '{usuario}' para o arquivo '{arquivoNome}'.\n")

# Atribuir permissoes
def garantirPermissoes(usuario, criarArquivo): 
    for usuarioData in permissoes:
            if usuarioData["login"] == usuario:
                usuarioData["permissoes"]["read"].append(criarArquivo)
                usuarioData["permissoes"]["write"].append(criarArquivo)
                usuarioData["permissoes"]["delete"].append(criarArquivo)
                break

    with open("usuariosPermissoes.json", mode="w") as arquivo:
        json.dump(permissoes, arquivo, indent=4)
    print(f"Permissões concedidas para {usuario} no arquivo '{criarArquivo}'.\n")


#  Menu Principal
def menuOpcoes(login):
    with open("usuariosPermissoes.json", mode="r") as arquivo:
        permissoes = json.load(arquivo)
    usuarioAutenticado = next((usuario for usuario in permissoes if usuario["login"] == login), None)
    permissoesDoUsuario = usuarioAutenticado["permissoes"]

    while True:
        with open("arquivos.json", mode="r") as bibliotecaDeArquivos:
            arquivos = json.load(bibliotecaDeArquivos)
        opcoes = input("Comandos disponíveis:\n"
                       " [1] - Listar arquivos\n"
                       " [2] - Ler arquivo\n"
                       " [3] - Executar arquivo\n"
                       " [4] - Excluir arquivo\n"
                       " [5] - Criar arquivo\n"
                       " [6] - Atribuir permissão\n"
                       " [7] - Sair\n")
        
        # Listar Arquivos
        if opcoes == "1":
            print("\nArquivos Disponíveis")
            for idx, arquivo in enumerate(arquivos):
                print(f"{idx+1} - {arquivo['arquivo']};")
            print()

        # Ler Arquivo
        elif opcoes == "2":
            lerArquivo = input("Qual arquivo você deseja ler: ").strip()
            if any(arquivo["arquivo"] == lerArquivo for arquivo in arquivos):               
                if lerArquivo in permissoesDoUsuario["read"]:
                    print(f"\nAcesso permitido!\nVocê está lendo o arquivo {lerArquivo}!\n")
                else:
                    print("\nAcesso negado!\nVocê não possui permissão para ler este arquivo!\n")
            else:
                print("Este arquivo não existe!")

        # Executar Arquivo
        elif opcoes == "3":
            executarArquivo = input("Qual arquivo você deseja executar: ").strip()
            if any(arquivo["arquivo"] == executarArquivo for arquivo in arquivos):               
                if executarArquivo in permissoesDoUsuario["write"]:
                    print(f"\nAcesso permitido!\nVocê está escrevendo no arquivo {executarArquivo}!\n")
                else:
                    print("\nAcesso negado!\nVocê não possui permissão para escrever neste arquivo!\n")
            else:
                print("Este arquivo não existe!")

        # Deletar Arquivo
        elif opcoes == "4":
            deletarArquivo = input("Qual arquivo você deseja deletar: ").strip()
            arquivoEncontrado = next((arquivo for arquivo in arquivos if arquivo["arquivo"] == deletarArquivo), None)

            if not arquivoEncontrado:
                print("Este arquivo não existe na lista de arquivos!")
            elif deletarArquivo not in permissoesDoUsuario["delete"]:
                print("Acesso negado! Você não possui permissão para deletar este arquivo!\n")
            else:
                try:
                    if os.path.exists(arquivoEncontrado):
                        os.remove(arquivoEncontrado)
                        print("Arquivo físico removido com sucesso.")
                    else:
                        print("Arquivo físico não encontrado, removendo apenas da bivlioteca de arquivos JSON.")
                    arquivos.remove(arquivoEncontrado)
                    
                    with open("arquivos.json", mode="w") as arquivo:
                        json.dump(arquivos, arquivo, indent=4)
                    print(f"Arquivo '{deletarArquivo}' deletado com sucesso!\n")

                except Exception as e:
                    print(f"Erro ao deletar o arquivo: {str(e)}")

        # Criar Arquivo
        elif opcoes == "5":
            criarArquivo = input("Digite o arquivo que você deseja criar: ").strip()
            newArquivo = {"arquivo": criarArquivo}
            arquivos.append(newArquivo)

            with open("arquivos.json", mode="w") as arquivo:
                json.dump(arquivos, arquivo)

            print(f"\nArquivo {criarArquivo} criado com sucesso!\n")
            
            garantirPermissoes(login, criarArquivo)
            garantirPermissoes("admin", criarArquivo)


        # Atribuir Permissões pelo Admin
        elif opcoes == "6":
            if login == "admin":
                acessoAdm = input("1 - Atribuir Permissões\n2 - Remover Permisões\n")
                if acessoAdm == "1":    
                    atribuirPermissao()
                elif acessoAdm == "2":
                    deletarPermissoes()
                else:
                    print("Opção Inválida")

            else:
                print("Acesso negado! Somente o usuário 'admin' pode atribuir permissões.\n")

        # Sair
        elif opcoes == "7":
            print("Até a próxima :3")
            break

        else:
            print("Opção Inválida!")

while True:
    with open("usuariosPermissoes.json", mode="r") as arquivo:
        permissoes = json.load(arquivo)

    menuInicial = input(f"\nBem-vindo \n--------------------------\n"
                        " [1] - Login\n [2] - Cadastrar \n [3] - Sair"
                        "\n--------------------------\n")

    autentificado = False

    # Login
    if menuInicial == "1":
        tentativas = 0
        while tentativas < 5:
            login = input("Login: ").strip().lower()
            senha = getpass.getpass("Senha: ")
            if any(usuario["login"] == login and usuario["senha"] == senha for usuario in permissoes):
                print(f"\n Usuário autenticado!\n Seja Bem-vindo(a) {login}!\n")
                autentificado = True
                menuOpcoes(login)
                break
            else:
                print(f"\n Login ou Senha incorretos, por favor tente novamente, você tem {4 - tentativas} tentativas restantes!\n")
                tentativas += 1

    # Cadastro
    elif menuInicial == "2":
        tentativas = 0
        while tentativas < 5:
            newLogin = input("Digite o seu nome (login): ").strip()
            logins_existentes = [usuario["login"].lower() for usuario in permissoes]
            if newLogin.lower() in logins_existentes:
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
                    json.dump(permissoes, arquivo, indent=4)
                print("\nUsuário cadastrado com sucesso!\n")
                break
            else:
                print("\nAs senhas não coincidem. Tente novamente\n")
                tentativas += 1

    # Sair
    elif menuInicial == "3":
        print("Obrigada pela visita :) \nAté Breve!\n")
        break

    else:
        print("\nErro! Opção inválida!\n")

