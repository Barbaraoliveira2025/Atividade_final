# noticias_api_completo.py
# Projeto de conclusão: Consulta de notícias usando NewsAPI
# Criado por: Bárbara Oliveira 💛

import requests
import os
from dotenv import load_dotenv

# Carrega a chave da API do arquivo .env
load_dotenv()
api_key = os.getenv("API_KEY_NEWS")

# Verifica se a chave foi carregada
if not api_key:
    raise ValueError("API Key não encontrada. Certifique-se de ter criado o arquivo .env com API_KEY_NEWS.")

# Lista para armazenar o histórico de buscas
historico = []

# Início do menu interativo
while True:
    print("\n===== PORTAL DE NOTÍCIAS DA BÁRBARA =====")
    print("1. Buscar notícias")
    print("2. Mostrar histórico de buscas")
    print("3. Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        tema = input("Digite o tema da notícia que deseja buscar: ")
        quantidade = 5  # Padrão fixo

        # Define a URL e os parâmetros da requisição
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": tema,
            "pageSize": quantidade,
            "apiKey": api_key,
            "language": "pt"
        }

        resposta = requests.get(url, params=params)

        if resposta.status_code == 200:
            dados = resposta.json()
            artigos = dados.get("articles", [])

            if not artigos:
                print("Nenhuma notícia encontrada.")
            else:
                print(f"\nForam encontradas {len(artigos)} notícias sobre '{tema}':\n")
                for i, noticia in enumerate(artigos, start=1):
                    print(f"{i}. {noticia.get('title', 'Sem título')}")
                    print(f"   Autor: {noticia.get('author', 'Desconhecido')}")
                    print(f"   Fonte: {noticia['source'].get('name', 'Sem fonte')}")
                    print(f"   Resumo: {noticia.get('description', 'Sem resumo disponível.')}")
                    print("-" * 50)

                # Adiciona a busca ao histórico
                historico.append((tema, len(artigos)))

                # Saber mais
                opcao_detalhe = input("Deseja saber mais sobre alguma notícia? (Digite o número ou 0 para pular): ")
                if opcao_detalhe.isdigit():
                    indice = int(opcao_detalhe)
                    if 1 <= indice <= len(artigos):
                        noticia = artigos[indice - 1]
                        print("\n==== MAIS DETALHES ====")
                        print(f"Título: {noticia.get('title', 'Sem título')}")
                        print(f"Conteúdo completo: {noticia.get('content', 'Não fornecido pela fonte')}")
                        print(f"Link para a matéria completa: {noticia.get('url', 'Não disponível')}")
                        print("=" * 50)
        else:
            print("Erro ao buscar notícias. Verifique sua conexão ou chave da API.")

    elif escolha == "2":
        if not historico:
            print("Nenhuma busca realizada ainda.")
        else:
            print("\nHistórico de buscas:")
            for i, item in enumerate(historico, start=1):
                print(f"{i}. Tema: {item[0]} → {item[1]} notícias")

    elif escolha == "3":
        print("Saindo do programa. Obrigada por usar o portal de notícias. 💛")
        break

    else:
        print("Opção inválida. Tente novamente.")
