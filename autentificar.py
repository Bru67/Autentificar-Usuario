import json

# Feito por: BRUNA DA SILVA CARNELOSSI
# Sistema de Autenticação de  Usuarios utilizando formato JSON para armazenar dados de usuários

with open("dadosUsuarios.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)  
# for dado in dados:
#     print(dado, "\n")

tentativas = 0
while tentativas <= 5:
    
    for dado in dados:
        login = input("Login: ")
        senha = input("Senha: ")
        if dado["nome"] == login and dado["senha"] == senha:
            print(f"Seja Bem-vindo: {login}")
            break  
            
        else:
            print("Login ou Senha incorretos, por favor tente novamente")
            tentativas +1
            
            if tentativas == 5:
                print("Muitas tentativas! Acesso Bloqueado!")
    break
