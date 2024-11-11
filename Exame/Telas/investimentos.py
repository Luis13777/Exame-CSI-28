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

        # dados = self.consultar_acao(simbolo)

        dados = [('2024-06-17', 216.67), ('2024-06-18', 214.29), ('2024-06-20', 209.68), ('2024-06-21', 207.49), ('2024-06-24', 208.14), ('2024-06-25', 209.07), ('2024-06-26', 213.25), ('2024-06-27', 214.1), ('2024-06-28', 210.62), ('2024-07-01', 216.75), ('2024-07-02', 220.27), ('2024-07-03', 221.55), ('2024-07-05', 226.34), ('2024-07-08', 227.82), ('2024-07-09', 228.68), ('2024-07-10', 232.98), ('2024-07-11', 227.57), ('2024-07-12', 230.54), ('2024-07-15', 234.4), ('2024-07-16', 234.82), ('2024-07-17', 228.88), ('2024-07-18', 224.18), ('2024-07-19', 224.31), ('2024-07-22', 223.96), ('2024-07-23', 225.01), ('2024-07-24', 218.54), ('2024-07-25', 217.49), ('2024-07-26', 217.96), ('2024-07-29', 218.24), ('2024-07-30', 218.8), ('2024-07-31', 222.08), ('2024-08-01', 218.36), ('2024-08-02', 219.86), ('2024-08-05', 209.27), ('2024-08-06', 207.23), ('2024-08-07', 209.82), ('2024-08-08', 213.31), ('2024-08-09', 216.24), ('2024-08-12', 217.53), ('2024-08-13', 221.27), ('2024-08-14', 221.72), ('2024-08-15', 224.72), ('2024-08-16', 226.05), ('2024-08-19', 225.89), ('2024-08-20', 226.51), ('2024-08-21', 226.4), ('2024-08-22', 224.53), ('2024-08-23', 226.84), ('2024-08-26', 227.18), ('2024-08-27', 228.03), ('2024-08-28', 226.49), ('2024-08-29', 229.79), ('2024-08-30', 229.0), ('2024-09-03', 222.77), ('2024-09-04', 220.85), ('2024-09-05', 222.38), ('2024-09-06', 220.82), ('2024-09-09', 220.91), ('2024-09-10', 220.11), ('2024-09-11', 222.66), ('2024-09-12', 222.77), ('2024-09-13', 222.5), ('2024-09-16', 216.32), ('2024-09-17', 216.79), ('2024-09-18', 220.69), ('2024-09-19', 228.87), ('2024-09-20', 228.2), ('2024-09-23', 226.47), ('2024-09-24', 227.37), ('2024-09-25', 226.37), ('2024-09-26', 227.52), ('2024-09-27', 227.79), ('2024-09-30', 233.0), ('2024-10-01', 226.21), ('2024-10-02', 226.78), ('2024-10-03', 225.67), ('2024-10-04', 226.8), ('2024-10-07', 221.69), ('2024-10-08', 225.77), ('2024-10-09', 229.54), ('2024-10-10', 229.04), ('2024-10-11', 227.55), ('2024-10-14', 231.3), ('2024-10-15', 233.85), ('2024-10-16', 231.78), ('2024-10-17', 232.15), ('2024-10-18', 235.0), ('2024-10-21', 236.48), ('2024-10-22', 235.86), ('2024-10-23', 230.76), ('2024-10-24', 230.57), ('2024-10-25', 231.41), ('2024-10-28', 233.4), ('2024-10-29', 233.67), ('2024-10-30', 230.1), ('2024-10-31', 225.91), ('2024-11-01', 222.91), ('2024-11-04', 222.01), ('2024-11-05', 223.45), ('2024-11-06', 222.72)]

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

