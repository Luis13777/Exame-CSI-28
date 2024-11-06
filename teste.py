import requests

def consultar_acao(api_key, simbolo):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': simbolo,
        'apikey': api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    print(data)

    # Extrair dados de preços diários
    daily_data = data.get("Time Series (Daily)", {})

    print(daily_data)

    # Pegar os últimos 7 dias úteis
    ultimos_30_dias = []
    for i, (data, valores) in enumerate(daily_data.items()):
        # if i >= 30:
        #     break
        fechamento = float(valores["4. close"])
        ultimos_30_dias.append((data, fechamento))

    # Ordenar os dados em ordem cronológica (do mais antigo ao mais recente)
    ultimos_30_dias = ultimos_30_dias[::-1]

    # Imprimir os resultados
    for data, fechamento in ultimos_30_dias:
        print(f"{data}: {fechamento:.2f}")

# Exemplo de uso
api_key = 'XKYKSMUGDMKP9ET0'
simbolo = 'AAPL'  # símbolo de exemplo para Apple
consultar_acao(api_key, simbolo)
