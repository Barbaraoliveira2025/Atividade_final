import sys
import requests

# Listas de contatos
clientes = []
fornecedores = []

# Função para buscar endereço via CEP
def buscar_cep():
    while True:
        cep = input("Digite o CEP para buscar: ")
        url = f"https://viacep.com.br/ws/{cep}/json/"
        resposta = requests.get(url=url)

        if resposta.status_code == 400:
            print("Erro. Verifique se digitou apenas números (8 dígitos).")
            continue

        resposta = resposta.json()

        if "erro" in resposta:
            print("CEP inválido. Tente novamente.")
            continue
        else:
            return resposta

# Função genérica que aplica a função em uma lista escolhida
def aplicar_funcao(funcao_escolhida):
    resposta = input("Qual lista você quer usar? 'fornecedores' ou 'clientes': ").lower()
    if resposta == "clientes":
        return funcao_escolhida(clientes)
    elif resposta == "fornecedores":
        return funcao_escolhida(fornecedores)
    else:
        print("Opção inválida. Tente novamente.")
        return None

# Menu principal
def menu():
    print("\nMenu de opções:")
    print("""
    0 - Sair
    1 - Cadastrar novo contato
    2 - Editar um contato
    3 - Deletar um contato
    4 - Mostrar todos os contatos cadastrados
    """)
    return input("Escolha uma opção: ")

# Cadastrar contato com CEP
def cadastrar_contato(lista_tipo_contato):
    contato = {}
    contato["codigo"] = len(lista_tipo_contato)
    contato["nome"] = input("Digite o nome: ")
    contato["email"] = input("Digite o email: ")
    contato["telefone"] = input("Digite o telefone: ")
    contato["endereco"] = buscar_cep()
    lista_tipo_contato.append(contato)
    print("Contato cadastrado com sucesso!")

# Editar contato
def editar_contato(lista_tipo_contato):
    codigo = int(input("Digite o código do contato que deseja editar: "))
    if 0 <= codigo < len(lista_tipo_contato):
        print("Contato atual:", lista_tipo_contato[codigo])
        nome = input("Novo nome (Enter para manter): ")
        email = input("Novo email (Enter para manter): ")
        telefone = input("Novo telefone (Enter para manter): ")
        troca_endereco = input("Trocar endereço? (s/n): ").lower()

        if nome:
            lista_tipo_contato[codigo]["nome"] = nome
        if email:
            lista_tipo_contato[codigo]["email"] = email
        if telefone:
            lista_tipo_contato[codigo]["telefone"] = telefone
        if troca_endereco == "s":
            lista_tipo_contato[codigo]["endereco"] = buscar_cep()

        print("Contato atualizado com sucesso!")
    else:
        print("Código inválido.")

# Deletar contato
def deletar_contato(lista_tipo_contato):
    codigo = int(input("Digite o código do contato que deseja deletar: "))
    if 0 <= codigo < len(lista_tipo_contato):
        lista_tipo_contato.pop(codigo)
        for i in range(len(lista_tipo_contato)):
            lista_tipo_contato[i]["codigo"] = i
        print("Contato deletado com sucesso!")
    else:
        print("Código inválido.")

# Mostrar todos os contatos com endereço formatado
def mostrar_contatos(lista_tipo_contato):
    if lista_tipo_contato:
        print("\nLista de contatos:")
        for contato in lista_tipo_contato:
            print(f"Código: {contato['codigo']}")
            print(f"Nome: {contato['nome']}")
            print(f"Email: {contato['email']}")
            print(f"Telefone: {contato['telefone']}")
            endereco = contato["endereco"]
            print(f"Endereço: {endereco['logradouro']}, {endereco['bairro']}, {endereco['localidade']}/{endereco['uf']}")
            print("-" * 40)
    else:
        print("Nenhum contato cadastrado.")

# Loop principal
while True:
    opcao = menu()

    if opcao == "0":
        print("Saindo do programa.")
        break
    elif opcao == "1":
        aplicar_funcao(cadastrar_contato)
    elif opcao == "2":
        aplicar_funcao(editar_contato)
    elif opcao == "3":
        aplicar_funcao(deletar_contato)
    elif opcao == "4":
        aplicar_funcao(mostrar_contatos)
    else:
        print("Opção inválida. Tente novamente.")
