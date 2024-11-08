import tkinter as tk
import requests
from Elementos.botoes import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ConsultaAcoes(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.area_grafico = None

        self.pack(fill="both", expand=True)

        self.frame = tk.Frame(self, bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        # Título
        self.label_titulo = tk.Label(self.frame, text="Consulta de Ações - Alpha Vantage", bg="#ffffff", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)

        self.frame_acoes = tk.Frame(self.frame, bg="#ffffff")
        self.frame_acoes.pack(fill="both", expand=True)
        self.api_key = self.get_api_key()


        simbolos = self.get_simbolos()

        # Criação da caixa de seleção para escolher um símbolo
        self.simbolo_selecionado = tk.StringVar(self.frame_acoes)
        self.simbolo_selecionado.set(simbolos[0])  # Define o primeiro símbolo como padrão

        self.caixa_selecao = tk.OptionMenu(self.frame_acoes, self.simbolo_selecionado, *simbolos)

        # Configurações de estilo
        self.caixa_selecao.config(
            bg="#3333cc",          # Fundo azul
            fg="white",         # Texto branco para contraste
            relief="flat",      # Estilo flat
            font=("Arial", 12, "bold")  # Fonte Arial tamanho 12
        )

        self.caixa_selecao.pack(pady=10)

        altura = 30
        largura = 100
    
        self.botao_consultar = RoundedButton(self.frame_acoes, text="Consultar", command=lambda: self.exibir_acoes(self.simbolo_selecionado.get()), radius=altura/3, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 13, "bold"), width=largura, height=altura)
        self.botao_consultar.pack(pady=10)
            
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
    
    def exibir_acoes(self, simbolo):

        if self.area_grafico:
            self.area_grafico.destroy()

        dados = self.consultar_acao(simbolo)



        self.area_grafico = tk.Frame(self.frame_acoes, bg="#ffffff")
        self.area_grafico.pack(fill="x", expand=True)

        datas = []
        fechamentos = []
        for data, fechamento in dados:
            datas.append(data)
            fechamentos.append(fechamento)

        # Criar o gráfico de linha usando Matplotlib
        fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
        ax.plot(datas, fechamentos, marker='o', color='blue', linestyle='-')
        
        # Configurações do gráfico
        ax.set_title(f'Ativo: {simbolo}')
        ax.set_xlabel('Data')
        ax.set_ylabel('Fechamento (USD)')

        # Exibir apenas algumas datas no eixo X (ex: uma a cada 5 datas)
        intervalo = max(1, len(datas) // 6)  # ajusta o intervalo de ticks no eixo X
        ax.set_xticks(datas[::intervalo])
        ax.tick_params(axis='x', rotation=0)

        # Adicionar grid
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray') 


        # Inserir o gráfico no Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.area_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

