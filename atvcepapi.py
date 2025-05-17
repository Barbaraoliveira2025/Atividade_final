import requests  # Biblioteca para fazer requisições HTTP

# Certifique-se de ter a biblioteca requests instalada:
# pip install requests

# Lista global para armazenar os contatos
contatos = []

def buscar_endereco_por_cep(cep):
    """
    Busca o endereço completo a partir de um CEP (código postal brasileiro) usando a API ViaCEP.
    Retorna um dicionário com rua, bairro, cidade e estado se o CEP for válido.
    Caso o CEP seja inválido ou não encontrado, retorna None.
    """
    # Removendo possíveis caracteres inválidos do CEP (como '-' ou espaços)
    cep = cep.strip().replace("-", "").replace(".", "").replace(" ", "")
    # Verifica se o CEP tem 8 dígitos numéricos
    if not cep.isdigit() or len(cep) != 8:
        return None  # Formato de CEP inválido
    try:
        # Faz a requisição para a API ViaCEP
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    except Exception as e:
        # Em caso de erro na conexão ou se a biblioteca requests não estiver disponível
        return None
    # Verifica se a requisição foi bem-sucedida (código 200 OK)
    if response.status_code != 200:
        return None
    # Converte a resposta JSON em dicionário Python
    dados = response.json()
    # Verifica se a resposta indica erro (CEP inexistente)
    if "erro" in dados:
        return None
    # Retorna um dicionário com os dados de endereço relevantes
    endereco = {
        "rua": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
        "estado": dados.get("uf", "")
    }
    return endereco

