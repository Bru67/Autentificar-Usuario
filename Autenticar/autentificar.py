import json

# Feito por: BRUNA DA SILVA CARNELOSSI
# Sistema de Autenticação de  Usuarios utilizando formato JSON para armazenar dados de usuários

# Abre o arquivo dadosUsuarios.json
try:
    with open("dadosUsuarios.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)  
except FileNotFoundError:
    dados = [] 

autentificado = False
tentativas = 0

while tentativas <= 5:
    login = input("Login: ")
    senha = input("Senha: ")
    if any(dado["nome"] == login and dado["senha"] == senha for dado in dados):
        print(f"\n Seja Bem-vindo: {login}\n")
        autentificado = True
        break
                            
    else:
        print("\n Login ou Senha incorretos, por favor tente novamente \n")
        tentativas +=1

    if autentificado == True:
        break
    
    if tentativas == 5:   
        # Abre o arquivo usuariosBloqueados.json
        try:
            with open("usuariosBloqueados.json", "r", encoding="utf-8") as arquivo:
                bloqueados = json.load(arquivo)  
        except FileNotFoundError:
            bloqueados = []  

        novoUsuarioBloqueado =  {"nome": login, "senha": senha}
        bloqueados.append(novoUsuarioBloqueado)

        with open("usuariosBloqueados.json", "w", encoding="utf-8") as arquivo2:
            json.dump(bloqueados, arquivo2, indent=4, ensure_ascii=False)
        print("Muitas tentativas! Acesso Bloqueado!")
        break
    elif autentificado == True:
        break