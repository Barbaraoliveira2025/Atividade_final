def buscar_gatos():
    import requests
    url = "https://api.thecatapi.com/v1/images/search?limit=5"
    resposta = requests.get(url)
    dados = resposta.json()

    for gatinho in dados:
        print(gatinho["url"])

buscar_gatos()