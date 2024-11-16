import tkinter as tk
import requests
from Elementos.botoes import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RemoverInvestimentos(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app
        self.mensgemDeConfirmacao = None

        self.pack(fill="both", expand=True)

        self.frame = tk.Frame(self, bg="#ffffff")
        self.frame.pack(fill="both", expand=True)

        # Título
        self.label_titulo = tk.Label(self.frame, text="Remover investimentos", bg="#ffffff", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)

        self.frame_acoes = tk.Frame(self.frame, bg="#ffffff")
        self.frame_acoes.pack(fill="both", expand=True)

        self.gerar_caixa_de_selecao()

        criarBackButton(self, app)
    
    def get_simbolos(self):
        conn = self.app.conn
        cursor = conn.cursor()
        cursor.execute(f"select i.simbolo from investimentos i join usuarios u on u.usuario_id = i.usuario_id where u.email = '{self.app.usuario}'")
        resultado = cursor.fetchall()
        simbolos = []
        for simbolo in resultado:
            simbolos.append(simbolo[0])
        return simbolos
    
    def remover_investimento(self):
        if self.mensgemDeConfirmacao:
            self.mensgemDeConfirmacao.destroy()
        try:
            conn = self.app.conn
            cursor = conn.cursor()

            investimento_nome = self.simbolo_selecionado.get()
            cursor.execute(f"delete from investimentos where simbolo = '{investimento_nome}'")
            conn.commit()
            

            # mensagem de sucesso
            self.mensgemDeConfirmacao = tk.Label(self.frame_acoes, text="Investimento removido com sucesso", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")


            self.mensgemDeConfirmacao.pack(pady=10)
            
            self.caixa_selecao.destroy()
            self.botao_consultar.destroy()
            self.gerar_caixa_de_selecao()


        except:
            # mensagem de erro
            self.mensgemDeConfirmacao = tk.Label(self.frame, text="Erro ao remover investimento", bg="#f0f4f7", font=("Arial", 12, "bold"), fg="red")

            self.mensgemDeConfirmacao.pack(pady=10)
    
    def gerar_caixa_de_selecao(self):


            
        simbolos = self.get_simbolos()
        if simbolos == []:

            if self.mensgemDeConfirmacao:
                self.mensgemDeConfirmacao.destroy()


            self.mensgemDeConfirmacao = tk.Label(self.frame_acoes, text="Nenhum investimento encontrado", bg="#ffffff", font=("Arial", 12, "bold"), fg="red")
            self.mensgemDeConfirmacao.pack(pady=10, expand=True, fill="both")

            return


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

        self.caixa_selecao.pack(pady=(100, 30))

        altura = 30
        largura = 100
    
        self.botao_consultar = RoundedButton(self.frame_acoes, text="Remover", command=self.remover_investimento, radius=altura/3, bg="#D9534F", hover_bg="#E08E8B", fg="white", font=("Arial", 13, "bold"), width=largura, height=altura)
        self.botao_consultar.pack(pady=10)
