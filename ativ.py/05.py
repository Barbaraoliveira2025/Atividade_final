import requests
import os
from dotenv import load_dotenv

load_dotenv()

def buscar_cachorros(quantidade):
    api_key = os.getenv("API_KEY_DOG")

    if not api_key:
        raise ValueError("API Key não encontrada nas variáveis de ambiente.")

    url = "https://api.thedogapi.com/v1/images/search"

    headers = {
        'x-api-key': api_key
    }

    params = {
        "limit": quantidade,
        "has_breeds": 1
    }

    resposta = requests.get(url=url, headers=headers, params=params)

    if resposta.status_code == 200:
        resposta = resposta.json()
        for image in resposta:
            print(image['url'])

    else:
        return None


def menu():
    print("\nMENU")
    print("0. Sair")
    print("1. Buscar imagens de cachorros")

    opcao = input("Digite a opção do menu: ")
    return opcao

while True:

    opcao = menu()
    if opcao == "0":
        break
    elif opcao == "1":
        try:
            quantidade = int(input("Digite a quantidade de cachorros para buscar imagens (máximo de 5):"))
        except ValueError:
            print("Erro de valor. Tente novamente e digite um número válido.")
            continue

        if 5 >= quantidade > 0:
            buscar_cachorros(quantidade)

        else:
            print("Quantidade inválida. Tente novamente.")
    else:
        print("Opção inválida. Tente novamente.")