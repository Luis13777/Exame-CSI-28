import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from BancoDeDados import *
from Elementos.botoes import *

class MainMenu(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root, bg="#ffffff")
        self.app = app
        self.conn = self.app.conn
        
        app.root.geometry("900x700")

        # Título
        label_title = tk.Label(self, text=f"Bem vindo {self.get_usuario_id()}", font=("Arial", 24, "bold"), bg="#ffffff")
        label_title.pack(pady=20)
        self.label_title = label_title

        # Frame para os botões de opções
        self.options_frame = tk.Frame(self, bg="#ffffff")
        self.options_frame.pack(fill="both", expand=True)

        # Botões de opções
        self.create_option_buttons()

        # Variável de controle para o estado do menu lateral
        self.menu_open = False

        # Criar um frame para o menu lateral que cobre toda a altura da tela
        self.sidebar = tk.Frame(self, bg="#333", width=200)
        self.sidebar.place(x=-200, y=0, relheight=1)  # Define a altura relativa a 100% da janela

        self.box_de_botoes = tk.Frame(self.sidebar, bg="#333")
        self.box_de_botoes.pack(fill="x", expand=False, pady=75)

        # Adicionar botões no menu lateral com mais espaçamento
        self.btn_logout = tk.Button(self.box_de_botoes, text="Logout", command=self.logout, bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)
        
        self.editar_perfil = tk.Button(self.box_de_botoes, text="Editar Perfil", command=self.editar_remover_gasto, bg="#444", fg="white", font=("Arial", 12), padx=10, pady=10)

        self.editar_perfil.pack(fill="x", pady=10, padx=20)
        self.btn_logout.pack(fill="x", pady=10, padx=20)

        # Botão que alterna o menu lateral
        self.toggle_btn = tk.Button(self, text="☰", command=self.toggle_sidebar,
                                    bg="#333", fg="white", padx=10, pady=5, font=("Arial", 16))
        self.toggle_btn.place(x=10, y=10)

    def create_option_buttons(self):

        largura = 300

        btn_consultar = RoundedButton(self.options_frame, text="Consultar Gastos", command=self.show_chart, radius=20, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 14, "bold"), width=largura, height=60)

        btn_opcao2 = RoundedButton(self.options_frame, text="Adicionar Gastos", command=self.adicionar_gasto, radius=20, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 14, "bold"), width=largura, height=60)

        btn_opcao3 = RoundedButton(self.options_frame, text="Editar Gastos", command=self.editar_remover_gasto, radius=20, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 14, "bold"), width=largura, height=60)

        btn_opcao4 = RoundedButton(self.options_frame, text="Consultar Investimentos", command=self.show_chart, radius=20, bg="#3333cc", hover_bg="#6666ff", fg="white", font=("Arial", 14, "bold"), width=largura, height=60)
        
    
        # Usando grid para que os botões ocupem o espaço disponível
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(2, weight=5)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        # Posiciona os botões na grid
        btn_consultar.grid(row=0, column=0, sticky="nsew", padx=5, pady=20)
        btn_opcao2.grid(row=0, column=1, sticky="nsew", padx=5, pady=20)
        btn_opcao3.grid(row=1, column=0, sticky="nsew", padx=5, pady=20)
        btn_opcao4.grid(row=1, column=1, sticky="nsew", padx=5, pady=20)

    def show_chart(self):

        self.app.show_frame("ConsultarGastos")
        

    def toggle_sidebar(self):
        self.sidebar.tkraise()
        self.toggle_btn.tkraise()
        if self.menu_open:
            # Animação para fechar o menu
            for i in range(0, 201, 20):
                self.sidebar.place(x=-i, y=0, relheight=1)
                self.update()
            self.menu_open = False
        else:
            # Animação para abrir o menu
            for i in range(-200, 1, 20):
                self.sidebar.place(x=i, y=0, relheight=1)
                self.update()
            self.menu_open = True

    def get_usuario_id(self):
        email_usuario = self.app.usuario
        query = f"SELECT nome FROM usuarios WHERE email = '{email_usuario}'"
        cursor = self.conn.cursor()
        cursor.execute(query)
        usuario_id = cursor.fetchone()[0]
        cursor.close()
        return usuario_id

    def adicionar_gasto(self):
        self.app.show_frame("AdicionarGasto")

    def editar_remover_gasto(self):
        self.app.show_frame("EditarGasto")

    def logout(self):
        self.conn.close()
        self.app.usuario = None
        self.app.show_frame("LoginScreen")
