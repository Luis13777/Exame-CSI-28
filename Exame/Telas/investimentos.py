import tkinter as tk
import requests
from Elementos.botoes import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ConsultaAcoes(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.pack(fill="both", expand=True)

        self.frame = tk.Frame(self, bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        # Título
        self.label_titulo = tk.Label(self.frame, text="Consulta de Ações - Alpha Vantage", bg="#ffffff", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)

        self.frame_acoes = tk.Frame(self.frame, bg="#ffffff")
        self.frame_acoes.pack(fill="both", expand=True)
        self.api_key = self.get_api_key()

        self.exibir_acoes()

        criarBackButton(self, app)

    def get_api_key(self):
        conn = self.app.conn
        cursor = conn.cursor()
        cursor.execute("SELECT api_key FROM usuarios WHERE email=?", (self.app.usuario))
        api_key = cursor.fetchone()[0]
        cursor.close()
        return api_key
    
    def get_simbolos(self):
        conn = self.app.conn
        cursor = conn.cursor()
        cursor.execute(f"select i.simbolo from investimentos i join usuarios u on u.usuario_id = i.usuario_id where u.email = '{self.app.usuario}'")
        resultado = cursor.fetchall()
        simbolos = []
        for simbolo in resultado:
            simbolos.append(simbolo[0])
        cursor.close()
        return simbolos
    
    def consultar_acao(self, simbolo):
        api_key = self.api_key
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


        # Pegar os últimos 7 dias úteis
        ultimos_30_dias = []
        for i, (data, valores) in enumerate(daily_data.items()):
            # if i >= 7:
            #     break
            fechamento = float(valores["4. close"])
            ultimos_30_dias.append((data, fechamento))

        return ultimos_30_dias[::-1]
    
    def exibir_acoes(self):
        simbolos = self.get_simbolos()
        for i, simbolo in enumerate(simbolos):
            dados = self.consultar_acao(simbolo)

            area_grafico = tk.Frame(self.frame_acoes, bg="#ffffff")
            area_grafico.pack(fill="both", expand=True)

            datas = []
            fechamentos = []
            for data, fechamento in dados:
                datas.append(data)
                fechamentos.append(fechamento)

            # Criar o gráfico de linha usando Matplotlib
            fig, ax = plt.subplots(figsize=(10, 3), dpi=100)
            ax.plot(datas, fechamentos, marker='o', color='blue', linestyle='-')
            
            # Configurações do gráfico
            ax.set_title(f'{simbolo}')
            ax.set_xlabel('Data')
            ax.set_ylabel('Fechamento (USD)')
            ax.tick_params(axis='x', rotation=45)

            # Exibir apenas algumas datas no eixo X (ex: uma a cada 5 datas)
            intervalo = max(1, len(datas) // 10)  # ajusta o intervalo de ticks no eixo X
            ax.set_xticks(datas[::intervalo])
            ax.tick_params(axis='x', rotation=45)

            # Inserir o gráfico no Tkinter
            canvas = FigureCanvasTkAgg(fig, master=area_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack()




