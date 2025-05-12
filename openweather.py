import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY_CLIMA")

if not api_key:
    raise ValueError("API Key não encontrada nas variáveis de ambiente.")

url = 'https://api.openweathermap.org/data/2.5/weather'

params = {
    "appid" : api_key,
    "q":" Blumenau , BR",
    "lang":'pt_br',
    'units': "metric"
}

resposta = requests.get(url = url, params= params)
print (resposta.status_code)
#print (resposta.json())
resposta_json = resposta.json()

clima = resposta_json["weather"][0]["description"]
temperatura = resposta_json["main"]["temp"]
 
print(f"Em Blumenau, o clima é {clima}"
      f" e está fazendo {temperatura} °C")