import tkinter as tk
from tkinter import font
from Elementos.botoes import *
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class consultarGastos(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app

        self.canvas_widget = None
        self.label_no_data = None

        self.consult_window = tk.Frame(self, bg="#ffffff")
        self.consult_window.pack(fill="both", expand=True)  # Para ocupar todo o espaço


        # Botão para voltar
        self.back_button = tk.Button(self, text="←", font=("Arial", 20), bg="#333333", fg="white", command=lambda: self.app.show_frame("MainMenu"))
        self.back_button.place(relx=1.0, y=10, x=-10, anchor="ne")

        
        self.consult_window.grid_rowconfigure(0, weight=1)
        self.consult_window.grid_rowconfigure(1, weight=4)
        self.consult_window.columnconfigure(0, weight=1)

        # Exibir campos de data
        frame_data = tk.Frame(self.consult_window, bg="#ffffff")
        self.frame_data = frame_data
        frame_data.grid(row=0, column=0, padx=100, sticky="nsew")

        self.lugarParaOGrafico = tk.Frame(self.consult_window, bg="#ffffff")
        self.lugarParaOGrafico.grid(row=1, column=0, sticky="nsew")

        self.frame_data.grid_rowconfigure(0, weight=1)
        self.frame_data.grid_rowconfigure(1, weight=1)
        self.frame_data.grid_rowconfigure(2, weight=1)
        self.frame_data.grid_rowconfigure(3, weight=1)
        self.frame_data.grid_columnconfigure(0, weight=3)
        self.frame_data.grid_columnconfigure(1, weight=3)
        self.frame_data.grid_columnconfigure(2, weight=1)
        self.frame_data.grid_columnconfigure(3, weight=3)
        self.frame_data.grid_columnconfigure(4, weight=3)

        tk.Label(self.frame_data, text=f"Gastos", font=("Arial", 24, "bold"), bg="#ffffff").grid(row=0, column=2, padx=10)

        tk.Label(self.frame_data, text="Data Inicial (YYYY-MM-DD):", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=1, column=0, padx=5, columnspan=3)
        
        self.entry_data_inicial = tk.Entry(self.frame_data, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")


        self.entry_data_inicial.grid(row=2, column=0, columnspan=3)

        tk.Label(self.frame_data, text="Data Final (YYYY-MM-DD):", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=1, column=2, padx=5, columnspan=3)
        self.entry_data_final = tk.Entry(self.frame_data, bg="#f0f0f0", fg="#333333", font=("Arial", 10, "bold"), bd=5, relief="flat", justify="center")

        self.entry_data_final.grid(row=2, column=2, columnspan=3)

        # Botão para gerar o gráfico

        largura = 150

        btn_gerar = RoundedButton(self.frame_data, text="Gerar Gráfico", command=self.create_gasto_chart, radius=20, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 12, "bold"), width=largura, height=40)

        btn_gerar.grid(row=3, sticky="nsew", column=1, padx=10, columnspan=3)

    def create_gasto_chart(self):
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None
        """Cria o gráfico de gastos com base nos dados do usuário"""
        data_inicial = self.entry_data_inicial.get()
        data_final = self.entry_data_final.get()

        # gastos = self.fetch_gastos_data()

        gastos = self.fetch_gastos_data(data_inicial, data_final)

        if not gastos.empty:

            if self.label_no_data:
                self.label_no_data.destroy()

            categorias = gastos['categoria'].unique()
            valores = [gastos[gastos['categoria'] == cat]['valor'].sum() for cat in categorias]

            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
            ax.axis('equal')  # Mantém o gráfico circular

            # Desenha o gráfico
            canvas = FigureCanvasTkAgg(fig, master=self.lugarParaOGrafico)
            canvas_widget = canvas.get_tk_widget()

            # Armazena a referência do canvas para permitir remoção futura
            self.canvas_widget = canvas_widget

            # Posiciona o canvas na interface usando grid
            canvas_widget.place(relwidth=1, relheight=1)
            # canvas_widget.pack(fill="both", expand=True)




            # Finalmente desenha o gráfico
            canvas.draw()

        else:
            self.label_no_data = tk.Label(self.frame_data, text="Nenhum dado de gasto disponível.", bg="#f0f4f7", font=("Arial", 12))
            self.label_no_data.grid(row=5, column=0, columnspan=5)  # Usando grid ao invés de pack

    def fetch_gastos_data(self, data_inicial, data_final):
        """Busca os dados de gastos do usuário logado"""
        email_usuario = self.app.usuario
        query = f"SELECT g.categoria, g.valor, g.data FROM usuarios u JOIN gastos g ON u.usuario_id = g.usuario_id WHERE u.email = '{email_usuario}'"
        query = ("""
        SELECT g.categoria, g.valor, g.data 
        FROM usuarios u 
        JOIN gastos g ON u.usuario_id = g.usuario_id 
        WHERE u.email = ? AND g.data BETWEEN ? AND ?
        """)
        cursor = self.app.conn.cursor()
        # cursor.execute(query)
        cursor.execute(query, (email_usuario, data_inicial, data_final))

        rows = cursor.fetchall()
        if rows:
            data = pd.DataFrame.from_records(rows, columns=['categoria', 'valor', 'data'])
        else:
            data = pd.DataFrame(columns=['categoria', 'valor', 'data'])

        cursor.close()
        return data