def cadastrar_contato():
    """Cadastra um novo contato solicitando os dados do usuário e obtendo o endereço via CEP."""
    print("\n-- Cadastrar novo contato --")
    nome = input("Nome: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    cep = input("CEP (apenas números): ")
    # Busca o endereço a partir do CEP fornecido
    endereco = buscar_endereco_por_cep(cep)
    if endereco is None:
        print("CEP inválido ou não encontrado. Não foi possível cadastrar o endereço.")
        print("Cadastro de contato cancelado.\n")
        return
    # Cria o dicionário do contato com um código (ID) único (índice da lista + 1)
    codigo = len(contatos) + 1
    contato = {
        "codigo": codigo,
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cep": cep.strip().replace("-", "").replace(" ", ""),
        "rua": endereco["rua"],
        "bairro": endereco["bairro"],
        "cidade": endereco["cidade"],
        "estado": endereco["estado"]
    }
    contatos.append(contato)
    print(f"Contato '{nome}' cadastrado com sucesso!\n")

def editar_contato():
    """Edita um contato existente identificado pelo código (ID), permitindo alterar seus dados."""
    if not contatos:
        print("\nNenhum contato cadastrado para editar.\n")
        return
    print("\n-- Editar contato --")
    codigo_str = input("Digite o código do contato a editar: ")
    if not codigo_str.isdigit():
        print("Código inválido.\n")
        return
    codigo = int(codigo_str)
    # Ajusta o índice interno (código começa em 1, índice da lista começa em 0)
    indice = codigo - 1
    if indice < 0 or indice >= len(contatos):
        print("Contato não encontrado.\n")
        return
    contato = contatos[indice]
    # Mostra os dados atuais do contato e solicita novas informações (pressione Enter para manter o valor atual)
    print(f"Editando contato #{codigo} - Nome atual: {contato['nome']}")
    novo_nome = input(f"Novo nome (Enter para manter '{contato['nome']}'): ")
    novo_email = input(f"Novo email (Enter para manter '{contato['email']}'): ")
    novo_telefone = input(f"Novo telefone (Enter para manter '{contato['telefone']}'): ")
    novo_cep = input(f"Novo CEP (Enter para manter '{contato['cep']}'): ")
    # Se o usuário pressionar Enter sem digitar nada, mantemos o valor antigo em cada campo
    if novo_nome.strip() == "":
        novo_nome = contato["nome"]
    if novo_email.strip() == "":
        novo_email = contato["email"]
    if novo_telefone.strip() == "":
        novo_telefone = contato["telefone"]
    if novo_cep.strip() == "":
        novo_cep = contato["cep"]
    # Se o CEP foi alterado, busca o novo endereço; caso contrário, mantém o endereço atual
    endereco = None
    if novo_cep != contato["cep"]:
        endereco = buscar_endereco_por_cep(novo_cep)
        if endereco is None:
            print("CEP inválido ou não encontrado. O endereço permanecerá inalterado.")
            # Mantém o CEP antigo e endereço antigo
            novo_cep = contato["cep"]
            endereco = {
                "rua": contato["rua"],
                "bairro": contato["bairro"],
                "cidade": contato["cidade"],
                "estado": contato["estado"]
            }
    else:
        # CEP não alterado, copia o mesmo endereço existente
        endereco = {
            "rua": contato["rua"],
            "bairro": contato["bairro"],
            "cidade": contato["cidade"],
            "estado": contato["estado"]
        }
    # Atualiza os dados do contato com as (possíveis) novas informações
    contato["nome"] = novo_nome
    contato["email"] = novo_email
    contato["telefone"] = novo_telefone
    contato["cep"] = novo_cep
    contato["rua"] = endereco["rua"]
    contato["bairro"] = endereco["bairro"]
    contato["cidade"] = endereco["cidade"]
    contato["estado"] = endereco["estado"]
    print("Contato atualizado com sucesso!\n")

def deletar_contato():
    """Deleta um contato existente, removendo-o da lista de contatos."""
    if not contatos:
        print("\nNenhum contato cadastrado para deletar.\n")
        return
    print("\n-- Deletar contato --")
    codigo_str = input("Digite o código do contato a deletar: ")
    if not codigo_str.isdigit():
        print("Código inválido.\n")
        return
    codigo = int(codigo_str)
    indice = codigo - 1
    if indice < 0 or indice >= len(contatos):
        print("Contato não encontrado.\n")
        return
    contato = contatos.pop(indice)  # Remove o contato da lista
    print(f"Contato '{contato['nome']}' removido com sucesso!\n")
    # Atualiza os códigos dos contatos restantes na lista (para manter a sequência de IDs)
    for i, c in enumerate(contatos, start=1):
        c["codigo"] = i

def mostrar_contatos():
    """Mostra todos os contatos cadastrados e seus detalhes."""
    print("\n-- Lista de Contatos --")
    if not contatos:
        print("Nenhum contato cadastrado.\n")
        return
    # Percorre a lista de contatos e imprime cada um em formato legível
    for c in contatos:
        print(f"Código: {c['codigo']}")
        print(f"Nome: {c['nome']}")
        print(f"Email: {c['email']}")
        print(f"Telefone: {c['telefone']}")
        endereco_formatado = f"{c['rua']}, {c['bairro']}, {c['cidade']} - {c['estado']}"
        print(f"Endereço: {endereco_formatado}")
        print("-" * 40)  # linha separadora para melhor visualização
    print()  # linha em branco após listar todos

def exibir_menu():
    """Exibe o menu de opções na tela."""
    print("===== Sistema de Gerenciamento de Contatos =====")
    print("1. Cadastrar novo contato")
    print("2. Editar um contato existente")
    print("3. Deletar um contato")
    print("4. Mostrar todos os contatos cadastrados")
    print("5. Sair")

def main():
    # Loop principal do menu que mantém o programa em execução até o usuário escolher sair
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-5): ")
        if opcao == "1":
            cadastrar_contato()
        elif opcao == "2":
            editar_contato()
        elif opcao == "3":
            deletar_contato()
        elif opcao == "4":
            mostrar_contatos()
        elif opcao == "5":
            print("Saindo do programa. Até mais!")
            break  # Sai do loop e encerra o programa
        else:
            print("Opção inválida, tente novamente.\n")

# Executa o programa principal (inicia o sistema de contatos)
if __name__ == "__main__":
    main()