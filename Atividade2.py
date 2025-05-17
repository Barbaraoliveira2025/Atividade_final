import requests

# Contadores de interações do usuário
contador_posts_vistos = 0
contador_comentarios_vistos = 0
contador_posts_criados = 0

# "Banco de dados" de usuários simulando o login
usuarios = {
    "001": {"email": "ana@email.com", "senha": "1234"},
    "002": {"email": "joao@email.com", "senha": "abcd"},
    "003": {"email": "bia@email.com", "senha": "senha123"}
}

def fazer_login():
    print("=== Login ===")
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")

    for codigo, dados in usuarios.items():
        if dados["email"] == email and dados["senha"] == senha:
            print(f"Login bem-sucedido! Bem-vindo(a), usuário {codigo}")
            return codigo  # retorna o código do usuário logado

    print("E-mail ou senha inválidos. Tente novamente.")
    return None

def visualizar_posts():
    global contador_posts_vistos
    url = "https://jsonplaceholder.typicode.com/posts"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        posts = resposta.json()
        for post in posts[:5]:
            print(f"\nID: {post['id']} | Título: {post['title']}")
            contador_posts_vistos += 1
    else:
        print("Erro ao buscar os posts.")

def visualizar_comentarios():
    global contador_comentarios_vistos
    post_id = input("Digite o ID do post para ver os comentários: ")
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        comentarios = resposta.json()
        for c in comentarios:
            print(f"- {c['name']} ({c['email']}): {c['body']}")
            contador_comentarios_vistos += 1
    else:
        print("Erro ao buscar os comentários.")

def visualizar_posts_usuario(usuario_id):
    global contador_posts_vistos
    url = f"https://jsonplaceholder.typicode.com/posts?userId={usuario_id}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        posts = resposta.json()
        for post in posts:
            print(f"\nID: {post['id']} | Título: {post['title']}")
            contador_posts_vistos += 1
    else:
        print("Erro ao buscar os posts do usuário.")

def filtrar_posts_outro_usuario():
    usuario = input("Digite o ID do usuário que deseja filtrar: ")
    url = f"https://jsonplaceholder.typicode.com/posts?userId={usuario}"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        posts = resposta.json()
        for post in posts:
            print(f"\nID: {post['id']} | Título: {post['title']}")
    else:
        print("Erro ao buscar os posts do usuário.")

def criar_post(usuario_id):
    global contador_posts_criados
    titulo = input("Digite o título do post: ")
    corpo = input("Digite o conteúdo do post: ")

    dados = {
        "userId": usuario_id,
        "title": titulo,
        "body": corpo
    }

    resposta = requests.post("https://jsonplaceholder.typicode.com/posts", json=dados)

    if resposta.status_code == 201:
        print("Post criado com sucesso!")
        contador_posts_criados += 1
    else:
        print("Erro ao criar o post.")

def menu_principal(usuario_logado):
    global contador_posts_vistos, contador_comentarios_vistos, contador_posts_criados

    while True:
        print("\n=== MENU ===")
        print("1. Visualizar todos os posts")
        print("2. Visualizar comentários de um post")
        print("3. Visualizar meus posts")
        print("4. Filtrar posts por outro usuário")
        print("5. Criar um novo post")
        print("6. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            visualizar_posts()
        elif opcao == "2":
            visualizar_comentarios()
        elif opcao == "3":
            visualizar_posts_usuario(usuario_logado)
        elif opcao == "4":
            filtrar_posts_outro_usuario()
        elif opcao == "5":
            criar_post(usuario_logado)
        elif opcao == "6":
            print("\n=== Resumo das interações ===")
            print(f"Posts visualizados: {contador_posts_vistos}")
            print(f"Comentários visualizados: {contador_comentarios_vistos}")
            print(f"Posts criados: {contador_posts_criados}")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Início do programa
usuario_logado = fazer_login()
if usuario_logado:
    menu_principal(usuario_logado)
