import json

# Leitura arquivo de permissões
with open("matriz_controle_acesso.json", mode="r") as arquivo:
    # Lê o conteúdo do arquivo (arquivo.read()) e deserializa o
    # JSON para dicionário do Python (json.loads())
    permissoes = json.loads(arquivo.read())

# Editar as permissões do primeiro usuário
print(permissoes[0]['permissoes'])

permissoes[0]['permissoes']['leitura'].remove('notas.csv')
permissoes[0]['permissoes']['escrita'].remove('notas.csv')
permissoes[0]['permissoes']['remocao'].remove('notas.csv')

print(permissoes[0]['permissoes'])

# Abre arquivo para escrita para salvarmos o resultado das nossas operações
with open('matriz_controle_acesso.json', mode='w') as arquivo:
    # Serializa a variável permissões para JSON
    permissoes_serializado = json.dumps(permissoes)

    # Salvar no arquivo especificado
    arquivo.write(permissoes_serializado)